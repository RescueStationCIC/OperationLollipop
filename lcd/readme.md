# USB + Serial Backpack Kit with 16x2 RGB backlight negative LCD (RGB on Black)

## What is it?
* get it [here](https://thepihut.com/products/adafruit-usb-serial-backpack-kit-with-16x2-rgb-backlight-negative-lcd)
* tutorial [here](https://learn.adafruit.com/usb-plus-serial-backpack)
* data sheets [here](https://learn.adafruit.com/usb-plus-serial-backpack/downloads)

## Why are we using it?

The RPi is running headless - it doesn't have a user interface. We need something to give us useful information about status:

Modes of operation:
  * Start up
  * Sensor warm-up
  * Operation
  * Error
  * Shut down


## How do we set it up?
The panel comes as a kit: there is the panel its-self, and a nifty converter 'backpack' which gives you either USB or UART input, used along with an SDK.
The backpack and panel need to be connected via a header. The tutorial shows you how to do this, but it seems a little out of date, and the LDC panel is not the same.
I soldered the header to the panel as they showed it, but when I looked at the next shot, of the orientation of the backpack, the orientation don't match mine.
Howver, going by the pin numbering, pin 1 should match up with GND on the backpack, so that is how I soldered it. We'll see if it goes 'fizz' later.