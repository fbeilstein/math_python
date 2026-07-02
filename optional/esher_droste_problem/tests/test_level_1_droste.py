import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestDroste(unittest.TestCase):
    def test_calculate_mathematical_bounds(self):
        H, W, cx, cy, w, h = 100, 100, 50, 50, 20, 20
        c, bound_x, bound_y, S_true, Bx, By = tasks.calculate_mathematical_bounds(H, W, cx, cy, w, h)
        # cx = 50. max_w_half = min(50, 50) = 50. 
        # w/2 = 10. c_x = 50/10 = 5.
        # bound_x = 5 * 10 = 50.
        self.assertEqual(c, 5.0)
        self.assertEqual(bound_x, 50.0)
        self.assertEqual(bound_y, 50.0)
        self.assertEqual(S_true, 50.0)
        self.assertEqual(Bx, 1.0)
        self.assertEqual(By, 1.0)

    def test_denormalize(self):
        Z = np.array([1 + 1j, -1 - 1j])
        cx, cy, S_true = 50, 50, 10
        x, y = tasks.denormalize(Z, cx, cy, S_true)
        # 1 * 10 + 50 = 60
        self.assertEqual(x[0], 60.0)
        self.assertEqual(y[0], 60.0)
        self.assertEqual(x[1], 40.0)
        self.assertEqual(y[1], 40.0)

    def test_backward_step_1_normalize(self):
        H, W, S_disp = 4, 4, 2.0
        Z = tasks.backward_step_1_normalize(H, W, S_disp)
        self.assertEqual(Z.shape, (4, 4))
        # At y=0, x=0: X = (0 - 2)/2 = -1, Y = (0 - 2)/2 = -1
        self.assertAlmostEqual(np.real(Z[0, 0]), -1.0)
        self.assertAlmostEqual(np.imag(Z[0, 0]), -1.0)

    def test_backward_step_2_log_polar(self):
        W_out = np.array([0, 1j * np.pi])
        res = tasks.backward_step_2_log_polar(W_out)
        self.assertAlmostEqual(res[0], 1.0)
        self.assertAlmostEqual(np.real(res[1]), -1.0)
        self.assertAlmostEqual(np.imag(res[1]), 0.0)

    def test_backward_step_3_conformal_twist(self):
        W = np.array([1.0, 1j])
        C = 1.0 + 1j
        res = tasks.backward_step_3_conformal_twist(W, C)
        self.assertAlmostEqual(res[0], 1.0 + 1j)
        self.assertAlmostEqual(res[1], -1.0 + 1j)

    def test_backward_step_4_exponentiation(self):
        Z = np.array([np.exp(1), np.exp(1j * np.pi)])
        res = tasks.backward_step_4_exponentiation(Z)
        self.assertAlmostEqual(np.real(res[0]), 1.0)
        self.assertAlmostEqual(np.imag(res[0]), 0.0)
        self.assertAlmostEqual(np.real(res[1]), 0.0)
        self.assertAlmostEqual(np.imag(res[1]), np.pi)

if __name__ == '__main__':
    unittest.main()
