# Investigation for device detection: messagepanelservice


https://python.hotexamples.com/examples/libusb/-/usb_get_string_simple/python-usb_get_string_simple-function-examples.html
Access to USB gives permissions errors. Have to add user to rules:
https://raspberrypi.stackexchange.com/questions/125091/how-to-create-a-linux-user-group-that-grants-access-to-usb-devices
https://forums.raspberrypi.com/viewtopic.php?t=186839
https://github.com/pyusb/pyusb/discussions/432

coops@raspberrypi:~/projects/OperationLollipop $ groups
coops adm dialout cdrom sudo audio video plugdev games users input render netdev gpio i2c spi 


VERY VERY NAUGHTY:
sudo adduser coops root
But works to stop permissions errors. VS Code currently not playing nicely with applying sudo to python as externalTerminal setting does not appear to behave itsself.

messagepanel's job is to listen for MESSAGE events, and queue them up to be displayed in order of receipt.

It needs a display, which will be detected via USB. Any USB device with a tty is likely to pass, so we must have some other way of distinuishing a display panel from sensors.


The messageservice is a daemon process which takes all of its instruction from MQTT, just like all sensor devices. The deviceservice emits an event to show that there are changes (addtions/removals) to USB devices. When an addition is notified, all usb daemon services need to probe the device to see if they can use it.

It's a first-come-first served protocol: 

service checks to see if the USB device has been claimed yet.
If the device has not been claimed, the service claims it and performs its probe. 
    If the probe succeeds the service will register it with the deviceservice.
    If the probe fails, the service will release the device
On receiving a registration (UBS ID, servicename), the deviceservice will emit a device update event, in which the usb device id is no registered to a servicename.
If the usb device has been claimed, the service will wait a random time (less than 1 second) and will attemtp to claim the device again. 
If the service recieves a deviceservice device update event, it will check to see if the device it is attemtping to claim has been registered. 
    If the device has been registered, the service will stop claim attempts.

This is common functionality, which we can use throughout the USB devices: panel display, sensor and data services







