import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from implementation_tasks import VectorizedDual, VectorizedSplit

class TestFractalsMath(unittest.TestCase):
    def test_dual_arithmetic(self):
        d1 = VectorizedDual(2, 3)
        d2 = VectorizedDual(4, 5)
        
        # Addition
        d_add = d1 + d2
        self.assertEqual(d_add.real, 6)
        self.assertEqual(d_add.dual, 8)
        
        # Subtraction
        d_sub = d1 - d2
        self.assertEqual(d_sub.real, -2)
        self.assertEqual(d_sub.dual, -2)
        
        # Multiplication (a1*a2, a1*b2 + a2*b1)
        d_mul = d1 * d2
        self.assertEqual(d_mul.real, 8)
        self.assertEqual(d_mul.dual, 2*5 + 4*3) # 10 + 12 = 22
        
        # Power
        d_pow = d1 ** 2
        self.assertEqual(d_pow.real, 4)
        self.assertEqual(d_pow.dual, 2 * 2 * 3) # 12
        
    def test_split_arithmetic(self):
        s1 = VectorizedSplit(2, 3)
        s2 = VectorizedSplit(4, 5)
        
        # Addition
        s_add = s1 + s2
        self.assertEqual(s_add.real, 6)
        self.assertEqual(s_add.j, 8)
        
        # Subtraction
        s_sub = s1 - s2
        self.assertEqual(s_sub.real, -2)
        self.assertEqual(s_sub.j, -2)
        
        # Multiplication (a1*a2 + b1*b2, a1*b2 + a2*b1)
        s_mul = s1 * s2
        self.assertEqual(s_mul.real, 2*4 + 3*5) # 8 + 15 = 23
        self.assertEqual(s_mul.j, 2*5 + 4*3) # 10 + 12 = 22
        
        # Power
        s_pow = s1 ** 2
        self.assertEqual(s_pow.real, 2**2 + 3**2) # 13
        self.assertEqual(s_pow.j, 2 * 2 * 3) # 12

if __name__ == '__main__':
    unittest.main()
