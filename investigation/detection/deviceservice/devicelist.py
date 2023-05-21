import re
import subprocess
import os.path
import jc
import jsonpickle
from common.definitions import Definitions
from common.devicedefinition import DeviceDefinition
from common.devicescan import DeviceScan
from common.connector import ConnectionDefinition
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
        self.data= DeviceScan()
        
    
    @classmethod  
    def read(cls):
        if (cls.__instance is None):
            raise Exception("use create first.")
        encoding = cls.__instance.encoding
        output = subprocess.check_output(
            ["lsusb"]
#            ,"-v"
            ).decode(encoding)
        parsed_items = jc.parse('lsusb', output )
        
        # completely refresh the scan data
        definitions:list[DeviceDefinition]=[]
        additions:list[DeviceDefinition]=[]
        removals:list[DeviceDefinition]=[]
        
        # but connections are added by another mechanism - we can only remove them here
        connections:dict = cls.__instance.data.connections
            
        
        for item in parsed_items:
            definitions.append(DeviceDefinition(item))
        
        
        incomings = definitions
        incumbents = cls.__instance.data.list
        
        # compare the incomings and incumbents
        # additions are the incomings which don't exist in the incumbents
        # removals are the incumbents which dont exist in the incomings
        # if removals have proper connections, they need to be disconnected. 

        # addtions
        for incoming in incomings:
            found = None
            for incumbent in incumbents:
                if incoming.device_full_id ==  incumbent.device_full_id: 
                    found = incoming
                    break  
            if (found is None):
                additions.append(incoming)
                
        # removals        
        for incumbent in incumbents:
            found = None
            for incoming in incomings:
                if incoming.device_full_id ==  incumbent.device_full_id:
                    found = incumbent
                    break  
            if (found is None):
                connections.pop(incumbent)
                removals.append(incumbent)
                         
        cls.__instance.data = DeviceScan(definitions,connections, additions, removals)
        
        #str_debug = jsonpickle.encode(cls.__instance.data, indent=2)
        #print (str_debug)
                
        return cls
    
    @classmethod
    def add_connection(connection_definition: ConnectionDefinition):
        cls.__instance.data.connections[connection_definition.device_full_id]=connection_definition.owner_name
    
    
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
