from common.messagehandler import MessageHandler
from common.definitions import Definitions

          


class DeviceListHandler(MessageHandler):
        
    def on_new_data(self,object):
        self.on_devicelist_update(object)
     
    def __init__(self, on_devicelist_update):
        MessageHandler.__init__(self, Definitions.TOPIC_DEVICELIST)
        self.on_devicelist_update = on_devicelist_update