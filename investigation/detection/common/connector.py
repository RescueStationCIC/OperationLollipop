import usb
import time
import random
import logging
from trio import run
from common.definitions import Definitions
from common.deviceprobe import ConnectorError
from common.deviceprobe import DeviceProbe
from common.deviceprobe import ConnectedDevice
from common.connectionpublisher import ConnectionPublisher
from common.connectionhandler import ConnectionHandler
from common.device import DeviceDefinition
from common.device import DeviceScan


class ConnectionDefinition:
    def __init__(self, device_full_id:str, owner_name:str):
        self.owner_name:str = owner_name
        self.device_full_id:str = device_full_id

class Connector():

    def __init__(self, device_definition:DeviceDefinition):
        self.device_probe = self.getProbe(device_definition)
        self.connection:ConnectedDevice = None
        self.cancel_requested = False
            
    def getProbe(self,device_definition:DeviceDefinition) -> DeviceProbe:
        raise NotImplementedError    
    
    async def connect(self):
        backoff_max:int = Definitions.CONNECTION_BACKOFF_PERIOD_MAX_MS
        backoff_min:int = Definitions.CONNECTION_BACKOFF_PERIOD_MIN_MS
        if(self.connection is not None):
            raise Exception("already connected.")
        
        while((self.connection is None) and (self.cancel_requested == False)):
            try:
                self.connection = await self.device_probe(self.device_definition)
            except ConnectorError as e:
                if(e.error_definition == ConnectorError.Definition.INTERFACE_CLAIM_FAILED):
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
        self.processing_scans:bool = False
        self.cancel_current_scan:bool = False
        self.publisher:ConnectionPublisher = ConnectionPublisher(self.getName())
        self.connectionHandler = ConnectionHandler(self.on_new_connection)
        self.current_connection_attempt:Connector = None 

    def createConnector(self, device_definition:DeviceDefinition) -> Connector:
        raise NotImplementedError
    
    def getName(self) -> str:
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
                incumbent: Connector = self.connectors[definition.device_full_id]
                if (incumbent is not None):
                    logging.warning("found unexpected incumbent: " + definition.device_full_id)
                    try:
                        incumbent.disconnect()
                    except Exception as e: 
                        logging.warning("unexpected exception on disposing: " + definition.device_full_id + " : " + e)
                    self.connectors.pop(definition.device_full_id)
                    
                connector:Connector = self.createConnector(definition)
                try: 
                    await connector.connect()
                    self.connectors[definition.device_full_id] = connector
                    self.publisher.publish(ConnectionDefinition(device_full_id=definition.device_full_id, owner_name=self.getName()))
                except ConnectorError as e: 
                    logging.warning("connection failed: " + self.connection.device_definition.device_full_id + " : " + e)            
        

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
            while (self.scan_queue.len > 0):
                scan:DeviceScan = self.scan_queue[0]
                self.scan_queue.remove[0]
                await self.handle_additions(scan.additions)
                self.handle_removals(scan.removals)
            self.processing_scans = False
                

    def receive_device_scan(self, scan:DeviceScan, filter):
        # process
        if(filter is None):
            # notification is a broadcast - this is done when devices are added or removed
            # only process this when we have completed first update after registration.
            if(self.registration_scan_complete == True):
                self.scanQueue.append(scan)
                run(self.process_scans)
        else:
            if(filter == self.getName()):
                if(self.registration_scan_complete == False):
                    # notification is especially for us. 
                    # only handle once, when we have just registered.
                    self.handle_additions(scan.list)
                    self.registration_scan_complete = True
                    

            
            
        
            
            

                

