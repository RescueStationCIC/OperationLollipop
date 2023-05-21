from common.messagehandler import MessageHandler
from common.definitions import Definitions
from common.registrationdefinition import RegistrationDefinition
class RegistrationHandler(MessageHandler):
    
    def on_new_data(self, object:RegistrationDefinition, filter):
        self.on_new_registration(object)
     
    def __init__(self, on_new_registration):
        MessageHandler.__init__(self, Definitions.TOPIC_REGISTRATION)
        self.on_new_registration = on_new_registration
        