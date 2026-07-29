import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel7StateSearcher(unittest.TestCase):
    def setUp(self):
        self.L = 10.0
        self.N = 512
        self.x = np.linspace(-self.L, 2*self.L, self.N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.V = np.where((self.x < 0) | (self.x > self.L), 1000.0, 0.0)

    def test_calculate_energy(self):
        # A simple plane wave exp(ikx) in flat potential
        # Choose a frequency that is perfectly periodic on the grid
        k_test = 2 * np.pi / (3 * self.L) * 10 
        V_flat = np.zeros_like(self.x)
        psi = np.exp(1j * k_test * self.x)
        psi /= np.sqrt(np.sum(np.abs(psi)**2) * self.dx)
        
        E = tasks.calculate_energy(psi, V_flat, self.dx)
        E_expected = (k_test**2) / 2.0
        self.assertAlmostEqual(E, E_expected, places=4)

    def test_imaginary_time_step(self):
        psi = np.exp(-(self.x - self.L/2)**2) + 0j
        psi /= np.sqrt(np.sum(np.abs(psi)**2) * self.dx)
        
        E_initial = tasks.calculate_energy(psi, self.V, self.dx)
        
        for _ in range(50):
            psi = tasks.imaginary_time_step(psi, self.V, self.dx, 0.01)
            
        E_final = tasks.calculate_energy(psi, self.V, self.dx)
        self.assertLess(E_final, E_initial, "Imaginary time step must decrease total expected energy.")

    def test_project_out(self):
        state1 = np.exp(-(self.x - 3)**2) + 0j
        state1 /= np.sqrt(np.sum(np.abs(state1)**2) * self.dx)
        
        state2 = np.exp(-(self.x - 7)**2) + 0j
        state2 /= np.sqrt(np.sum(np.abs(state2)**2) * self.dx)
        
        # Project state1 out of state2
        psi_new = tasks.project_out(state2, state1, self.dx)
        
        overlap = np.sum(np.conj(state1) * psi_new) * self.dx
        self.assertAlmostEqual(overlap, 0.0, places=7, msg="project_out must yield exactly zero overlap.")

if __name__ == '__main__':
    unittest.main()
