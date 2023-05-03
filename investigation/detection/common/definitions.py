


class Definitions():
    
    __create_key = object()
    __instance = None

    
    @classmethod
    def instance(cls):
        if (cls.__instance is None): 
            cls.__instance = Definitions(cls.__create_key)
        return cls.__instance
           
    @classmethod  
    def definition(cls,key):
        if (cls.__instance is None):
            raise Exception("use instance first.")
        return cls.__instance.definitions.get(key)     
                
    def __init__(self, create_key): 
        assert(create_key == Definitions.__create_key), \
            "Definitions objects must be created using the class method, instance"
        self.definitions = {
            'PUBSUB_ADDRESS': '127.0.0.1',
            'PUBSUB_PORT': 1883,
            'PUBSUB_KEEPALIVE': 60,
            'TOPIC_CONFIG' : 'CONFIG',
            'TOPIC_REGISTRATION': 'REGISTRATION',
            'TOPIC_DEVICELIST': 'DEVICELIST',
            'TRANSFER_ENCODING': 'UTF-8',
            'RECEIVER_TIMEOUT_MS' : 100000,
            'SERVICENAME_CONFIG' : 'configurationservice',
            'SERVICENAME_DEVICE' : 'deviceservice',
            'SERVICENAME_MESSAGEPANEL': 'messagepanelservice',
            'PATH_DEVICES':'/dev/bus/usb',
            'PATH_CONFIG':'./config.json'
            }
        


        

