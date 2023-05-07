import time
from trio import run
from common.definitions import Definitions
from common.configurationhandler import ConfigurationHandler
from common.devicelisthandler import DeviceListHandler
from common.publisher import RegistrationPublisher
from common.connector import Connector
                
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon





    
def setup():
    
    
    #
    # configuration service changes
    #
    
    def on_new_config(config):
        print('messagepanelservice sees new config')
        
    async def some_async_func():
        time.sleep(10)
            
        
    def on_devicelist_update(devicelist):
        print('messagepanelservice sees new devices')
        
    # listener for configuration updates
    config_handler = ConfigurationHandler( on_new_config)
    run(config_handler.start)
    
    # listener for device list updates
    devicelist_handler = DeviceListHandler( on_devicelist_update)
    run(devicelist_handler.start)    
    
    # tell everyone (but mostly the configuration service) we're alive
    RegistrationPublisher(Definitions.SERVICENAME_MESSAGEPANEL).prepare().publish()
    
    print('messagepanelservice setup complete')
        

def start():
    setup()
   
    
    
    
 