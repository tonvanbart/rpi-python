#!/usr/bin/python3

from sense_hat import SenseHat
from time import sleep
import signal
import sys
import lines

sense = SenseHat()
sense.set_rotation(180)

# handle Ctrl-C
def signal_handler(sig, frame):
    sense.clear()
    sense.show_message("Cncl", 0.02,(0,60,0))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

sense.clear()

while True:
    lines.line0()
    sleep(0.2)
    sense.clear()
    lines.line90()
    sleep(0.2)
    sense.clear()
    lines.line180()
    sleep(0.2)
    sense.clear()
    lines.line270()
    sleep(0.2)
    sense.clear()
