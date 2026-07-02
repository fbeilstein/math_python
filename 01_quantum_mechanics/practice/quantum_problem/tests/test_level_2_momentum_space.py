import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel2MomentumSpace(unittest.TestCase):

    def setUp(self):
        L  = 10.0
        self.x  = np.linspace(0, L, 2048, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.k0 = 5.0
        psi = tasks.gaussian_packet(self.x, L / 2, 0.8, self.k0)
        self.k, self.phi = tasks.momentum_wavefunction(psi, self.dx)

    def test_returns_two_arrays(self):
        self.assertIsInstance(self.k,   np.ndarray, "First return value must be k (numpy array).")
        self.assertIsInstance(self.phi, np.ndarray, "Second return value must be phi (numpy array).")

    def test_same_length(self):
        self.assertEqual(len(self.k), len(self.phi), "k and phi must have the same length.")

    def test_normalization(self):
        idx = np.argsort(self.k)
        dk = self.k[idx][1] - self.k[idx][0]
        norm = np.sum(np.abs(self.phi)**2) * dk
        self.assertAlmostEqual(norm, 1.0, delta=0.05,
                               msg="Momentum wavefunction must be normalized.")

    def test_peak_at_k0(self):
        peak_k = self.k[np.argmax(np.abs(self.phi)**2)]
        self.assertAlmostEqual(peak_k, self.k0, delta=0.5,
                               msg="Momentum-space peak must be near k0.")


# ============================================================
# STANDALONE
# ============================================================

if __name__ == '__main__':
    unittest.main()
