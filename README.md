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
You'll need to install git on the RPi.  
On the RPi terminal:

```bash
apt update
```

```bash
apt install git
```
### Fork this repo
In your browser, you'll need to create an account on GitHub, if you haven't already, and Fork this repository, so a linked copy of it appears in your account.

### Download the repo
On the RPi terminal:

1. create a projects directory:
```bash
mkdir -p ~/projects
```
2. In the browser, go to your forked project in GitHub. In the **Code** tab, use the 'Code' button to get the HTTPS address of the repository. For example, this one is:
```bash
https://github.com/RescueStationCIC/OperationLollipop.git
```
3. Clone your repo into the project directory
For example:
```bash
cd ~/projects
````
```bash
git clone https://github.com/RescueStationCIC/OperationLollipop.git
```ß

### Start your developing
1. In the browser, navigate to your GitHub account. In [settings, email address](https://github.com/settings/emails) make sure you have set a PRIVATE email address. This is just so your actual email address isn't made public in your commit comments, if you don't want it to be.
2. In the RPi terminal, set your github configuration, for the username and email which will be attributed to you when you check in. For example:

```bash
git config --global user.name coopsatwork
``` 

```bash
git config --global user.email coopsatwork@users.noreply.github.com
```

2. Open the remote project in VS Code 
When you start VS Code, look for the green >< in the bottom left corner. This will help you log into the RPi.  
VSCode will give you the option to Open A Folder. Browse to your downloaded fork of this project.
3. Make a change to this file, and attempt to check it back in.










