from common.publisher import Publisher
from common.definitions import Definitions
from common.device import DeviceDefinition

class ConnectionPublisher(Publisher):
    def __init__(self, name:str):
        Publisher.__init__(self, Definitions.TOPIC_CONNECTION)
        self.name = name
        
    def publish(self, device_definition:DeviceDefinition):
        Publisher.publish(self,{'system_id':device_definition.system_id})