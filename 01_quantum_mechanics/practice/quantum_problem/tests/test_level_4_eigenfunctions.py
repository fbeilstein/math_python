import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel4Eigenfunctions(unittest.TestCase):

    def setUp(self):
        self.L  = 10.0
        self.x  = np.linspace(0, self.L, 4096)   # include endpoints for BC check
        self.dx = self.x[1] - self.x[0]

    def test_boundary_left(self):
        for n in [1, 2, 3, 4]:
            psi = tasks.well_eigenfunction(self.x, n, self.L)
            self.assertAlmostEqual(float(psi[0]), 0.0, delta=1e-6,
                                   msg=f'psi(0) must be 0 for n={n}')

    def test_boundary_right(self):
        for n in [1, 2, 3, 4]:
            psi = tasks.well_eigenfunction(self.x, n, self.L)
            self.assertAlmostEqual(float(psi[-1]), 0.0, delta=1e-6,
                                   msg=f'psi(L) must be 0 for n={n}')

    def test_normalization(self):
        for n in [1, 2, 3]:
            psi = tasks.well_eigenfunction(self.x, n, self.L)
            norm = np.sum(psi**2) * self.dx
            self.assertAlmostEqual(norm, 1.0, delta=0.01,
                                   msg=f'n={n} eigenfunction must be normalized.')

    def test_noninteger_breaks_bc(self):
        """Non-integer n should NOT give psi(L) ≈ 0."""
        n_bad = 1.5
        psi = tasks.well_eigenfunction(self.x, n_bad, self.L)
        bc_right = abs(float(psi[-1]))
        self.assertGreater(bc_right, 0.01,
                           msg='Non-integer n should violate the right boundary condition.')

    def test_orthogonality(self):
        psi1 = tasks.well_eigenfunction(self.x, 1, self.L)
        psi2 = tasks.well_eigenfunction(self.x, 2, self.L)
        inner = np.sum(psi1 * psi2) * self.dx
        self.assertAlmostEqual(inner, 0.0, delta=0.01,
                               msg='n=1 and n=2 eigenfunctions must be orthogonal.')


# ============================================================
# STANDALONE
# ============================================================

if __name__ == '__main__':
    unittest.main()
