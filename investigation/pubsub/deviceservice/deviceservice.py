import time
import daemon
import json

from trio import run
from common.definitions import Definitions
from common.messagehandler import ConfigurationHandler
from common.publisher import RegistrationPublisher

                
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon


def on_new_config(config):
    print ('new config, sir!')
    
    
    
def setup():
    # listener for configuration updates
    config_handler = ConfigurationHandler(Definitions.instance().definition('TOPIC_CONFIG'), on_new_config)
    run(config_handler.start)
    
    # tell everyone (but mostly the configuration service) we're alive
    RegistrationPublisher(Definitions.instance().definition('SERVICENAME_DEVICE')).prepare().publish()
        

def start():
    setup()
   
    
    
    
 