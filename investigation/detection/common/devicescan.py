from common.devicedefinition import DeviceDefinition

class DeviceScan:
    def __init__(self, list:list[DeviceDefinition]=[], connections:dict={}, additions:list[DeviceDefinition]=[], removals:list[DeviceDefinition]=[]):
        self.list = list
        self.connections = connections
        self.additions = additions
        self.removals = removals