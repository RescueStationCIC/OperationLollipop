from common.messagehandler import MessageHandler
from common.definitions import Definitions

class ConnectionHandler(MessageHandler):
    
    def on_new_data(self,object):
        self.on_new_connection(object)
     
    def __init__(self, on_new_connection):
        MessageHandler.__init__(self, Definitions.TOPIC_CONNECTION)
        self.on_new_connection = on_new_connection
        