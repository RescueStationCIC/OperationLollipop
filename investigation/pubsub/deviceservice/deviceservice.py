import time
import daemon
import json

from trio import run
from pynng import Sub0, Timeout
from common.definitions import Definitions
from common.messagehandler import ConfigurationHandler
from common.publisher import RegistrationPublisher

                
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon


def on_new_config(config):
    print ('new config, sir!')
    
    
    
async def setup():
    # listener for configuration updates
    config_handler = ConfigurationHandler(Definitions.instance().definition('TOPIC_CONFIG'), on_new_config)
    config_handler.start
    # tell everyone (but mostly the configuration service) we're alive
    RegistrationPublisher(Definitions.instance().definition('SERVICENAME_DEVICE')).publish()
        

def start():
    run (setup)
   
    
    
    
 