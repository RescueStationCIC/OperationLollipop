import time
import daemon
import json

from trio import run
from pynng import Sub0, Timeout
from common.definitions import Definitions
from common.messagehandler import MessageHandler

class ConfigHandler(MessageHandler):
    
    def on_new_data(self, object):
        self.on_new_config(object)
    
    def __init__(self, topic_name, on_new_config):
        MessageHandler.__init__(self, topic_name)
        self.on_new_config = on_new_config
            
        
                
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon


def on_new_config(config):
    print ('new config, sir!')

def start():
    config_handler = ConfigHandler(Definitions.instance().definition('TOPIC_CONFIG'), on_new_config)
    run (config_handler.start)
    
    
 