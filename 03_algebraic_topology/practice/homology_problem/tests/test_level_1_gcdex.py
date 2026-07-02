import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel1GCD(unittest.TestCase):
    
    def test_l1_basic_gcd(self):
        x, y, g = tasks.z_gcdex(42, 30)
        self.assertEqual(g, 6)
        self.assertEqual(42*x + 30*y, g)

    def test_l1_coprime(self):
        x, y, g = tasks.z_gcdex(17, 23)
        self.assertEqual(g, 1)
        self.assertEqual(17*x + 23*y, g)

    def test_l1_negative_numbers(self):
        x, y, g = tasks.z_gcdex(-15, 25)
        self.assertTrue(g >= 0, "GCD must be non-negative")
        self.assertEqual(g, 5)
        self.assertEqual(-15*x + 25*y, g)

    def test_l1_zero(self):
        x, y, g = tasks.z_gcdex(10, 0)
        self.assertEqual(g, 10)
        self.assertEqual(10*x + 0*y, g)

    def test_l1_both_zero(self):
        x, y, g = tasks.z_gcdex(0, 0)
        self.assertEqual(g, 0)
        self.assertEqual(0*x + 0*y, g)

if __name__ == '__main__':
    unittest.main()
