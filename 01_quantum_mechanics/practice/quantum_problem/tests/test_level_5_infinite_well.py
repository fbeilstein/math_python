import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel5InfiniteWell(unittest.TestCase):

    def setUp(self):
        self.N = 512
        self.L = 10.0

    def test_returns_array(self):
        E_k = tasks.dst_energy_levels(self.N, self.L)
        self.assertIsInstance(E_k, np.ndarray)
        self.assertEqual(len(E_k), self.N)

    def test_ground_state_energy(self):
        E_k = tasks.dst_energy_levels(self.N, self.L)
        E1_expected = (np.pi / self.L)**2 / 2   # hbar=m=1
        self.assertAlmostEqual(E_k[0], E1_expected, places=6,
                               msg='Ground state energy E1 = (pi/L)^2/2 must match.')

    def test_quadratic_scaling(self):
        E_k = tasks.dst_energy_levels(self.N, self.L)
        # E_n should scale as n^2: E_k[1] / E_k[0] ≈ 4
        ratio = E_k[1] / E_k[0]
        self.assertAlmostEqual(ratio, 4.0, places=4,
                               msg='Energies must scale as n² (E2/E1 = 4).')

    def test_monotone_increasing(self):
        E_k = tasks.dst_energy_levels(self.N, self.L)
        self.assertTrue(np.all(np.diff(E_k) > 0),
                        msg='Energy levels must be strictly increasing.')


# ============================================================
# STANDALONE
# ============================================================

if __name__ == '__main__':
    unittest.main()
