import time
import daemon


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from trio import run
from .config import Config

from common.definitions import Definitions
from common.publisher import Publisher
from common.registrationhandler import RegistrationHandler

class ConfigChangeHandler(FileSystemEventHandler):
    
    def __init__(self, on_config_modified):
        FileSystemEventHandler.__init__(self)
        self.on_config_modified = on_config_modified

    
    def on_modified(self, event):
        if (event.key[2] == True):
           self.on_config_modified("configuration change")
            

def setup():
    # holds variable config changes reported over Publish and Subscribe
    Config.create(Definitions.PATH_CONFIG)
    
    def publish_config(reason: str):
        print (reason)
        publisher.publish(Config.read().data())

    def on_new_registration(object:dict):
        publish_config("regsitration: " + object['name'])
        
    
    # create config publisher
    publisher = Publisher(Definitions.TOPIC_CONFIG)
    
    publisher.prepare()
    
    event_handler = ConfigChangeHandler(publish_config)
    registration_handler = RegistrationHandler(on_new_registration)

    # Create the file_observer.
    file_observer = Observer()

    # Attach the file_observer to the event handler.
    file_observer.schedule(event_handler, Config.path())

    # Start the file_observer.
    file_observer.start()
    
    # Start the registration handler
    run(registration_handler.start)
    
    print ('configservice setup complete')
    



# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon
def start():
    setup()
    

    
    

    

    
    
 