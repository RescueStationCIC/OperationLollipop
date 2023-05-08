from common.publisher import Publisher
from common.definitions import Definitions
from common.registration import RegistrationDefinition

class RegistrationPublisher(Publisher):
    def __init__(self, registration_definition: RegistrationDefinition):
        Publisher.__init__(self, Definitions.TOPIC_REGISTRATION)
        self.registration_definition: RegistrationDefinition = registration_definition
        
        
    def publish(self):
        Publisher.publish(self,self.registration_definition)
    