import re
import subprocess
import os.path
import json
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
        self.encoding = Definitions.instance().definition('TRANSFER_ENCODING')
    
    @classmethod  
    def read(cls):
        if (cls.__instance is None):
            raise Exception("use create first.")

        device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
        df = subprocess.check_output("lsusb")
        df_str = df.decode(cls.__instance.encoding)
        devices = []
        for i in df_str.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)
        cls.__instance.data = devices
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
