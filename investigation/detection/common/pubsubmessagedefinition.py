class PubSubMessageDefinition:
    def __init__(self, data:object, filter:str):
        self.data:object = data
        self.filter:str = filter
