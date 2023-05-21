import jsonpickle
import time
import uuid
import paho.mqtt.client as mqtt
from common.error import GeneralError
from common.definitions import Definitions
from common.pubsubmessagedefinition import PubSubMessageDefinition


class Publisher:
    def __init__(self, topic:str):
        print ('PUB: init: ' + topic)
        self.topic = topic        
        self.publisher = mqtt.Client(client_id=str(uuid.uuid4()))
        self.encoding = Definitions.TRANSFER_ENCODING
        self.address = Definitions.PUBSUB_ADDRESS
        self.port = Definitions.PUBSUB_PORT
        self.keepalive = Definitions.PUBSUB_KEEPALIVE
        self.publisher_id = None
    
    
    def on_connect(self, client, userdata, flags, rc):
        self.publisher_id = client    
    
    def on_publish(self, client, userdata, result):
        pass
        
    def prepare(self):  
     
        self.publisher.on_connect = self.on_connect  
        self.publisher.on_publish = self.on_publish 
        self.publisher.connect(self.address, self.port, self.keepalive)
        self.publisher.loop_start()
        while(self.publisher_id is None):
            time.sleep(1)
        
        return self
        
    def publish(self,data, filter:str):
        message_definition=PubSubMessageDefinition(data, filter)
        msg = jsonpickle.encode(message_definition) #.encode(self.encoding)
        self.publisher.publish(self.topic, payload=msg, qos=0, retain=False)
    
        
    

            