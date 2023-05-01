import time
import daemon
import importlib

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pynng import Pub0, Timeout

from .config import Config
from common.definitions import Definitions

class FileCreateHandler(FileSystemEventHandler):
    
    def __init__(self, publisher):
        FileSystemEventHandler.__init__(self)
        self.publisher = publisher
    
    def on_modified(self, event):
        self.publisher.send(Config.read().data().encode())
        
        
        
        
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon
def start_config():
    

    
    # holds variable config changes reported over Publish and Subscribe
    Config.create('./config.json')
    
    
    # create config publisher

    publisher = Pub0(listen=Definitions.instance().definition('PUBSUB_ADDRESS'))
    
    
    event_handler = FileCreateHandler(publisher)

    # Create an file_observer.
    file_observer = Observer()

    # Attach the file_observer to the event handler.
    file_observer.schedule(event_handler, Config.path())

    # Start the file_observer.
    file_observer.start()

    try:
        while file_observer.is_alive():
            file_observer.join(1)
    finally:
        file_observer.stop()
        file_observer.join()
    
    
 