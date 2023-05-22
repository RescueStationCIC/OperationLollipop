
import usb
import logging
from enum import Enum
from common.devicedefinition import DeviceDefinition
from common.error import ConnectionError

# device probe
# base class which encapsulates claiming a USB device and probing its capabilities
# call start() to kick off the process
# subclasses will provide the probe functionality which calls on_probe_success if the class recognises the device, or on_probe_fail if it does not
# this allows for asynchronous comms with the device.


class DeviceEndpoints: 
    def __init__(self, e_in:usb.Endpoint = None, e_out:usb.Endpoint = None):
        self.e_in:usb.Endpoint = e_in
        self.e_out:usb.Endpoint = e_out
        
class ConnectedDevice:
    def __init__(self, device_definition:DeviceDefinition):
        self.device_definition: DeviceDefinition = device_definition
        self.device: usb.Device = None
        self.interface: usb.Interface = None
        self.claimed: bool = False
        self.endpoints: DeviceEndpoints = DeviceEndpoints()

        

      
class DeviceProbe:

    def __init__(self):
        pass
    
    
    def isDeviceClassRecognised(self,device:usb.Device) -> bool:
        raise ConnectionError(device, ConnectionError.Definition.NOT_IMPLEMENTED, "isDeviceClassRecognised")

    def getInterface (self,device:usb.Device) -> usb.Interface: 
        raise ConnectionError(device, ConnectionError.Definition.NOT_IMPLEMENTED, "getInterface")
    
    def getEndpoints( self, device:usb.Device, interface:usb.Interface) -> DeviceEndpoints:
        raise ConnectionError(device, ConnectionError.Definition.NOT_IMPLEMENTED,"getEndpoints") 
    
    async def probeInterface(self,device:ConnectedDevice)-> ConnectedDevice:
        raise ConnectionError(device, ConnectionError.Definition.NOT_IMPLEMENTED, "probeInterface")
    
    
    async def connectIfRecognised(self, device_definition:DeviceDefinition) -> ConnectedDevice:
        result = ConnectedDevice(device_definition)
        result.device = usb.core.find(idVendor=device_definition.id_vendor, idProduct=device_definition.id_product, bus=device_definition.bus, address=device_definition.address)
        
        if(result.device is None):
            raise ConnectionError(result, ConnectionError.Definition.NO_DEVICE_FOR_DEFINITION)
        else: 
            
            if(self.isDeviceClassRecognised(result.device)):
                result.interface = self.getInterface(result.device)
                if(result.interface is None):
                    raise ConnectionError(result, ConnectionError.Definition.NO_INTERFACE_FOR_DEVICE)
                else:
                    try:
                        usb.util.claim_interface(result.device, result.interface)
                        result.claimed = True
                    except:
                        raise ConnectionError(result, ConnectionError.Definition.INTERFACE_CLAIM_FAILED)
                    try:
                        result.endpoints = await self.getEndpoints(result)
                        result = await self.probeInterface(result)
                    except ConnectionError:
                        usb.util.release_interface(result.device, result.interface)
                        result.claimed = False
                        raise
            else:
                raise ConnectionError(result, ConnectionError.Definition.DEVICE_CLASS_NOT_RECOGNISED)
        return result
            
        
        
        
        
    
        
        