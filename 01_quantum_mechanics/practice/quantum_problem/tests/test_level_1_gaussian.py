import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel1Gaussian(unittest.TestCase):

    def setUp(self):
        self.L  = 10.0
        self.x  = np.linspace(0, self.L, 2048, endpoint=False)
        self.dx = self.x[1] - self.x[0]

    def test_returns_complex_array(self):
        psi = tasks.gaussian_packet(self.x, 5.0, 0.8, 5.0)
        self.assertIsInstance(psi, np.ndarray, "Return value must be a numpy array.")
        self.assertEqual(psi.dtype.kind, 'c', "Array must be complex.")

    def test_normalization(self):
        psi = tasks.gaussian_packet(self.x, 5.0, 0.8, 5.0)
        norm = np.sum(np.abs(psi)**2) * self.dx
        self.assertAlmostEqual(norm, 1.0, places=4, msg="Wavefunction must be normalized to 1.")

    def test_peak_at_x0(self):
        x0 = 4.0
        psi = tasks.gaussian_packet(self.x, x0, 0.5, 5.0)
        peak_idx = np.argmax(np.abs(psi)**2)
        self.assertAlmostEqual(self.x[peak_idx], x0, delta=0.1, msg="Probability peak must be at x0.")

    def test_momentum_phase(self):
        k0 = 6.0
        psi = tasks.gaussian_packet(self.x, 5.0, 0.8, k0)
        # The phase winding rate should equal k0
        phase = np.angle(psi)
        # finite diff of phase near center
        center = len(self.x) // 2
        dphi = np.diff(phase[center-5:center+5])
        dphi = (dphi + np.pi) % (2*np.pi) - np.pi  # unwrap locally
        k_measured = np.mean(dphi) / self.dx
        self.assertAlmostEqual(k_measured, k0, delta=0.3, msg="Phase gradient must equal k0.")

if __name__ == '__main__':
    unittest.main()
