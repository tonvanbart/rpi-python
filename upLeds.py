#!/usr/bin/python

from  sense_hat import SenseHat
import time
import socket

def get_ip_address():
   ip_address = ''
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   try:
       s.connect(("8.8.8.8", 80))
       ip_address = s.getsockname()[0]
       s.close()
   except Exception, e:
       ip_address = 'not connected'
   return ip_address

#-------------------------------------------------------------------------------

sense = SenseHat()
speed = 0.075
maxRGB = 100
hostname = socket.gethostname()
rgbLightYellow = (50, 50, 30)

for rotation, text in zip([0, 90, 180], ["IoT", "BLE", "MQTT"]):
	sense.set_rotation(rotation)
 	sense.show_message(text, speed, (rotation/2, maxRGB, maxRGB))
 	sense.show_message(hostname, speed, (rotation/2, maxRGB, maxRGB))
 	sense.show_message(get_ip_address(), speed, (rotation/2, maxRGB, maxRGB))
	time.sleep(0.5)

sense.show_message("I'm completely operational and all my circuits are functioning perfectly.",speed,text_colour=[0,127,0])
sense.clear()
#sense.set_rotation(0)
#sense.clear(rgbLightYellow)
#
## x: 0 is on the left, 7 on the right
## y: 0 is at the top, 7 at the bottom
#sense.set_rotation(0)
#sense.set_pixel(0, 0, (maxRGB, maxRGB, maxRGB))
#sense.set_pixel(0, 7, (maxRGB, 0, 0))
#sense.set_pixel(7, 0, (0, maxRGB, 0))
#
#for x in range(1, 7):
#	sense.set_pixel(x, 0, maxRGB/(x+1), maxRGB, maxRGB/(x+1))
#for y in range(1, 7):
#	sense.set_pixel(0, y, maxRGB, maxRGB/(y+1), maxRGB/(y+1))
