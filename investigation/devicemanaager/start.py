# this is for debugging: the intention is to daemonise the services, but for now we're starting them up in the same application.


import time
from configservice.configservice import start as start_configservice
from deviceservice.deviceservice import start as start_deviceservice


start_configservice()
start_deviceservice()


while(1):
    time.sleep(1)
