from trio import run
from common.definitions import Definitions
from common.configurationhandler import ConfigurationHandler
from common.publisher import Publisher
from common.publisher import RegistrationPublisher

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from deviceservice.devicelist import DeviceList
 
# deviceservice is central point for:
# * recording connected USB hardware: system_id (bus:device:product:vendor)
# * recording the association of the hardware with a service
#
# when USB hardware is connected, services are notified on the DEVICESCAN channel
# when services come up or are removed, devicemanageer is notified on the REGISTER channel
# services may have multiple device connections, since USB is not limited to the number of deviced which can be connected
# servicees may choose not to accept multiple devices, in which case, they will not connect.
# services identify a device by a number of methods, including interrogation 
# while a service interrogates a device, it is connected exclusively. Other services must wait.
# If a service discovers a device is compatible, it broadcasts on the CONNECTION channel
# the deviceservice listens on the CONNECTION channel. 
# On getting a connection event, the deviceservice updates the status of the device with the name of the service with which is connected
# it then broadcasts on the DEVICESCAN channel
# services listen on the CONNECTION channel, while they wait for exclusive access to a device. 
# if a waiting service sees a connection event for the device they are waiting for, they will stop waiting.

# The device service sends device status data on the DEVICESCAN channel:
# on REGISTER, with a message exclusive to the service registering.
# on hardware device detection, broadcasting to all services
# on CONNECTION of a service with a device.

 
                
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon


class DeviceListChangeHandler(FileSystemEventHandler):
    
    def __init__(self, on_device_list_modified):
        FileSystemEventHandler.__init__(self)
        self.on_device_list_modified = on_device_list_modified

    
    def on_modified(self, event):
        
        if (event.key[2] == True):
           self.on_device_list_modified("device list modified")

    
def setup():
    
    #
    # changes to connected devices
    #
    
    

    # reads and holds the current device list
    DeviceList.create(Definitions.PATH_DEVICES)
    
    
    # reads and publishes the current device list
    def publish_devices(reason: str):
        print (reason)
        devicelist_publisher.publish(DeviceList.read().data())
    
    # the PUB SUB publisher of the device list
    devicelist_publisher = Publisher(Definitions.TOPIC_DEVICESCAN)
    devicelist_publisher.prepare()
    
    
    # monitors changes to subsets of /dev, 
    file_observer = Observer()

    # handles item changes to the directory, and calls publish_devices
    event_handler = DeviceListChangeHandler(publish_devices)
    
    
    # event handler attached to the file_observer
    file_observer.schedule(event_handler, DeviceList.path(),recursive=True)

    # Start the file_observer.
    file_observer.start()
    
    
    #
    # configuration service changes
    #
    
    def on_new_config(config):
        publish_devices('devices published on new config')
        
    
    
    # listener for configuration updates
    config_handler = ConfigurationHandler(on_new_config)
    run(config_handler.start)
    
    # tell everyone (but mostly the configuration service) we're alive
    RegistrationPublisher(Definitions.SERVICENAME_DEVICE).prepare().publish()
    
    print('deviceservice setup complete')
        

def start():
    setup()
   
    
    
    
 