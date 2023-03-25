# OperationLollipop
A Raspberry Pi - based project, to drive a bright, wearable sign, advertising the current local air quality.

## This repo
This repo holds the scripts and code to be downloaded to the RPi.

## RPi
Needs an SD Card, loaded up with RPi OS Lite, 64-bit, via the RPi Imager.  
Using the RPi Imager advanced options, I set it up with:
* username (mine is coops) and password (mine is - erk, wait.)
* SSH Enabled
* no default WiFi (I'll be connected to my internet-connected network, via an Ethernet cable)

# For best results
I'm developing using my trusty MacBook pro, on the same network as the Pi.  
The idea is that I use a combination of Microsoft's Visual Studio Code (VS Code) editor running on the Mac and an SSH connection to directly create and build applications on the RPi.  
### SSH 
I use the command:   
```bash
arp -a
```  
... this shows me the devices that I have on my local network. The RPi should be listed, along with its IP address - for example:   
```bash
arp -a
raspberrypi.lan (10.57.10.128) ...
```   
I can then connect to the RPi from my Mac's terminal, using

```bash
ssh coops@10.57.10.128
```
I get a password prompt, and then I'm in :-)

### MS VS Code
I've downloaded VS Code onto my Mac. Then I set it up to work on a remote machine, via SSH, by installing Microsoft's Remote Extension pack, from within VS Code.

### Git
#### Install on the RPi
You'll need to install git on the RPi:

```bash
apt update
```

```bash
apt install git
```
### Fork this repo
You'll need to create an account on GitHub, if you haven't already, and Fork this repository, so a linked copy of it appears in your account.

### Download the repo













