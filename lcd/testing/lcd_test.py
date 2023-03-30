# testing we can send special characters to the LCD screen
# ASCII 13 is a new line character
# We can set the RGB of the backlight using hex values
# We can write text

import time
import serial
import codecs

length = 31
serialport = serial.Serial("/dev/ttyACM0")
time.sleep(0.1)

serialport.write(bytearray([13,13,13]))
# Backlight RED
cmd = bytearray([0xFE, 0xD0, 0xFF, 0x00, 0x00])
serialport.write(cmd)
serialport.write(b'RED')
serialport.write(bytearray([13]))
time.sleep(1)
# Backlight GREEN
cmd = bytearray([0xFE, 0xD0, 0x00, 0xFF, 0x50])
serialport.write(cmd)
serialport.write(b'GREEN')
serialport.write(bytearray([13]))
time.sleep(1)
# Backlight BLUE
cmd = bytearray([0xFE, 0xD0, 0x00, 0x00, 0xFF])
serialport.write(cmd)
serialport.write(b'BLUE')
serialport.write(bytearray([13]))
time.sleep(1)
# Backlight WHITE
cmd = bytearray([0xFE, 0xD0, 0xFF, 0xFF, 0xFF])
serialport.write(cmd)
serialport.write(b'WHITE')
serialport.write(bytearray([13]))
serialport.close()

