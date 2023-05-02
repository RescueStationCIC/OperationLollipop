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
    
    def on_new_data(self, object):
        print (object)  
    
    def stop (self):
        self.stopped = True 
        
    async def start(self):
        self.subscriber = Sub0(
            dial = self.address,
            recv_timeout=self.timeout)
        self.subscriber.subscribe(self.topic_tag_bytes)
        while (self.stopped == False):
            msg = await self.subscriber.arecv_msg()
            raw = msg.bytes
            data = raw.decode(self.encoding).partition(self.topic_tag)[2]
            object = json.loads(data)
            self.on_new_data(object)
