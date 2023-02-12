from sense_hat import SenseHat
import time
import signal
import sys

sense = SenseHat()

def signal_handler(sig, frame):
    sense.clear()
    sense.show_message("Cncl", 0.02,(0,60,0))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print(sense.compass_raw)

north = 0
newn = round(sense.get_compass(), 1)
while True:
    if newn != north:
        print(newn)
        north = newn
    time.sleep(0.1)
    newn = round(sense.get_compass(), 1)
