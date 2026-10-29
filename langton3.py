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

x = random.randint(0,7);  y = random.randint(0,7) # ant start coordinates
course = 0   # initial course is "north"

while True:
#   test 3 color rule:
#   if the current square is blank, turn right, flip color green, move
#   if it is green, turn it red, don't turn, move
#   if it is red, turn left, make it black, move
    if sense.get_pixel(x, y) == [0,0,0]:
        course = directions[course][3]
        sense.set_pixel(x, y, 0, 60, 0)
        x = x + directions[course][0]
        y = y + directions[course][1]
    elif sense.get_pixel(x, y) == [0, 60, 0]:
        sense.set_pixel(x, y, 60, 0, 0)
        x = x + directions[course][0]
        y = y + directions[course][1]
    else:
        course = directions[course][2]
        sense.set_pixel(x, y, 0,0,0)
        x = x + directions[course][0]
        y = y + directions[course][1]

    # wrap around the display
    if x > 7:
        x = 0
    if x < 0:
        x = 7
    if y > 7:
        y = 0
    if y < 0:
        y = 7

    time.sleep(0.01)

