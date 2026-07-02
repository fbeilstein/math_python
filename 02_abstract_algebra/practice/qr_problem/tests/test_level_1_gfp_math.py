import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel1(unittest.TestCase):
    def test_division_gf2(self):
        dividend = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        divisor = [1, 0, 0, 0, 1, 1, 1, 0, 1]
        q, r = tasks.gfp_poly_divide(dividend, divisor, 2)
        self.assertEqual(r, [1, 1, 1, 0, 1])

    def test_division_gf3(self):
        q, r = tasks.gfp_poly_divide([2, 0, 1], [1, 2], 3)
        self.assertEqual(q, [2, 2])
        self.assertEqual(r, [0])

if __name__ == '__main__':
    unittest.main()
