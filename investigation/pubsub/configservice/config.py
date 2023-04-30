
import os.path
import json

class Config():
    def create(config_path:str, create_if_missing:bool):
        
        if os.path.isfile(config_path):
            json.load(config_path)
            return Config(json)
        elif create_if_missing == True:
            Config().write(config_path)
        else:
            raise Exception("could not find config file at: " + config_path)
           
                
    def __init__(self, json):
        
        self.config_path = config_path;