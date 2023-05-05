import re
import subprocess
import os.path
import json
from common.definitions import Definitions

class MessagePanel():
    
    __create_key = object()
    __instance = None

    
    @classmethod
    def create(cls ):
        if (cls.__instance is None): 
            cls.__instance = MessagePanel(cls.__create_key)
        cls.__instance.read()
        return cls
           
                
    def __init__(self, create_key): 
        assert(create_key == MessagePanel.__create_key), \
            "MessagePanel objects must be created using the class method, create"
        
    
    @classmethod  
    def read(cls):
        # find appropriate USB devices to send text to, for display
        if (cls.__instance is None):
            raise Exception("use create first.")

        print(cls.__instance.data)
        
        return cls
    
    @classmethod  
    def data(cls):
        # return the current set of identified devices
        if (cls.__instance is None):
            raise Exception("use create first.")
        return cls.__instance.data
        
    @classmethod
    def display(cls, message:str):
        