from common.publisher import Publisher
from common.definitions import Definitions

class RegistrationPublisher(Publisher):
    def __init__(self, name:str):
        Publisher.__init__(self, Definitions.TOPIC_REGISTRATION)
        self.name = name
        
    def publish(self):
        Publisher.publish(self,{'name':self.name})
    