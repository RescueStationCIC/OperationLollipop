import time
import daemon


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from trio import run
from pynng import Pub0, Timeout
from .config import Config

from common.definitions import Definitions

class FileCreateHandler(FileSystemEventHandler):
    
    def __init__(self, publisher):
        FileSystemEventHandler.__init__(self)
        self.publisher = publisher
        self.topic = Definitions.instance().definition('TOPIC_CONFIG')
        self.encoding = Definitions.instance().definition('TRANSFER_ENCODING')
    
    def on_modified(self, event):
        msg = self.topic + ': ' + Config.read().data()
        self.publisher.send(msg.encode(self.encoding))
        


async def begin_config_listeners():
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

    # try:
    #     while file_observer.is_alive():
    #         file_observer.join(1)
    # finally:
    #     file_observer.stop()
    #     file_observer.join()



# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon
def start():
    run(begin_config_listeners)

    
    

    

    
    
 