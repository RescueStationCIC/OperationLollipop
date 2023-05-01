import time
import daemon
from .config import Config
from ..common import Common
from watchdog.observers import file_observer
from watchdog.events import FileSystemEventHandler
from pynng import Pub0, Timeout





class FileCreateHandler(FileSystemEventHandler):
    
    def __init__(self, publisher):
        FileSystemEventHandler.__init__()
        self.publisher = publisher
    
    def on_modified(self, event):
        self.publisher.send(Config.read().data())
        
        
        
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon
if ( 1==1):
    
    # holds immutable variables: access to all
    Common.create()
    
    # holds variable config changes reported over Publish and Subscribe
    Config.create('./config.json')
    
    
    # create config publisher
    publisher = Pub0(listen=Common.definitions().PUBSUB_ADDRESS)
    
    
    event_handler = FileCreateHandler(publisher)

    # Create an file_observer.
    file_observer = file_observer()

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
    
    
 