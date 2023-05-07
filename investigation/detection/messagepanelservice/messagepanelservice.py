import time
import logging
from trio import run
from common.definitions import Definitions
from common.error import ConnectorError
from common.configurationhandler import ConfigurationHandler
from investigation.detection.common.devicescanhandler import DeviceScanHandler
from common.publisher import RegistrationPublisher
from common.device import DeviceScan
from common.device import DeviceDefinition
from common.connector import Connector
from common.connector import ConnectorManager
from messagepanel import MessagePanelManager
                
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon





    
def setup():
    
    
    #
    # configuration service changes
    #
    
    def on_new_config(config):
        print('messagepanelservice sees new config')
        
    manager = MessagePanelManager();     
        
    # listener for configuration updates
    config_handler = ConfigurationHandler( on_new_config)
    run(config_handler.start)
    
    # listener for device list updates
    devicescan_handler = DeviceScanHandler( manager.receive_device_scan )
    run(devicescan_handler.start)    
    
    # tell everyone (but mostly the configuration service) we're alive
    RegistrationPublisher(Definitions.SERVICENAME_MESSAGEPANEL).prepare().publish()
    
    print('messagepanelservice setup complete')
        

def start():
    setup()
   
    
    
    
 