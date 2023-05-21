class DeviceDefinition:
    def __init__(self, lsusb_object:dict) -> None:
        self.lsusb_object = lsusb_object
        self.bus=int(lsusb_object['bus'],16)
        self.address=int(lsusb_object['device'],16)
        self.id=lsusb_object['id']
        self.description=lsusb_object['description']
        self.id_vendor= int(lsusb_object['id'].split(':')[0],16)
        self.id_product= int(lsusb_object['id'].split(':')[1],16)
        self.device_full_id = str(self.bus) + ":" + str(self.address) + ":" + self.id        


    
        