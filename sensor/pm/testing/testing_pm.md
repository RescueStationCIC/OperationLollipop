# Testing the DF Robot PM 1.0 - 10um Sensor 

The datasheet for the kit is [here](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/pm/datasheet/PMS5003ST_series_data_manual_English_V2.6.pdf)  

However, this doesn't contain the information necessary to drive it through the interface card, which they supply. You can find it[here](https://www.dfrobot.com/product-1612.html), and on the company's wiki, [here](https://wiki.dfrobot.com/Air_Quality_Monitor__PM_2.5_Temperature_and_Humidity_Sensor__SKU__SEN0233#target_6)

The intention is to put this sensor on the end of a USB cable, so it can be situated away from the the processor. This means we need a USB cable, and a USB-UART Adapter, for comms.

The company info for the USB to UART Adapter is [here](https://www.deshide.com/product-details.html?pid=303205&_t=1661493660)


# Connecting the USB-UART Adapter to the sensor 

The one thing which is clear is that the sensor requires a Vcc of 5v, and yet expects a UART connection with 3.3v. 

That is unkind.  
 
I was trusting to some sort of luck, that the USB to UART converter I was buying would have some way of me getting at the 5v USB voltage on it, without too much trouble, because it has settable voltages. Alas, not to be.

My only option is to run a 5v cable alongside the USB cable. Which is 5v. That sucks.

You can do this, of course; there is a perfectly good 5v output from the RPi. 

But, if you're feeling lucky, you can always grab the soldering iron, and make a hopeless mess of a perfectly good component. This is what I am going to do.

To start off, here's the PM sensor, its adapter board, cable and in the foreground, the USB-UART adapter.

![](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/pm/photo/IMG_0293.jpeg)  

I checked the incoming pins on the USB, for the 5V VCC. I've got a standard debug cable and snipped off one of the ends. I've tinned it with a bit of solder and I've got some Blu-Tack (other sticky things are available) to hold it steady.

I'm going to try and solder it, keeping aware that the inportant chips are really close. I don't want to cook them. I also want to avoid shorting the data lines to the 5V line, with my fat-fingered soldering.

Here's the setup, having miracualously removed the case without cracking it.

![](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/pm/photo/IMG_0296.jpeg)  

Here's the final thing, with the 5v wire soldered in and ready to go:

![](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/pm/photo/IMG_0300.jpeg) 

Now I plug it in, and wait for a short to fry the USB controller on my RPi:

![](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/pm/photo/IMG_0301.jpeg) 

Presto! The red-light, and celebratory snack, shows no ill-effects! One point for the idiot with the iron.

Here's the output from the diagnostic, showing our newly connected USB-UART, on ttyUSB1.
```bash
coops@raspberrypi:~/projects/OperationLollipop/diagnostic $ ./get_usb.sh
/dev/ttyUSB0 - Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001
/dev/ttyUSB1 - FTDI_FT232R_USB_UART_A10OEDT2
```

Finally, let's connect the USB-UART adapter, the sensor interface and the sensor.

Here's the set-up:

![](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/sensor/pm/photo/IMG_0302.jpeg) 

A few things to mention:

1. I've used a jumper on the Adapter, to connect the pins CTS and RTS ( I think they correspod to CTS (clear to send) and DSR (data set ready) from RS232 days) it's so that when the UART adapter has data to go it will send it instantly. When data is ready flicks on the DSR to signal that it has data, and waits for the receiving entity to flick on CTS. In this case, I connect them.
2. The line from the TX (transmit) on the UART adapter goes to the RX on sensor interface. The TX on the sensor interface goes to the RX on the UART adapter.
3. The hacked-on 5v line goes to the 5v Vcc of the sensor adapter.
4. The GND (ground) line connects both the UART adapter and sensor adapter.

Disconnect the UART adapter from USB, so there is no power, while you mess about with the connections
When you're happy with your connections, plug the USB in. If you're powered, you should hear the fan in the PM sensor start to hum.


# Comms check
We're going to use some Python code, and VS Code in debug mode to check that the USB-UART-sensor comms is working.

Worth saying, at this point the version of Python we're using. Don't forget there's still a load of stuff out there for v2.7. But we are using v3:

```bash
coops@raspberrypi:~ $ python --version
Python 3.9.2
```
Install Python's package manager, pip:

```bash
sudo apt install python3-pip
```

Check pip's version:
```
coops@raspberrypi:~/projects/OperationLollipop $ pip --version
pip 20.3.4 from /usr/lib/python3/dist-packages/pip (python 3.9)
```


Install Pyserial:

```
python3 -m pip install pyserial
```

To check all has gone well, use Python to query the RPi for the serial devices we have connected. This is a more comprehensive version of the methods we used in [testing the gas sensors](../../gas/testing/testing_ethanol.md)

```
coops@raspberrypi:~/projects/OperationLollipop $ python -m serial.tools.miniterm

--- Available ports:
---  1: /dev/ttyAMA0         'ttyAMA0'
---  2: /dev/ttyUSB0         'CP2102 USB to UART Bridge Controller - CP2102 USB to UART Bridge Controller'
---  3: /dev/ttyUSB1         'FT232R USB UART - FT232R USB UART'
```

You can see we are on /dev/ttyUSB1 

To check the actual comms, use VS Code. Open the file: serialv2.py, and check the following line matches the entry above:
```python
serialport = serial.Serial("/dev/ttyUSB1")
```

VSCode will now let you debug `pm_test.py`. It's a very quick and dirty test, just to see if we're getting anything sensible out of the serial port:
```bash
coops@raspberrypi:~/projects/OperationLollipop $  cd /home/coops/projects/OperationLollipop ; /usr/bin/env /bin/python /home/coops/.vscode-server/extensions/ms-python.python-2023.4.1/pythonFiles/lib/python/debugpy/adapter/../../debugpy/launcher 40311 -- /home/coops/projects/OperationLollipop/sensor/pm/testing/pm_test.py 
42 start character found
b'M\x00\x1c\x00\x03\x00\x04\x00\x05\x00\x03\x00\x04\x00\x05\x02F\x00\xc0\x00\x1e\x00\x01\x00\xb3\x01\xda\x9a\x00\x04\x12'
4d start character found
42 start character found
b'M\x00\x1c\x00\x03\x00\x04\x00\x05\x00\x03\x00\x04\x00\x05\x02F\x00\xc0\x00 \x00\x01\x00\xb3\x01\xda\x9a\x00\x04\x14'
4d start character found
42 start character found
```

What this is doing is reading what's coming over, and checking it for two specific markers. Once we know the data is good, we can continue. Note also that the data is changing from one reading to the next.