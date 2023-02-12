from sense_hat import SenseHat
from paho.mqtt import client as mqtt_client

sense =  SenseHat()
fmt = "Humidity: {0:.1f}%,Pressure: {1:.1f}Mb"
broker = "broker.hivemq.com"
port = 1883
topic = "ESEiot/1718/reading"
clientid = 'python-rpi-mqtt'

def connect_mqtt():
	def on_connect(client,userdata,flags,rc):
		if rc==0:
			print("connected to broker")
		else:
			print("connection failed, return code %d\n",rc)
	client = mqtt_client.Client(clientid)
	client.on_connect = on_connect
	client.connect(broker,port)
	return client

def publish(client,msg):
	result = client.publish(topic, msg)
	print(result)
	status = result[0]
	if status==0:
		print("send successful")
	else:
		print("failed to send message")


client = connect_mqtt()

hum = sense.get_humidity()
press = sense.get_pressure()

message = fmt.format(hum, press)
sense.set_rotation(180)
print(message)
#sense.show_message(message, 0.03)
publish(client, message)
sense.show_message("published", 0.03)

