# Testing the LCD
As with all the other devices connected to the RPi, this is connected via USB. It's mini-USB. So, having jumped that particular cable-hurdle, we're up for testing.

## Comms check
We're going to use some Python code, and VS Code in debug mode to check that the USB-serial comms is working.

### Install 
If you've aleady tested the other USB device, you can skip this step.

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
### Ready to test
To check all has gone well, use Python to query the RPi for the serial devices we have connected. This is a more comprehensive version of the methods we used in [testing the gas sensors](../../gas/testing/testing_ethanol.md)

```
coops@raspberrypi:~/projects/OperationLollipop $  python -m serial.tools.miniterm

--- Available ports:
---  1: /dev/ttyACM0         'Adafruit Industries'
---  2: /dev/ttyAMA0         'ttyAMA0'
---  3: /dev/ttyUSB0         'CP2102 USB to UART Bridge Controller - CP2102 USB to UART Bridge Controller'
---  4: /dev/ttyUSB1         'FT232R USB UART - FT232R USB UART'
```

You can see we are on /dev/tttyACM0.

The next thing to note is that miniterm is actually interactive. It's asking you to type the index number of the device. Our device is Index 1: 'Adafruit Industries'.
If you type '1', you'll see that mini term then attempts to connect to the serial device:
```
--- Enter port index or full name: 1
--- Miniterm on /dev/ttyACM0  9600,8,N,1 ---
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---
```

The numbers `9600,8,N,1 ---' is how the program is attempting to define the communications parameters. This is for legacy serial drivers. USB simply ignores this.

You'll now find that, thanks to the Adafruit backpack board, whatever you type into the keyboard, appears on the screen :-)

![](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopResources/lcd/photo/IMG_0303.jpeg) 

We'll do a quick python program to send some special characters, according to the blurb above. You can see it in [lcd_test.py](./lcd_test.py).