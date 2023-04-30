# Investigation into PubSub

https://levelup.gitconnected.com/how-to-deserialize-json-to-custom-class-objects-in-python-d8b92949cd3b

https://pypi.org/project/python-daemon/

https://pynng.readthedocs.io/_/downloads/en/latest/pdf/

https://stackoverflow.com/questions/8110310/simple-way-to-query-connected-usb-devices-info-in-python

Config Service will start, and open the default configuration file. it will send the configuration out onto the Config Topic.

Device Service will start, enumerate all USB devices, and send them out onto a PubSub topic: Devices
Device Service will listen to Config topic for any changes.

Data Service will start and subscribe to the Devices topic. It will use this to find all USB devices and all internally mounted drives. It will search for all devices which look like a removable drive. 
It will record the ids of all items. 
Data Service will listent to the Config Service
Data service will listen to the Log topic for any updates, and write the items to the file path specified by the Config service.

Reporting Service will start, and subscribe to the Devices topic. It will use this to find all USB devices currently connected. It will test each in turn to find one which is a Display Panel. Once tested successfully, the USB device ID is recorded. The Service will push a success message to the new panel display.

----


```
pip install python-daemon
```






