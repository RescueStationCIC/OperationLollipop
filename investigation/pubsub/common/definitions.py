


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
            'PUBSUB_ADDRESS': 'tcp://127.0.0.1:31313',
            'TOPIC_CONFIG' : 'CONFIG',
            'TRANSFER_ENCODING': 'UTF-8',
            'RECEIVER_TIMEOUT_MS' : 100000
            
            }
        


        

