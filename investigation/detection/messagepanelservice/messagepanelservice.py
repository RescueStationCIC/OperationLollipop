import time
import logging
from trio import run
from common.definitions import Definitions
from common.error import ConnectionError
from common.configurationhandler import ConfigurationHandler
from common.devicescanhandler import DeviceScanHandler
from common.registrationpublisher import RegistrationPublisher
from common.registrationdefinition import RegistrationDefinition
from common.devicescan import DeviceScan
from common.devicedefinition import DeviceDefinition
from common.connector import Connector
from common.connector import ConnectorManager
from messagepanelservice.messagepanel import MessagePanelConnector
                
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon





    
def setup():
    
    

    
    

    #
    # configuration service changes
    #
    
    def on_new_config(config):
        print('messagepanelservice sees new config')
         
    # listener for configuration updates
    config_handler = ConfigurationHandler( on_new_config)
    run(config_handler.start)
    
    # looks after connections to message panels
    class MessagePanelManager (ConnectorManager):   
        def get_name(self): 
            return Definitions.SERVICENAME_MESSAGEPANEL
        
        def create_connector(self, device_definition:DeviceDefinition) -> Connector:
            return MessagePanelConnector(device_definition)
    
    manager = MessagePanelManager()
    
    # listener for device list updates
    # passes them on to manager, so it can check for addtional or removed panels
    devicescan_handler = DeviceScanHandler( manager.on_device_scan )
    run(devicescan_handler.start)    
    
    # tell everyone (but mostly the configuration service) we're alive
    RegistrationPublisher(RegistrationDefinition(Definitions.SERVICENAME_MESSAGEPANEL)).prepare().publish()
    
    print('messagepanelservice setup complete')
        

def start():
    setup()
   
    
    
    
 