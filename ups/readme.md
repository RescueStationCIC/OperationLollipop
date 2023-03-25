# Geekworm X728 UPS

Provides uninteruptable power supply, function for auto shutdown on low power and buzzer.

## What is it?

Hmm. Well, ordered from Amazon, (here)[https://www.amazon.co.uk/dp/B087J7WTYM]. But this now resolves to (here)[https://www.amazon.co.uk/Geekworm-Raspberry-Management-Shutdown-Function/dp/B08YRCJP37], which is the X708. No explanation.

Tutorial [here](https://wiki.geekworm.com/X728)

Battery specification [here](https://wiki.geekworm.com/images/2/2e/NCR18650B.pdf)

Software Tutorial [here]()

## Why are we using it?

If the battery is allowed to fail, then the Raspberry Pi operation is rudely interrupted. It can cause a whole host of unexepected problems. This kit provides the ability for the Pi to keep going, until it can be plugged into a power supply, or automatically save and shutdown. If the supply is turned off, or becomes unstable, a buzzer sounds. At this point, it's time to stop using the LED sign (it will discharge the battery REALLY quickly) and to charde the device and the main battery. There's plenty of time to do this, and it means that the sensors don't have to be cooled down.

## How do we set it up?
It's really important to get the battery right. Panasonic 18650 3.7V NON-PROTECTED.  

