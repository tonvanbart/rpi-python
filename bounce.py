from sense_hat import SenseHat
import random
import time
import signal 
import sys

sense = SenseHat()
sense.clear()
sense.set_rotation(180)

def signal_handler(sig, frame):
    sense.clear()
    sense.show_message("Cncl", 0.02,(0,60,0))
    sys.exit(0)

G = [0,120,0]

signal.signal(signal.SIGINT, signal_handler)
x = random.randint(0,7)
y = random.randint(0,7)
speedx = -1
speedy = 1

for i in range(1000):
    sense.set_pixel(x,y,G)
    x = x + speedx
    y = y + speedy
    if x == 0 or x == 7:
        speedx = -speedx
#        if speedy > 0:
#            y = y+1 if y < 7 else y
#        else:
#            y = y-1 if y > 0 else y

    if y == 0 or y == 7:
        speedy = -speedy
#        if speedx > 0:
#            x = x+1 if x<7 else x
#        else:
#            x = x-1 if x>0 else x

    time.sleep(0.05)
    sense.clear()
