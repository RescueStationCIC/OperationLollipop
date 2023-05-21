from enum import Enum
from common.devicedefinition import DeviceDefinition


class GeneralError(Exception):
    class Definition(Enum):
        NO_ERROR=0
        NOT_IMPLEMENTED=1

    def __init__(self, error_definition: int, msg:str=""):
        self.error_definition:int = error_definition
        self.msg:str = msg
        super().__init__(msg)

class ConnectionError(GeneralError):
    class Definition(Enum):
        NO_ERROR=GeneralError.Definition.NO_ERROR
        NOT_IMPLEMENTED=GeneralError.Definition.NOT_IMPLEMENTED
        NO_DEVICE_FOR_DEFINITION=2
        DEVICE_CLASS_NOT_RECOGNISED=3
        NO_INTERFACE_FOR_DEVICE=4
        INTERFACE_CLAIM_FAILED=5 
        
    def __init__(self, device_definition:DeviceDefinition, error_definition:int, msg:str=""):
        self.device_definition:DeviceDefinition = device_definition
        super().__init__(error_definition, msg)