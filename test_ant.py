import unittest
import ant

class TestAnt(unittest.TestCase):
    def test_direction(self):
        n = ant.Direction(0, 1)
        s = ant.Direction(0, -1)
        e = ant.Direction(1, 0)
        w = ant.Direction(-1, 0)
        n.left = w; n.right = e
        w.left = s; w.right = n
        s.left = e; s.right = w
        e.left = n; e.right = s

        self.assertEqual(n, n.right.left)
        self.assertEqual(s, s.right.left)

if __name__ == '__main__':
    unittest.main()
