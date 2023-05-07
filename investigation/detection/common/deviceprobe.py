
import usb
import logging
from enum import Enum
from common.device import DeviceDefinition

# device probe
# base class which encapsulates claiming a USB device and probing its capabilities
# call start() to kick off the process
# subclasses will provide the probe functionality which calls on_probe_success if the class recognises the device, or on_probe_fail if it does not
# this allows for asynchronous comms with the device.


class DeviceEndpoints: 
    def __init__(self, e_in:usb.Endpoint, e_out:usb.Endpoint ):
        self.e_in:usb.Endpoint = e_in
        self.e_out:usb.Endpoint = e_out
        
class ConnectedDevice:
    def __init__(self, device_definition:DeviceDefinition):
        self.device_definition: DeviceDefinition = device_definition
        self.device: usb.Device = None
        self.interface: usb.Interface = None
        self.claimed: bool = False
        self.endpoints: DeviceEndpoints = DeviceEndpoints()

        
class ProbeError(Exception):
    class Definition(Enum):
        NO_ERROR=0
        NOT_IMPLEMENTED=1
        NO_DEVICE_FOR_DEFINITION=2
        DEVICE_CLASS_NOT_RECOGNISED=3
        NO_INTERFACE_FOR_DEVICE=4
        INTERFACE_CLAIM_FAILED=5
        
    def __init__(self, device_definition:DeviceDefinition, error_definition:Definition, msg:str=""):
        self.device_definition:DeviceDefinition = device_definition
        self.error_definition:ProbeError.Definition = error_definition
        self.msg:str = msg
        super().__init__(self.msg)
      
class DeviceProbe:

    def __init__(self):
        pass
    
    
    def isDeviceClassRecognised(self,device:usb.Device) -> bool:
        raise ProbeError(device, ProbeError.Definition.NOT_IMPLEMENTED, "isDeviceClassRecognised")

    def getInterface (self,device:usb.Device) -> usb.Interface: 
        raise ProbeError(device, ProbeError.Definition.NOT_IMPLEMENTED, "getInterface")
    
    def getEndpoints( self, device:usb.Device, interface:usb.Interface) -> DeviceEndpoints:
        raise ProbeError(device, ProbeError.Definition.NOT_IMPLEMENTED,"getEndpoints") 
    
    async def probeInterface(self,device:ConnectedDevice)-> ConnectedDevice:
        raise ProbeError(device, ProbeError.Definition.NOT_IMPLEMENTED, "probeInterface")
    
    
    async def connectIfRecognised(self, device_definition:DeviceDefinition) -> ConnectedDevice:
        result:ConnectedDevice(device_definition)
       
        result.device = usb.core.find(id=device_definition.id, bus=device_definition.bus, device=device_definition.device)
        if(result.device is None):
            raise ProbeError(result, ProbeError.Definition.NO_DEVICE_FOR_DEFINITION)
        else: 
            
            if(self.isDeviceClassRecognised(result.device)):
                result.interface = self.getInterface(result.device)
                if(result.interface is None):
                    raise ProbeError(result, ProbeError.Definition.NO_INTERFACE_FOR_DEVICE)
                else:
                    try:
                        usb.util.claim_interface(result.device, result.interface)
                        result.claimed = True
                    except:
                        raise ProbeError(result, ProbeError.Definition.INTERFACE_CLAIM_FAILED)
                    try:
                        result.endpoints = await self.getEndpoints(result)
                        result = await self.probeInterface(result)
                    except ProbeError:
                        usb.util.release_interface(result.device, result.interface)
                        result.claimed = False
                        raise
        return result
            
        
        
        
        
    
        
        