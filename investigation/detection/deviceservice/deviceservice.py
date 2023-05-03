import time
import daemon
import json

from trio import run
from common.definitions import Definitions
from common.messagehandler import ConfigurationHandler
from common.publisher import Publisher
from common.publisher import RegistrationPublisher

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .devicelist import DeviceList
                
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
    DeviceList.create(Definitions.instance().definition('PATH_DEVICES'))
    
    
    # reads and publishes the current device list
    def publish_devices(reason: str):
        print (reason)
        devicelist_publisher.publish(DeviceList.read().data())
    
    # the PUB SUB publisher of the device list
    devicelist_publisher = Publisher(Definitions.instance().definition('TOPIC_DEVICELIST'))
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
    RegistrationPublisher(Definitions.instance().definition('SERVICENAME_DEVICE')).prepare().publish()
    
    print('deviceservice setup complete')
        

def start():
    setup()
   
    
    
    
 