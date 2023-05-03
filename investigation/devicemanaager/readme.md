# Investigation into PubSub

https://stackoverflow.com/questions/2349991/how-do-i-import-other-python-files

https://stackoverflow.com/questions/73166298/cant-do-python-imports-from-another-dir

https://stackoverflow.com/questions/8212053/private-constructor-in-python

https://levelup.gitconnected.com/how-to-deserialize-json-to-custom-class-objects-in-python-d8b92949cd3b

https://pypi.org/project/python-daemon/

https://pynng.readthedocs.io/_/downloads/en/latest/pdf/

https://stackoverflow.com/questions/8110310/simple-way-to-query-connected-usb-devices-info-in-python

https://www.engineersgarage.com/mqtt-broker-mosquitto-raspberry-pi/


configurationservice will start, and open the default configuration file. it will send the configuration out onto the CONFIG Topic. It will listen for publishes to the REGISTRATION topic.

Device Service will start, and listen to the CONFIG Topic. When ready, it will publish to the REGISTRATION Topic. This will cause the configurationservice to publish to CONFIG.

Originally, I was working with an ultra-lite PUBSUB implementation, which had no data retention. This meant that subscribing to a particular topic would not cause a message to be sent witht he current state. The alternative is to you registration to trigger an update of the latest information.

As it was the implementation didn't support multiple publishers to a topic, so I ended up having to port to the slightly more heavyweight Mosquitto MQTT broker. I'm happy with that :-)

----


daemon service
```
pip install python-daemon
```

filesystem events
```
pip install watchdog
```

NNG PubSub
```
pip3 install pynng
```

NNG PubSub was a VERY BAD IDEA. Cannot do multiple Publishers to Multiple subscribers. And If I'd thought about it for any length of time, that would have been obvious.

Going to put mosquito MQTT onto RPi. This supports retention, too:
```
sudo apt install -y mosquitto mosquitto-clients
```

Then install pahoe-mqtt:
```
pip install paho-mqtt
```


check MQTT configuration
```
sudo nano etc/mosquitto/mosquitto.conf
```

add the following:
```
allow_anonymous true
```

startup mosquitto:

```
sudo systemctl start mosquitto
```

but debugging, it's more useful to create a new terminal login, and startup mosquitto from the commandline, as it outputs all logging of connections and data transfers:

```
sudo systemctl stop mosquitto
mosquitto -v
```


