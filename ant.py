# Langston's ant

import sensehat

class Direction:
    def __init__(self, dx, dy, left=None, right=None):
        self.dx = dx
        self.dy = dy
        self.left = left
        self.right = right

n = Direction(0, 1)
s = Direction(0, -1)
e = Direction(1, 0)
w = Direction(-1, 0)

n.left = w; n.right = e
w.left = s; w.right = n
s.left = e; s.right = w
e.left = n; e.right = s

ant = (4,4)


