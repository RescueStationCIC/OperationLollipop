# Grateful thanks to Yusof Bandar :-) 
# https://github.com/Air92/Project-CAD

import time
import serial

def checkValue(buffer, length ):
    recievedflag = False
    recievedSum = 0
    for i in range(0, (length-2)):
        recievedSum = recievedSum + int(buffer[i],16)

    recievedSum = recievedSum + 0x42

    if((int(buffer[length-2],16)<<8)+(int(buffer[length-1],16))==recievedSum):
        recievedflag = True
    
    return recievedflag


length = 31
#serialport = serial.Serial("/dev/serial0", 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1500)
serialport = serial.Serial("/dev/ttyUSB1")
#test = serialport.write(serial.to_bytes([0x4D]))
time.sleep(0.1)


def SensorData():
    startArray = serialport.read(1)
    
    #startArray = [elem.encode("hex") for elem in startArray]
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