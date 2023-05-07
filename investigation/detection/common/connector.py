import usb
import time
import random
import logging
from common.device import DeviceDefinition
from common.deviceprobe import DeviceProbe

from common.deviceprobe import ProbeError

from common.definitions import Definitions
from common.deviceprobe import ConnectedDevice



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
            except ProbeError as e:
                if(e.error_definition == ProbeError.Definition.INTERFACE_CLAIM_FAILED):
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
                logging.warning("exception, trying to close: " + self.connection.device_definition.id + " : " + e)
            
            usb.util.dispose_resources(self.connection.device)
            self.connection = None
            


class Connectors:
    def __init__(self):
        self.connectors:list[Connector] = None

