# Testing the Spec Sensor Dev Kit

We're using the ethanol sensor, and connecting it onto it's driver board. The driver board powers the sensor, and converts the analog sensor output to digital, which can be read via UART. A total bonus (caused, probably, by not reading the datasheet properly) is that there is a further interface board, converting the UART to serial USB. 
We will test this, by connecting the sensor to the RPi, via USB, and sending it commands.  

The datasheet for the kit is [here](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/gas/datasheet/968-045_9-6-17.pdf)  

We're going to use the ethanol sensor, as it's not needed for ourp purposes, so we don't mind too much if we mess up, easiest and most fun to test. A little Brandy, anyone..? :-D

## Mate sensor with main board

Here's the unpopulated board:  

![](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/gas/photo/IMG_0284.jpeg)  

Being as careful as possible to earth yourself, handle the sensor by the outside of the board only:  

![](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/gas/photo/IMG_0288.jpeg) 

It's dead easy to push the sensor onto the board. There's only one way it can go:  

![](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/gas/photo/IMG_0289.jpeg) 


## Comms

OK, after plugging the device in, on the RPi, us the folloing to list the all USB devices.  
```bash
coops@raspberrypi:~ $ lsusb
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 003: ID 10c4:ea60 Silicon Labs CP210x UART Bridge
Bus 001 Device 002: ID 2109:3431 VIA Labs, Inc. Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

You can see that Device 003 Silicon Labs CP210x UART Bridge, is the one we want. 

Everything on Linux is either a file or a directory. Linux will marry up the USB device to a 'file' under the directory /dev/

```bash
coops@raspberrypi:~/projects/OperationLollipop $ ls /dev | grep USB
ttyUSB0
```
Looks like there's only one USB device connected. But how do we know it's ours?

```bash
dmesg
```

This is quickest way of checking. It's a log-file of all device interactions so far. If you've just plugged in the device, it'll be one of the last entries.

Sure enough:
```bash
[ 7298.951108] usb 1-1.3: new full-speed USB device number 3 using xhci_hcd
[ 7299.056536] usb 1-1.3: New USB device found, idVendor=10c4, idProduct=ea60, bcdDevice= 1.00
[ 7299.056574] usb 1-1.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[ 7299.056592] usb 1-1.3: Product: CP2102 USB to UART Bridge Controller
[ 7299.056607] usb 1-1.3: Manufacturer: Silicon Labs
[ 7299.056621] usb 1-1.3: SerialNumber: 0001
[ 7299.151921] usbcore: registered new interface driver usbserial_generic
[ 7299.152009] usbserial: USB Serial support registered for generic
[ 7299.159018] usbcore: registered new interface driver cp210x
[ 7299.159069] usbserial: USB Serial support registered for cp210x
[ 7299.159149] cp210x 1-1.3:1.0: cp210x converter detected
[ 7299.164428] usb 1-1.3: cp210x converter now attached to ttyUSB0
```

or, you can use the diagnostic script in this repo:

```bash
coops@raspberrypi:~/projects/OperationLollipop/diagnostic $ ./get_usb.sh
/dev/ttyUSB0 - Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001
```

(thanks to: [Dmitry Grigoryev](https://raspberrypi.stackexchange.com/a/124588))

We're going to install the 'screen' utility, which will enable us to talk to the device:

```bash
sudo apt update
sudo apt install screen
```

Now we can connect:

```bash
screen /dev/ttyUSB0
```

Note: you can disconnect at any time, by pressing `CTRL+D`. More [here](https://linuxize.com/post/how-to-use-linux-screen/) 


## RTFM (Read the !Fine! Manual)

From the fine manual:

```
Start Continuous Measurement in Terminal Window
    a. Type any key to exit low-power standby mode.
    b. Press the Enter key (‘\r’) to transmit a single measurement string.
    c. Type ‘c’ (lower-case c, without quotation marks) to start continuous output.
    d. The format of the output is:
            SN, PPB, T (°C), RH (%), ADC Raw, T Raw, RH Raw, Day, Hour, Minute, Second
    e. Type ‘c’ to stop the continuous output
    f. Type ‘s’ to enter low-power standby mode
Initial ZERO (Clean Air) Calibration
    a. When first given power after a long period of unpowered storage, the sensor needs to
stabilize in clean air to its zero offset current.
    b. WAIT at least 1 hour in clean air while ensuring the computer and USB port have not
gone to sleep.
    c. Type ‘Z’ in the terminal window to re-zero the sensor output.
```

WORKS (with a whiff of Brandy)

SN, PPB, T (°C), RH (%), ADC Raw, T Raw, RH Raw, Day, Hour, Minute, Second
081021010213, 7956, 17, 46, 13484, 23868, 27590, 00, 00, 58, 21
081021010213, 7611, 17, 46, 13464, 23960, 27526, 00, 00, 59, 31
081021010213, 7811, 17, 46, 13476, 23960, 27526, 00, 00, 59, 33
081021010213, 7082, 18, 45, 13434, 24212, 26918, 00, 01, 06, 48
081021010213, 14719, 18, 56, 13897, 24476, 32602, 00, 01, 07, 13
081021010213, 8115, 18, 85, 13497, 24328, 47766, 00, 01, 07, 23
081021010213, 7701, 18, 86, 13472, 24320, 48534, 00, 01, 07, 26
081021010213, 7653, 18, 86, 13469, 24304, 48662, 00, 01, 07, 31