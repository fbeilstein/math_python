import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestStability(unittest.TestCase):
    def test_get_derivatives(self):
        x, z = 2.0, 3.0
        tr, det = -1.0, 2.0
        dx, dz = tasks.get_derivatives(x, z, tr, det)
        # dx = z = 3.0
        # dz = -det*x + tr*z = -2*2 + (-1)*3 = -4 - 3 = -7.0
        self.assertEqual(dx, 3.0)
        self.assertEqual(dz, -7.0)

    def test_get_lambdas(self):
        # Case 1: Real roots (disc >= 0)
        # tr = 5, det = 4 -> disc = 25 - 16 = 9
        # L = (5 +- 3)/2 -> 4, 1
        res_real = tasks.get_lambdas(5.0, 4.0)
        self.assertAlmostEqual(res_real[0], 4.0)
        self.assertAlmostEqual(res_real[1], 0.0)
        self.assertAlmostEqual(res_real[2], 1.0)
        self.assertAlmostEqual(res_real[3], 0.0)
        
        # Case 2: Complex roots (disc < 0)
        # tr = 0, det = 1 -> disc = -4
        # L = +- 1i
        res_complex = tasks.get_lambdas(0.0, 1.0)
        self.assertAlmostEqual(res_complex[0], 0.0)
        self.assertAlmostEqual(res_complex[1], 1.0)
        self.assertAlmostEqual(res_complex[2], 0.0)
        self.assertAlmostEqual(res_complex[3], -1.0)

    def test_classify_system(self):
        self.assertEqual(tasks.classify_system(0, -1), "Saddle")
        self.assertEqual(tasks.classify_system(0, 1), "Center")
        self.assertEqual(tasks.classify_system(-1, 2), "Stable Spiral")
        self.assertEqual(tasks.classify_system(1, 2), "Unstable Spiral")
        self.assertEqual(tasks.classify_system(-4, 3), "Stable Node")
        self.assertEqual(tasks.classify_system(4, 3), "Unstable Node")

if __name__ == '__main__':
    unittest.main()
