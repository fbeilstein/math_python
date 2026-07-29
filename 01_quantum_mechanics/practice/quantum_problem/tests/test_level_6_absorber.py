import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel6Absorber(unittest.TestCase):

    def setUp(self):
        self.N  = 512
        self.gf = 0.1

    def test_returns_array(self):
        mask = tasks.absorbing_mask(self.N, self.gf)
        self.assertIsInstance(mask, np.ndarray)
        self.assertEqual(len(mask), self.N)

    def test_values_in_range(self):
        mask = tasks.absorbing_mask(self.N, self.gf)
        self.assertTrue(np.all(mask >= 0) and np.all(mask <= 1),
                        "All mask values must be in [0, 1].")

    def test_edges_near_zero(self):
        mask = tasks.absorbing_mask(self.N, self.gf)
        self.assertAlmostEqual(float(mask[0]),  0.0, delta=0.01, msg="mask[0] must be ≈ 0.")
        self.assertAlmostEqual(float(mask[-1]), 0.0, delta=0.01, msg="mask[-1] must be ≈ 0.")

    def test_center_near_one(self):
        mask = tasks.absorbing_mask(self.N, self.gf)
        center_val = float(mask[self.N // 2])
        self.assertAlmostEqual(center_val, 1.0, delta=1e-6, msg="Interior must be 1.")

    def test_norm_decreases_after_mask(self):
        """After applying the mask many times, norm should decrease."""
        from numpy.fft import fftfreq
        L  = 40.0
        x  = np.linspace(-L/2, L/2, self.N, endpoint=False)
        dx = x[1] - x[0]
        k  = 2 * np.pi * fftfreq(self.N, d=dx)
        V  = np.zeros(self.N)
        mask = tasks.absorbing_mask(self.N, self.gf)
        psi  = tasks.gaussian_packet(x, 18.0, 1.0, 8.0)
        for _ in range(200):
            psi = tasks.split_operator_step(psi, k, V, 0.002)
            psi *= mask
        norm = np.sum(np.abs(psi)**2) * dx
        self.assertLess(norm, 0.95, "Absorber should decrease the norm over time.")


# ============================================================
# STANDALONE
# ============================================================

if __name__ == '__main__':
    unittest.main()
