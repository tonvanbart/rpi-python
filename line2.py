#!/usr/bin/python3

from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

sense.clear()
#sense.set_rotation(180)
green = (0, 120, 0)
red = (120, 0, 0)

for x in range(0,8):
    sense.set_pixel(x, 3, green if x < 4 else red)
    sense.set_pixel(x, 4, green if x < 4 else red)
    sleep(0.5)

