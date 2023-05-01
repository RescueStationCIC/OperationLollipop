
import os.path
import json

class Config():
    
    __create_key = object()
    __instance = None

    
    @classmethod
    def create(cls, config_path:str):
        abs_path = config_path
        if(config_path.startswith('.')):
            abs_path = os.path.join(os.path.dirname(__file__),config_path)
        if os.path.isfile(abs_path):
            if (cls.__instance is None): 
                cls.__instance = Config(cls.__create_key, abs_path)
            cls.__instance.read()
        else:
            raise Exception("could not find config file at: " + abs_path)
        return cls
           
                
    def __init__(self, create_key, config_path:str): 
        assert(create_key == Config.__create_key), \
            "Config objects must be created using the class method, create"
        self.config_path = config_path
    
    
    @classmethod  
    def read(cls):
        if (cls.__instance is None):
            raise Exception("use create first.")
        f = open(cls.__instance.config_path)
        cls.__instance.data = json.load(f)
        f.close
        return cls
    
    @classmethod  
    def data(cls):
        if (cls.__instance is None):
            raise Exception("use create first.")
        return json.dumps(cls.__instance.data)
        
    @classmethod  
    def path(cls):
        if (cls.__instance is None):
            raise Exception("use create first.")
        return cls.__instance.config_path    
