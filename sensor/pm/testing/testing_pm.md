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


```bash
coops@raspberrypi:~/projects/OperationLollipop/diagnostic $ ./get_usb.sh
/dev/ttyUSB0 - Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001
/dev/ttyUSB1 - FTDI_FT232R_USB_UART_A10OEDT2
```

# Comms check

We're using [this resource](https://opensource.com/article/20/5/usb-port-raspberry-pi-python), from opensource.com, to find out how Python can be made to connect to the /dev USB devices.

Worth saying, at this point the version of Python we're using. Don't forget there's still a load of stuff out there for v2.7. But we are using v3:

```bash
coops@raspberrypi:~ $ python --version
Python 3.9.2
```

