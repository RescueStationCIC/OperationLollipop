from common.messagehandler import MessageHandler
from common.definitions import Definitions

class ConfigurationHandler(MessageHandler):
    
    def on_new_data(self, object):
        self.on_new_config(object)
    
    def __init__(self, on_new_config):
        MessageHandler.__init__(self, Definitions.TOPIC_CONFIG)
        self.on_new_config = on_new_config