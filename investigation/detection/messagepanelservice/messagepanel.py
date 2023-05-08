import usb
import time
import logging
from common.definitions import Definitions
from common.device import DeviceDefinition
from common.device import DeviceScan
from common.deviceprobe import DeviceProbe
from common.deviceprobe import ConnectorError
from common.connector import Connector
from common.connector import ConnectorManager

from investigation.detection.common.deviceprobe import ConnectedDevice, DeviceEndpoints, DeviceProbe


# Example output from lsusb -v:
# Bus 001 Device 005: ID 239a:0001 Adafruit CDC Bootloader
# Device Descriptor:
#   bLength                18
#   bDescriptorType         1
#   bcdUSB               1.01
#   bDeviceClass            2 Communications
#   bDeviceSubClass         0 
#   bDeviceProtocol         0 
#   bMaxPacketSize0        32
#   idVendor           0x239a Adafruit
#   idProduct          0x0001 CDC Bootloader
#   bcdDevice            1.00
#   iManufacturer           0 
#   iProduct                1 Adafruit Industries
#   iSerial                 0 
#   bNumConfigurations      1
#   Configuration Descriptor:
#     bLength                 9
#     bDescriptorType         2
#     wTotalLength       0x0043
#     bNumInterfaces          2
#     bConfigurationValue     1
#     iConfiguration          0 
#     bmAttributes         0xc0
#       Self Powered
#     MaxPower              100mA
#     Interface Descriptor:
#       bLength                 9
#       bDescriptorType         4
#       bInterfaceNumber        0
#       bAlternateSetting       0
#       bNumEndpoints           1
#       bInterfaceClass         2 Communications
#       bInterfaceSubClass      2 Abstract (modem)
#       bInterfaceProtocol      1 AT-commands (v.25ter)
#       iInterface              0 
#       CDC Header:
#         bcdCDC               1.10
#       CDC Call Management:
#         bmCapabilities       0x00
#         bDataInterface          1
#       CDC ACM:
#         bmCapabilities       0x06
#           sends break
#           line coding and serial state
#       CDC Union:
#         bMasterInterface        0
#         bSlaveInterface         1 
#       Endpoint Descriptor:
#         bLength                 7
#         bDescriptorType         5
#         bEndpointAddress     0x82  EP 2 IN
#         bmAttributes            3
#           Transfer Type            Interrupt
#           Synch Type               None
#           Usage Type               Data
#         wMaxPacketSize     0x0008  1x 8 bytes
#         bInterval              64
#     Interface Descriptor:
#       bLength                 9
#       bDescriptorType         4
#       bInterfaceNumber        1
#       bAlternateSetting       0
#       bNumEndpoints           2
#       bInterfaceClass        10 CDC Data
#       bInterfaceSubClass      0 
#       bInterfaceProtocol      0 
#       iInterface              0 
#       Endpoint Descriptor:
#         bLength                 7
#         bDescriptorType         5
#         bEndpointAddress     0x03  EP 3 OUT
#         bmAttributes            2
#           Transfer Type            Bulk
#           Synch Type               None
#           Usage Type               Data
#         wMaxPacketSize     0x0020  1x 32 bytes
#         bInterval               0
#       Endpoint Descriptor:
#         bLength                 7
#         bDescriptorType         5
#         bEndpointAddress     0x84  EP 4 IN
#         bmAttributes            2
#           Transfer Type            Bulk
#           Synch Type               None
#           Usage Type               Data
#         wMaxPacketSize     0x0020  1x 32 bytes
#         bInterval               0
# can't get debug descriptor: Resource temporarily unavailable
# Device Status:     0x0000
#   (Bus Powered)



class MessagePanelDeviceProbe(DeviceProbe):
    def __init__(self,device_definition:DeviceDefinition): 
        super().__init__(self)
        
    def isDeviceTypeRecognised(full_device):
        # check device class:
        #   bDeviceClass            2 Communications
        # check interfaces for:
        #       bInterfaceClass         2 Communications
        #       bInterfaceSubClass      2 Abstract (modem)
        #       bInterfaceProtocol      1 AT-commands (v.25ter)
        
        return full_device.deviceClass == Definitions.USB_DEVICE_CLASS_COMMS 

    def getInterface(full_device:usb.Device)-> usb.Interface:
        result = None
        for c in full_device.configurations:
            configuration:usb.Configuration = c
            for i in configuration.interfaces:
                interface:usb.Interface = i
                if((interface.interfaceClass == Definitions.USB_INTERFACE_CLASS_COMMS) and
                  (interface.interfaceSubClass == Definitions.USB_INTERFACE_SUBCLASS_MODEM) and
                  (interface.interfaceProtocol == Definitions.USB_INTERFACE_PROTOCOL_AT)):
                    result = interface
                    break
        return result 
    
    def getEndpoints(self, device: usb.Device, interface: usb.Interface) -> DeviceEndpoints:
        result:DeviceEndpoints = DeviceEndpoints()
        
        result.e_in = usb.util.find_descriptor(
                    interface,
                    custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
        result.e_out = usb.util.find_descriptor(
                    interface,
                    custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        
        return result    
        
    
    async def probeInterface(self, device: ConnectedDevice) -> ConnectedDevice:
        device.endpoints.e_out.write('test')
        time.sleep(1)
        return device
        
            

class MessagePanelConnector(Connector):
    def __init__(self, device_definition:DeviceDefinition):
        super().__init__(self, device_definition)
        
    def getProbe(self, device_definition: DeviceDefinition) -> DeviceProbe:
        return MessagePanelDeviceProbe(self.device_definition)


class MessagePanelManager (ConnectorManager): 
    def __init__(self, device_definition:DeviceDefinition):
        super().__init__(self, device_definition)
    
    def getName(self): 
        return 'message_panel_manager' 
    
    def createConnector(self, device_definition:DeviceDefinition) -> Connector:
        return MessagePanelConnector(device_definition)

            
    
        
        
        
                       

        
        
        

        
    

        