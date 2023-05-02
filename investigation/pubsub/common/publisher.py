import json
from trio import run
from pynng import Pub0
from common.definitions import Definitions

class Publisher:
    def __init__(self, topic:str):
        self.topic = topic
        self.publisher = Pub0(listen=Definitions.instance().definition('PUBSUB_ADDRESS'))
        self.encoding = Definitions.instance().definition('TRANSFER_ENCODING')
        
    def publish(self,object):
        msg = (self.topic + ': ' + json.dumps(object)).encode(self.encoding)
        self.publisher.send(msg)
    
        
    
class RegistrationPublisher(Publisher):
    def __init__(self, name:str):
        Publisher.__init__(self, Definitions.instance().definition('TOPIC_REGISTRATION'))
        self.name = name
        
    def publish(self):
        Publisher.publish({'name':self.name})
    
            