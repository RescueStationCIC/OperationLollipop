# Investigation for device detection: messagepanelservice


messagepanel's job is to listen for MESSAGE events, and queue them up to be displayed in order of receipt.

It needs a display, which will be detected via USB. Any USB device with a tty is likely to pass, so we must have some other way of distinuishing a display panel from sensors.


