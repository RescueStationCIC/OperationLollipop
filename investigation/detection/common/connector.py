import usb
import time
import random
import logging
from trio import run
from common.definitions import Definitions
from common.deviceprobe import ConnectionError
from common.deviceprobe import DeviceProbe
from common.deviceprobe import ConnectedDevice
from common.connectionpublisher import ConnectionPublisher
from common.connectionhandler import ConnectionHandler
from common.devicedefinition import DeviceDefinition
from common.connectiondefinition import ConnectionDefinition
from common.devicescan import DeviceScan




class Connector():

    def __init__(self, device_definition:DeviceDefinition):
        self.device_definition = device_definition
        self.connection:ConnectedDevice = None
        self.cancel_requested = False
            
    def create_probe(self) -> DeviceProbe:
        raise NotImplementedError    
    
    async def connect(self):
        backoff_max:int = Definitions.CONNECTION_BACKOFF_PERIOD_MAX_MS
        backoff_min:int = Definitions.CONNECTION_BACKOFF_PERIOD_MIN_MS
        if(self.connection is not None):
            raise Exception("already connected.")
        
        device_probe = self.create_probe()        
        while((self.connection is None) and (self.cancel_requested == False)):
            try:
                self.connection = await device_probe.connectIfRecognised(self.device_definition)
            except ConnectionError as e:
                if(e.error_definition == ConnectionError.Definition.INTERFACE_CLAIM_FAILED):
                    sleep_seconds:float = random.randrange(backoff_min, backoff_max) / 1000
                    time.sleep(sleep_seconds)
                else:
                    raise  
                
                
        self.cancel_requested = False
            
     
    def disconnect(self):
        if(self.connection is None):
            self.cancel_requested = True
        else:
            try:
                self.connection.device.reset()
            except usb.core.USBError as e:
                logging.warning("exception, trying to close: " + self.connection.device_definition.device_full_id + " : " + e)
            
            try:
                usb.util.dispose_resources(self.connection.device)
            except usb.core.USBError as e: 
                logging.warning("exception on disposing: " + self.connection.device_definition.device_full_id + " : " + e)
            
            self.connection = None
            


class ConnectorManager:
    
    def __init__(self):
        self.connectors:dict={}
        self.scan_queue:list[DeviceScan]=[]
        self.has_scanned_after_registration = False
        self.processing_scans:bool = False
        self.cancel_current_scan:bool = False
        self.publisher:ConnectionPublisher = ConnectionPublisher(self.get_name())
        self.connectionHandler = ConnectionHandler(self.on_new_connection)
        self.current_connection_attempt:Connector = None 

    def create_connector(self, device_definition:DeviceDefinition) -> Connector:
        raise NotImplementedError
    
    def get_name(self) -> str:
        raise NotImplementedError
    
    def cancel_current_connection_attempts(self):
        if(self.current_connection_attempt is not None):
           self.current_connection_attempt.disconnect()

    def on_new_connection(self,device_full_id):
        if(self.current_connection_attempt.connection.device_definition.device_full_id == device_full_id):
            self.cancel_active_connection_attempts()

        

    async def handle_additions(self,definitions:list[DeviceDefinition]):
        for definition in definitions:
            if (self.cancel_current_scan == False):
                # safety: check to see if we have an incumbent. It will need removing
                incumbent:Connector = None
                try:
                    incumbent: Connector = self.connectors[definition.device_full_id]
                except KeyError as e:
                    pass 

                if (incumbent is not None):
                    logging.warning("found unexpected incumbent: " + definition.device_full_id)
                    try:
                        incumbent.disconnect()
                    except Exception as e: 
                        logging.warning("unexpected exception on disposing: " + definition.device_full_id + " : " + e)
                    self.connectors.pop(definition.device_full_id)
                    
                connector:Connector = self.create_connector(definition)
                try: 
                    await connector.connect()
                    self.connectors[definition.device_full_id] = connector
                    self.publisher.publish(ConnectionDefinition(device_full_id=definition.device_full_id, owner_name=self.get_name()))
                except ConnectionError as e: 
                    logging.warning("connection failed: " + connector.device_definition.device_full_id + " : " + e.msg)            
        

    def handle_removals(self, definitions:list[DeviceDefinition]):
        for definition in definitions:
            incumbent: Connector = self.connectors[definition.device_full_id]
            if (incumbent is not None):
                try:
                    incumbent.disconnect()
                except Exception as e: 
                    logging.warning("unexpected exception on disposing: " + definition.device_full_id + " : " + e)
                self.connectors.pop(definition.device_full_id)

    async def process_scans(self):
        if(self.processing_scans == False):
            self.processing_scans = True
            while (len(self.scan_queue) > 0):
                scan:DeviceScan = self.scan_queue[0]
                self.scan_queue.pop(0)
                await self.handle_additions(scan.additions)
                self.handle_removals(scan.removals)
            self.processing_scans = False
                

    def on_device_scan(self, scan:DeviceScan, filter:str):
        # process
        if(filter is None):
            # notification is a broadcast - this is done when devices are added or removed
            # only process this when we have completed first update after registration.
            if(self.has_scanned_after_registration == True):
                self.scan_queue.append(scan)
                run(self.process_scans)
        else:
            myname = self.get_name()
            if(filter == myname):
                if(self.has_scanned_after_registration == False):
                    # notification is especially for us. 
                    # only handle once, when we have just registered.
                    # in this special case we want to process the entire list, not the additions
                    scan.additions = scan.list
                    self.scan_queue.append(scan)
                    self.has_scanned_after_registration = True
                    run(self.process_scans)
                    
                    

            
            
        
            
            

                

