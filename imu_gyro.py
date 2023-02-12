from sense_hat import SenseHat
from time import sleep
import signal
import sys

sense = SenseHat()
sense.set_rotation(180)

def signal_handler(sig, frame):
    sense.clear()
    sense.show_message("stop", 0.02,(0,60,0))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


y = [255,255,0]
x = [0,0,0]
b = [0,0,255]

charx = 0
chary = 0

while True:
    sense.set_pixel(charx, chary, b)
    pitch = sense.get_orientation()['pitch']
    roll = sense.get_orientation()['roll']
    if 270 < pitch < 315 and charx < 7:
        charx = charx + 1
    if 45 < pitch < 90 and charx > 0:
        charx = charx - 1
    if 45 < roll < 90 and chary < 7:
        chary = chary + 1
    if 270 < roll < 315 and chary > 0:
        chary = chary -1
    sleep(0.5)
