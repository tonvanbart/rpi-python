from sense_hat import SenseHat
import time
import random

sense = SenseHat()
sense.clear()

G = [0,120,0]
R = [120,0,0]
x = random.randint(0,7)
y = random.randint(0,7)
redx = random.randint(0,7)
redy = random.randint(0,7)

# make redx and redy "follow" x and y
#def follow(x,y):

sense.clear()
sense.set_rotation(180) # it's on it's side in the cupboard...
sense.set_pixel(x,y,G)
sense.set_pixel(redx, redy, R)

for i in range(1000):
    direction = random.randint(1,4)
    if direction == 1:
        x = x-1
        if x<0:
            x = 1
    elif direction == 2:
        x = x+1
        if x>7:
            x = 6
    elif direction == 3:
        y = y-1
        if y<0:
            y = 1
    else:
        y = y+1
        if y>7:
            y = 6
    if redx == x:
        redx = redx-1 if redx>0 else 2
    if redy == y:
        redy = redy-1 if redy>0 else 2
    if redx - x > 3:
        redx = redx - 1
    elif x - redx > 3:
        redx = redx + 1
    if redy - y > 3:
        redy = redy - 1
    elif y - redy > 3:
        redy = redy + 1
    sense.clear()
    sense.set_pixel(x,y,G)
    sense.set_pixel(redx,redy,R)
    time.sleep(0.05)
