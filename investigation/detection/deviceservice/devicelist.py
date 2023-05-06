import re
import subprocess
import os.path
import json
import jc
from common.definitions import Definitions

class DeviceList():
    
    __create_key = object()
    __instance = None

    
    @classmethod
    def create(cls, devices_path:str):
        abs_path = devices_path
        if(devices_path.startswith('.')):
            abs_path = os.path.join(os.path.dirname(__file__),devices_path)
        if os.path.isdir(abs_path):
            if (cls.__instance is None): 
                cls.__instance = DeviceList(cls.__create_key, abs_path)
            cls.__instance.read()
        else:
            raise Exception("could not find devices directory at: " + abs_path)
        return cls
           
                
    def __init__(self, create_key, devices_path:str): 
        assert(create_key == DeviceList.__create_key), \
            "DeviceList objects must be created using the class method, create"
        self.devices_path = devices_path
        self.default_langid = Definitions.USB_LANGID
        self.encoding = Definitions.TRANSFER_ENCODING
        self.data={'list':[], 'additions':[], 'removals':[]}
        
    
    @classmethod  
    def read(cls):
        if (cls.__instance is None):
            raise Exception("use create first.")
        encoding = cls.__instance.encoding
        output = subprocess.check_output(
            ["lsusb"]
#            ,"-v"
            ).decode(encoding)
        devices = jc.parse('lsusb', output )
        
        incumbents = cls.__instance.data['list']
        additions=[]
        removals=[]
            
        for incoming in devices:
            found = False
            for incumbent in incumbents:
                if incoming['id'] ==  incumbent['id']: # reconnected USB devices get same id 
                    found = True
                    break  
            if (found == False):
                additions.append(incoming)
                
        for incumbent in incumbents:
            found = False
            for incoming in devices:
                if incoming['id'] ==  incumbent['id']: # reconnected USB devices get same id 
                    found = True
                    break  
            if (found == False):
                removals.append(incoming)
                         
        cls.__instance.data['list'] = devices
        cls.__instance.data['additions'] = additions
        cls.__instance.data['removals'] = removals
        
        str_debug = json.dumps(cls.__instance.data, indent=2)
        print (str_debug)
                
        return cls
    
    @classmethod  
    def data(cls):
        if (cls.__instance is None):
            raise Exception("use create first.")
        return cls.__instance.data
        
    @classmethod  
    def path(cls):
        if (cls.__instance is None):
            raise Exception("use create first.")
        return cls.__instance.devices_path    
