import uuid
import json

import paho.mqtt.client as mqtt
from common.definitions import Definitions
          
class MessageHandler:

    def __init__(self,topic_name):
        print ('SUB: init: ' + topic_name)
        self.topic_name = topic_name 
        self.encoding = Definitions.TRANSFER_ENCODING
        self.address = Definitions.PUBSUB_ADDRESS
        self.port = Definitions.PUBSUB_PORT
        self.keepalive = Definitions.PUBSUB_KEEPALIVE
        self.timeout = Definitions.RECEIVER_TIMEOUT_MS
        self.subscriber = mqtt.Client(str(uuid.uuid4()))
        self.subscriber_id = None
        self.subscribed = None
        self.connected = False
    
    async def start(self):

        self.subscriber.on_subscribe = self.on_subscribe        
        self.subscriber.on_message =  self.on_message
        self.subscriber.on_connect = self.on_connect 
        self.subscriber.on_disconnect = self.on_disconnect  
        self.subscriber.connect(self.address, self.port, self.keepalive)#, on_connect)
        self.subscriber.loop_start()


    
    def on_connect(self, client, userdata, flags, rc):
        self.connected = True
        self.subscriber_id = client
        self.subscriber.subscribe(self.topic_name,2)   
 
    def on_disconnect(self,client, userdata,  rc):
        self.connected = False
        print('WARNING: Disconnected.')
        
    def on_subscribe (self,client, userdata, mid, granted_qos):
        self.subscribed = True

        
    def on_message(self, client, userdata, message,tmp=None):
    
        object = json.loads(message.payload.decode(self.encoding))
        self.on_new_data(object)
        
    def on_new_data(self, object):
        print (object)  
            



        
