from common.messagehandler import MessageHandler
from common.definitions import Definitions

          
class DeviceScanHandler(MessageHandler):
        
    def on_new_data(self,object, filter ):
        self.on_devicelist_update(object, filter)
     
    def __init__(self, on_devicescan_update):
        MessageHandler.__init__(self, Definitions.TOPIC_DEVICESCAN)
        self.on_devicescan_update = on_devicescan_update