from sense_hat import SenseHat
import time
import signal
import sys
import random

# handle Ctrl-C
def signal_handler(sig, frame):
    sense.clear()
    sense.show_message("Cncl", 0.02,(0,60,0))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Langston's ant

# a list of tuples containing dx, dy, ix left turn, ix right turn
directions = [
        (0, 1, 1, 3),  # north
        (-1, 0, 2, 0), # west
        (0, -1, 3, 1), # south
        (1, 0, 0, 2)   # east
        ]

sense = SenseHat()
sense.clear()
sense.set_rotation(180)

x = 4; y = 4;
alive = set()
course = 0   # initial course is "north"

while True:
    #print (x, y)
    # if present in set: turn right, delete, move
    if (x,y) in alive:
        course = directions[course][3]
        alive.remove((x,y))
        x = x + directions[course][0]
        y = y + directions[course][1]
    else: # turn left, add to set, move
        course = directions[course][2]
        alive.add((x,y))
        x = x + directions[course][0]
        y = y + directions[course][1]

    # draw the area around the ant
    sense.clear()
    for ix in range(0,8):
        for iy in range(0,8):
            testx = x-4+ix
            testy = y-4+iy
            if ix == 4 and iy == 5:
                # here is the ant
                sense.set_pixel(ix,iy,100,0,0)
            elif (testx,testy) in alive:
                sense.set_pixel(ix,iy,0,60,0)

    time.sleep(0.08)

