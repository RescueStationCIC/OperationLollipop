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
            
     
    async def disconnect(self):
        if(self.connection is None):
            self.cancel_requested = True
        else:
            try:
                self.connection.device.reset()
            except usb.core.USBError as e:
                logging.warning("exception, trying to close: " + self.connection.device_definition.system_id + " : " + e)
            
            try:
                usb.util.dispose_resources(self.connection.device)
            except usb.core.USBError as e: 
                logging.warning("exception on disposing: " + self.connection.device_definition.system_id + " : " + e)
            
            self.connection = None
            


class ConnectorManager:
    
    def __init__(self):
        self.connectors:dict={}
        self.scan_queue:list[DeviceScan]=[]
        self.processing_scans:bool = False
        self.publisher:ConnectionPublisher = ConnectionPublisher('connection manager')
        self.connectionHandler = ConnectionHandler(self.on_new_connection)
        self.current_connection_attempt:Connector = None 

    def createConnector(self, device_definition:DeviceDefinition) -> Connector:
        raise NotImplementedError
    

    def on_new_connection(self,system_id):
        if(self.current_connection_attempt is not None):
            if(self.current_connection_attempt.connection.device_definition.system_id == system_id):
                # someone bagged this already!
                self.current_connection_attempt.disconnect()
        

    async def handle_additions(self,scan:DeviceScan):
        definitions:list[DeviceDefinition] = scan.additions
        if(self.connectors.len == 0):
            # we've probably just started. Process everything
           definitions = scan.list
        for definition in definitions:
            # safety: check to see if we have an incumbent. It will need removing
            incumbent: Connector = self.connectors[definition.system_id]
            if (incumbent is not None):
                logging.warning("found unexpected incumbent: " + definition.system_id)
                try:
                    incumbent.disconnect()
                except Exception as e: 
                    logging.warning("unexpected exception on disposing: " + definition.system_id + " : " + e)
                self.connectors.pop(definition.system_id)
                
            connector:Connector = self.createConnector(definition)
            try: 
                await connector.connect()
                self.connectors[definition.system_id] = connector
                self.publisher.publish(definition)
            except ConnectorError as e: 
                logging.warning("connection failed: " + self.connection.device_definition.system_id + " : " + e)            
        

    async def handle_removals(self, scan:DeviceScan):
        definitions:list[DeviceDefinition] = scan.list
        if(self.connectors.len > 0):
            logging.warning("connectors are empty, but " + definitions.count + "have been removed. Has the service just started?")
        else:     
            for definition in definitions:
                incumbent: Connector = self.connectors[definition.system_id]
                if (incumbent is not None):
                    try:
                        incumbent.disconnect()
                    except Exception as e: 
                        logging.warning("unexpected exception on disposing: " + definition.system_id + " : " + e)
                    self.connectors.pop(definition.system_id)

    async def processScans(self):
        self.processing_scans = True
        while (self.scan_queue.len > 0):
            scan:DeviceScan = self.scan_queue[0]
            self.scan_queue.remove[0]
            await self.handle_additions(scan)
            await self.handle_removals(scan)
                

    def receive_device_scan(self, scan:DeviceScan):
        self.scanQueue.append(scan)
        if (self.processingScans == False):
            run(self.processScans)

