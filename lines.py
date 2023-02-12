#!/usr/bin/python3

from sense_hat import SenseHat
import logging
from time import sleep
sense = SenseHat()

green = (0, 120, 0)
red = (120, 0, 0)
blue = (0, 0, 120)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger = logging.getLogger('lines')
logger.setLevel(logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)
logging.debug("created logging")

#   0 1 2 3 4 5 6
# 0 . . . . . . .
# 1 . . . . . . .
# 2 . . . . . . .
# 3 . . . . . . .
# 4 . . . . . . .
# 5 . . . . . . .
# 6 . . . . . . .
#

# direction (degrees) to points (x, y) to color; center is 3,3
__lines = { 
        0  : [(3,3),(3,2),(3,1),(3,0)],
        45 : [(3,3),(4,2),(5,1),(6,0)],
        90 : [(3,3),(4,3),(5,3),(6,3)],
        135: [(3,3),(4,4),(5,5),(6,6)],
        180: [(3,3),(3,4),(3,5),(3,6)],
        225: [(3,3),(2,4),(1,5),(0,6)],
        270: [(3,3),(2,3),(1,3),(0,3)],
        315: [(3,3),(2,2),(1,1),(0,0)]
        }

def draw_line(degrees):
    if not degrees in __lines:
        raise ValueError("unknown degrees:"+degrees)
    for coords in __lines[degrees]:
        (x, y) = coords
#        logging.debug("set_pixel", x, y)
        sense.set_pixel(x, y, green)

def test():
    for x in range(0, 360, 45):
        sense.clear()
        draw_line(x)
        sleep(0.5)

if __name__ == "__main__":
    test()
