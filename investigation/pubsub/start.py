import time
from configservice.configservice import start as start_configservice
from deviceservice.deviceservice import start as start_deviceservice


start_configservice()
start_deviceservice()


while(1):
    time.sleep(1)
