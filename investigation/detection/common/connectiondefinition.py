class ConnectionDefinition:
    def __init__(self, device_full_id:str, owner_name:str):
        self.owner_name:str = owner_name
        self.device_full_id:str = device_full_id