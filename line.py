#!/usr/bin/python3

from sense_hat import SenseHat
from time import sleep
from math import radians,sin,cos

sense = SenseHat()
sense.set_rotation(180)

#sense.show_message("test")

def draw_line(direction):
    if direction < 0 or direction > 360:
        raise ValueError("direction should be between 0 and 360")
    rad = radians(direction)
    mysin = sin(rad)
    mycos = cos(rad)
    x = int(round(3.5 + mycos * 4))
    y = int(round(3.5 + mysin * 4))
    if x > 7:
        x = 7
    if y > 7:
        y = 7
    if x < 0:
        x = 0
    if y < 0:
        y = 0

    sense.set_pixel(x, y, 0, 120, 0)
    
    print(direction,x,y)


sense.clear()
for deg in range(0, 360, 20):
    #print(deg)
    sense.clear()
    draw_line(deg)
    sleep(0.5)

sense.clear()
