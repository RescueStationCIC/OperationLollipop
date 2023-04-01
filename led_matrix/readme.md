# Adafruit RGB Matrix HAT + RTC  

This HAT uses a Real Time Clock (RTC) to sync the driver signals to the LED matrix display.

## What is it?
* Get it [here](https://www.amazon.co.uk/Adafruit-RGB-Matrix-HAT-Raspberry/dp/B00SK69C6E)
* Tutorial [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi)
* Data sheet [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/pinouts)

NOTE: This really does use ALOT of pins, which is why most of the other functionality uses the USB connection.

## Why are we using it?

This HAT sits between the RPi and the LED Matrix display. It provides the 5v high current connection needed by the display, and converts the output from the RPi to the HUB75 protocol, which addresses the LEDs in the panel, via an 8x2 connector.
Both the power and HUB75 connectors come with the LED Matrix display, but they are too short. Fortunately, we can get the from PiHut.

## How do we set it up?
The Hat needs a 5v DC Input, which needs to supply it with enough juice to light the LEDs on the display panel. We're trying to keep things as Plug-n-play as possible, so we have a battery pack which delivers USB PD. We plug this into a device called a spoofer, which tells the USB PC battery pack that it is a high power device. The spoofer is connected to a 5v 2.1mm male connector, which plugs into the driver board.
Meanwhile the driver board connects onto the RPi's 40-pin GPIO connector. The UPS also connects via this connector, and is huge, with the giant Li-ion batteries, so we use standoffs to support the board a fair distance above it (they both get very warm), and a 40-way ribbon cable.


### Quick
The USB Spoofer starts up with the Blue LED flashing. It means it's not set (although the output is 5v). To set it, hold the little button down as you power up the board. It starts multicolour flashing. Make sure you measure the output voltage. As you press the button, you'll cycle through the output voltages. When you get to 5v. Long press the button, until the light goes out. Keep measuring the voltage, and ensure that you have 5v.
