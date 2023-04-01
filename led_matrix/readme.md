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


### Setting up the power supply
Power off EVERYTHING!
#### Spoofer
The USB Spoofer starts up with the Blue LED flashing. It means it's not set (although the output is 5v). To set it, hold the little button down as you power up the board. It starts multicolour flashing. 
Once the button is released, the LED returns red indicating that it is at 5v. 
Press and hold until the LED goes out, to save the value.

NOTE: in programming mode the output is ALWAYS 5v regardless of what we are going to set. The selected voltage will be output at the next connection.

Briefly pressing the button will cycle the modes; once you arrive at the necessary one hold it until the LED is switched off (then press and hold the button for a couple of seconds approx.) to save the setting.

LED colours are: Red-5V, yellow-9V, green-12V, blue-15V, blue-20V, purple-select the maximum voltage available (the output will therefore depend on the power supply connected to the module), white-cycle continuously all available voltages, useful for example with a multimeter connected to the output for Test different powerbank or USB charger/power supplies and know what their steps are available.

Since the device works as a Pass-Through, it supports up to 100W (which is the maximum supported by the PD standard); in the case of powerbanks instead the maximum power is 18W (PD2) - 20W (PD3), ie 12V to 1.5 UNTO

Disconnect and reeconnect. Ensure the LED lights up to the colour you have chosen. Make sure you measure the output voltage!

Plug the power connector into its connector on the display board
Plug the other end of the power connector into the spoofer. 

### Data
Mount the Adafruit matrix driver on the 40 pin connector of the UPS.
Plug the HUB75 connector into the Adafruit Mmatrix driver
Plug the other end of the HUB75 connector into the HUB75 connector, marked INPUT, on the display board.

### Power ON
Is there any fizzing?



