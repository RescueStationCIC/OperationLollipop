# Investigation for deviceservice

deviceservice's job is to listen for device connections and removals.

This is for all USB devices: sensors, drives, and displays.

The idea is that the service will publish the connection details of any new devices, and subscribers can check that the details correspond to devices which they are interested in.


service will monitor devices. On a connect, the service will ascertain if the device is a drive or a USB device. If USB, it will publish DEVICE/USB topic if drive, it will publish on DEVICE/DRIVE topic.

on publishing DEVICE/USB there are components (messagedisplayservice, sensorservice) which will need to interrogate the device, in order to work out if it is usable. 

There will need to be some form of competition management for connections.



