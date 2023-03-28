# Grateful thanks to Yusof Bandar :-) 
# https://github.com/Air92/Project-CAD

import time
import serial

length = 31
serialport = serial.Serial("/dev/ttyUSB1")
time.sleep(0.1)

def SensorData():
    startArray = serialport.read(1)
    
    if(startArray[0] == 66):
        print ("42 start character found")
        byteArray = serialport.read(length)
        print (byteArray)        
        if(byteArray[0]== 0x4d):
            print ("4d start character found")
        else:
            print ("4d not found")
    else:
        print ("42 not found")    