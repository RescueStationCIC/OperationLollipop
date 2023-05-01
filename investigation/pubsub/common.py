


class Common():
    
    __create_key = object()
    __instance = None

    
    @classmethod
    def create(cls):
        if (cls.__instance is None): 
            cls.__instance = Common(cls.__create_key)
        return cls.__instance
           
                
    def __init__(self, create_key): 
        assert(create_key == Common.__create_key), \
            "Common objects must be created using the class method, create"
        self.definitions = {
            'PUBSUB_ADDRESS': 'tcp://127.0.0.1:31313'
        }
        

    @classmethod  
    def definitions(cls):
        if (cls.__instance is None):
            raise Exception("use create first.")
        return cls.__instance.defintions
        

