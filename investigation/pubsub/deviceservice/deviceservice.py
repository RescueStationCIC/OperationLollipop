import time
import daemon
import json

from trio import run
from pynng import Sub0, Timeout
from common.definitions import Definitions
                
# uncomment to behave as daemon
# with daemon.DaemonContext():
# comment to behave as daemon


def on_new_config(config):
    print (config)

async def config_handler(subscriber, on_new_config, topic_def, encoding):
    msg = await subscriber.arecv_msg()
    raw = msg.bytes
    data = raw.decode(encoding).partition(topic_def)[2]

    object = json.loads(data)
    on_new_config(object)
    
async def begin_config_handler():
        # create config publisher
    encoding = Definitions.instance().definition('TRANSFER_ENCODING')
    topic_def:str = Definitions.instance().definition('TOPIC_CONFIG') + ": "
    topic_def_bytes:bytes = topic_def.encode(encoding)
    topic_def_offset = len(topic_def_bytes)
    config_subscriber = Sub0(
        dial=Definitions.instance().definition('PUBSUB_ADDRESS'), 
        recv_timeout=Definitions.instance().definition('RECEIVER_TIMEOUT_MS'))
    config_subscriber.subscribe(topic_def_bytes)
    
    while (1):
        await config_handler(config_subscriber, on_new_config, topic_def, encoding)


def start():
    run (begin_config_handler)
    

    
    
 