#!/usr/bin/python3

# install paho-mqtt for python3

from threading import Thread, Lock
from  sense_hat import SenseHat
import paho.mqtt.client as mqtt

mutex = Lock()

red = (150, 0, 0)
green = (0, 150, 0)
blue = (0, 0, 150)
txt_colour = blue;

sense = SenseHat()
sense.set_rotation(180)
sense.show_message("MQTT", text_colour=green);
sense.clear(60,0,60)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ESEiot/1718/+/Demo/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global txt_colour
    print(msg.topic+" "+str(msg.payload))
    # sense.show_message(msg.topic + " " + str(msg.payload));
    sense.show_message(str(msg.payload), text_colour=txt_colour);
    sense.clear(60,60,0)
    if txt_colour == red:
      txt_colour = blue
    else:
      txt_colour = red

#broker_address = "broker.hivemq.com"
broker_address = "127.0.0.1"  # local broker

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    # connect(host, port=1883, keepalive=60, bind_address="")
    client.connect(broker_address, 1883, 60)
    with mutex:
        print("Success connecting: " + broker_address)
except ():
    with mutex:
        print("Cannot connect to:  " + broker_address)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

