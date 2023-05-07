class DeviceDefinition:
    def __init__(self, lsusb_object:dict) -> None:
        self.lsusb_object = lsusb_object
        self.bus=lsusb_object['bus']
        self.device=lsusb_object['device']
        self.id=lsusb_object['id']
        self.description=lsusb_object['description']
        self.system_id = self.bus + ":" + self.device + ":" + self.id
        

class DeviceScan:
    def __init__(self, list:list[DeviceDefinition]=[], additions:list[DeviceDefinition]=[], removals:list[DeviceDefinition]=[]):
        self.list = list
        self.additions = additions
        self.removals = removals
    
        