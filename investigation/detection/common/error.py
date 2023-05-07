from enum import Enum
from common.device import DeviceDefinition

class ConnectorError(Exception):
    class Definition(Enum):
        NO_ERROR=0
        NOT_IMPLEMENTED=1
        NO_DEVICE_FOR_DEFINITION=2
        DEVICE_CLASS_NOT_RECOGNISED=3
        NO_INTERFACE_FOR_DEVICE=4
        INTERFACE_CLAIM_FAILED=5
        
    def __init__(self, device_definition:DeviceDefinition, error_definition:Definition, msg:str=""):
        self.device_definition:DeviceDefinition = device_definition
        self.error_definition:ConnectorError.Definition = error_definition
        self.msg:str = msg
        super().__init__(self.msg)