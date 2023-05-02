import json
from trio import run
from pynng import Sub0, Timeout
from common.definitions import Definitions
                



class MessageHandler:

    def __init__(self,topic_name):
        self.topic_name = topic_name 
        self.encoding = Definitions.instance().definition('TRANSFER_ENCODING')
        self.address = Definitions.instance().definition('PUBSUB_ADDRESS')
        self.timeout = Definitions.instance().definition('RECEIVER_TIMEOUT_MS')
        self.topic_tag = self.topic_name + ': '
        self.topic_tag_bytes:bytes = topic_name.encode(self.encoding)
        self.stopped=False
        self.subscriber = Sub0(
            dial = self.address,
            recv_timeout=self.timeout)
        self.subscriber.subscribe(self.topic_tag_bytes)
    
    def on_new_data(self, object):
        print (object)  
    
    def stop (self):
        self.stopped = True 
        
    async def start(self):
        while (self.stopped == False):
            try:
                msg = await self.subscriber.arecv_msg()
                raw = msg.bytes
                data = raw.decode(self.encoding).partition(self.topic_tag)[2]
                object = json.loads(data)
                self.on_new_data(object)
            except:
                pass # todo: log this eventually
            
            
            
class ConfigurationHandler(MessageHandler):
    
    def on_new_data(self, object):
        self.on_new_config(object)
    
    def __init__(self, topic_name, on_new_config):
        MessageHandler.__init__(self, topic_name)
        self.on_new_config = on_new_config

class RegistrationHandler(MessageHandler):
    
    def on_new_data(self,object):
        self.on_new_registration(object)
     
    def __init__(self, on_new_registration):
        MessageHandler.__init__(self, Definitions.instance().definition('TOPIC_REGISTRATION'))
        self.on_new_registration = on_new_registration