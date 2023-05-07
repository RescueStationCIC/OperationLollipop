from common.messagehandler import MessageHandler
from common.definitions import Definitions

class RegistrationHandler(MessageHandler):
    
    def on_new_data(self,object):
        self.on_new_registration(object)
     
    def __init__(self, on_new_registration):
        MessageHandler.__init__(self, Definitions.TOPIC_REGISTRATION)
        self.on_new_registration = on_new_registration
        