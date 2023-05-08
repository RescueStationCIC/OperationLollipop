from common.publisher import Publisher
from common.definitions import Definitions
from common.connector import ConnectionDefinition

class ConnectionPublisher(Publisher):
    def __init__(self, name:str):
        Publisher.__init__(self, Definitions.TOPIC_CONNECTION)
        self.name = name
        
    def publish(self, connection_definition:ConnectionDefinition):
        Publisher.publish(self, connection_definition)