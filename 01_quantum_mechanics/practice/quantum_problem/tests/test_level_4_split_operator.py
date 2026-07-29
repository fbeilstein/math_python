import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel4SplitOperator(unittest.TestCase):

    def setUp(self):
        from numpy.fft import fftfreq
        L  = 40.0
        N  = 512
        self.x  = np.linspace(-L/2, L/2, N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.k  = 2 * np.pi * fftfreq(N, d=self.dx)
        self.dt = 0.002
        self.V  = np.zeros(N)
        self.psi0 = tasks.gaussian_packet(self.x, -L*0.25, 1.0, 8.0)

    def test_returns_array(self):
        psi_new = tasks.split_operator_step(self.psi0, self.k, self.V, self.dt)
        self.assertIsInstance(psi_new, np.ndarray)

    def test_norm_conserved_free(self):
        """Norm conserved for V=0 (reduces to free particle)."""
        psi = self.psi0.copy()
        for _ in range(200):
            psi = tasks.split_operator_step(psi, self.k, self.V, self.dt)
        norm = np.sum(np.abs(psi)**2) * self.dx
        self.assertAlmostEqual(norm, 1.0, delta=1e-4,
                               msg="Split-operator must conserve norm for V=0.")

    def test_norm_conserved_barrier(self):
        """Norm still conserved (no absorber) when a barrier is present."""
        V = np.where(np.abs(self.x) < 0.5, 10.0, 0.0)
        psi = self.psi0.copy()
        for _ in range(200):
            psi = tasks.split_operator_step(psi, self.k, V, self.dt)
        norm = np.sum(np.abs(psi)**2) * self.dx
        self.assertAlmostEqual(norm, 1.0, delta=1e-3,
                               msg="Split-operator must conserve norm (barrier, no absorber).")


# ============================================================
# STANDALONE
# ============================================================

if __name__ == '__main__':
    unittest.main()
