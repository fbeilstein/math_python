import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel3FreeParticle(unittest.TestCase):

    def setUp(self):
        from numpy.fft import fftfreq
        L  = 20.0
        N  = 1024
        self.x  = np.linspace(0, L, N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.k  = 2 * np.pi * fftfreq(N, d=self.dx)
        self.dt = 0.01
        self.k0 = 5.0
        self.psi0 = tasks.gaussian_packet(self.x, L / 2, 0.8, self.k0)

    def test_returns_array(self):
        psi_new = tasks.evolve_free_particle(self.psi0, self.k, self.dt)
        self.assertIsInstance(psi_new, np.ndarray)

    def test_norm_conserved(self):
        psi = self.psi0.copy()
        for _ in range(100):
            psi = tasks.evolve_free_particle(psi, self.k, self.dt)
        norm = np.sum(np.abs(psi)**2) * self.dx
        self.assertAlmostEqual(norm, 1.0, delta=1e-4,
                               msg="Free evolution must conserve norm (unitary).")

    def test_group_velocity(self):
        # After time T the peak should shift by v_g * T = (k0/m) * T
        T   = 1.0
        n_steps = int(T / self.dt)
        psi = self.psi0.copy()
        for _ in range(n_steps):
            psi = tasks.evolve_free_particle(psi, self.k, self.dt)
        peak_x = self.x[np.argmax(np.abs(psi)**2)]
        expected = self.x[np.argmax(np.abs(self.psi0)**2)] + self.k0 * T   # v_g = k0 in natural units
        self.assertAlmostEqual(peak_x, expected, delta=0.5,
                               msg="Wave packet group velocity should equal k0.")


# ============================================================
# STANDALONE
# ============================================================

if __name__ == '__main__':
    unittest.main()
