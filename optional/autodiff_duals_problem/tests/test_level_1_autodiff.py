import unittest
import math
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestAutodiff(unittest.TestCase):
    def test_addition(self):
        d1 = tasks.Dual(2, 3)
        d2 = tasks.Dual(4, 5)
        res = d1 + d2
        self.assertEqual(res.real, 6)
        self.assertEqual(res.dual, 8)
        
        res2 = d1 + 10
        self.assertEqual(res2.real, 12)
        self.assertEqual(res2.dual, 3)
        
        res3 = 10 + d1
        self.assertEqual(res3.real, 12)
        self.assertEqual(res3.dual, 3)

    def test_subtraction(self):
        d1 = tasks.Dual(5, 3)
        d2 = tasks.Dual(2, 5)
        res = d1 - d2
        self.assertEqual(res.real, 3)
        self.assertEqual(res.dual, -2)
        
        res2 = d1 - 1
        self.assertEqual(res2.real, 4)
        self.assertEqual(res2.dual, 3)
        
        res3 = 10 - d1
        self.assertEqual(res3.real, 5)
        self.assertEqual(res3.dual, -3)

    def test_multiplication(self):
        d1 = tasks.Dual(2, 3)
        d2 = tasks.Dual(4, 5)
        res = d1 * d2
        self.assertEqual(res.real, 8)
        self.assertEqual(res.dual, 22) # 2*5 + 3*4 = 22
        
        res2 = d1 * 2
        self.assertEqual(res2.real, 4)
        self.assertEqual(res2.dual, 6)
        
        res3 = 3 * d1
        self.assertEqual(res3.real, 6)
        self.assertEqual(res3.dual, 9)

    def test_division(self):
        d1 = tasks.Dual(6, 4)
        d2 = tasks.Dual(2, 3)
        # (6+4e)/(2+3e) = 6/2 + (4*2 - 6*3)/4 e = 3 + (8-18)/4 e = 3 - 2.5e
        res = d1 / d2
        self.assertEqual(res.real, 3)
        self.assertEqual(res.dual, -2.5)
        
        res2 = d1 / 2
        self.assertEqual(res2.real, 3)
        self.assertEqual(res2.dual, 2)
        
        res3 = 12 / d2
        # 12 / (2+3e) = 12/2 + (0 - 12*3)/4 = 6 - 9e
        self.assertEqual(res3.real, 6)
        self.assertEqual(res3.dual, -9)

    def test_power(self):
        d1 = tasks.Dual(3, 2)
        # (3+2e)^3 = 27 + 3*(3^2)*2 e = 27 + 54e
        res = d1 ** 3
        self.assertEqual(res.real, 27)
        self.assertEqual(res.dual, 54)

    def test_sin(self):
        x = tasks.Dual(math.pi/2, 1)
        res = tasks.sin(x)
        self.assertAlmostEqual(res.real, 1.0)
        self.assertAlmostEqual(res.dual, 0.0)

    def test_cos(self):
        x = tasks.Dual(math.pi, 2)
        res = tasks.cos(x)
        self.assertAlmostEqual(res.real, -1.0)
        self.assertAlmostEqual(res.dual, 0.0)

    def test_tan(self):
        x = tasks.Dual(math.pi/4, 2)
        res = tasks.tan(x)
        self.assertAlmostEqual(res.real, 1.0)
        # sec^2(pi/4) = 2, so 2 * 2 = 4
        self.assertAlmostEqual(res.dual, 4.0)

    def test_exp(self):
        x = tasks.Dual(1.0, 3)
        res = tasks.exp(x)
        self.assertAlmostEqual(res.real, math.e)
        self.assertAlmostEqual(res.dual, 3 * math.e)

    def test_log(self):
        x = tasks.Dual(math.e, 2)
        res = tasks.log(x)
        self.assertAlmostEqual(res.real, 1.0)
        self.assertAlmostEqual(res.dual, 2 / math.e)

if __name__ == '__main__':
    unittest.main()
