# Testing the Spec Sensor Dev Kit

We're using the ethanol sensor, and connecting it onto it's driver board. The driver board powers the sensor, and converts the analog sensor output to digital, which can be read via UART. A total bonus (caused, probably, by not reading the datasheet properly) is that there is a further interface board, converting the UART to serial USB. 
We will test this, by connecting the sensor to the RPi, via USB, and sending it commands.  

The datasheet for the kit is [here](https://cdn.jsdelivr.net/gh/RescueStationCIC/OperationLollipopRescources/sensor/gas/datasheet/968-045_9-6-17.pdf)]  

We're going to use the ethanol sensor, as it's not needed for ourp purposes, so we don't mind too much if we mess up, easiest and most fun to test. A little Brandy, anyone..? :-D

## Comms



