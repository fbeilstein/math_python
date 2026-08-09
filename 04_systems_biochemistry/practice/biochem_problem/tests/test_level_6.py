import unittest
import numpy as np
import implementation_tasks as tasks

class TestLevel6Turing(unittest.TestCase):
    def test_schnakenberg_pde_rhs(self):
        N = 10
        flat_state = np.ones(2 * N)
        res = tasks.schnakenberg_pde_rhs(flat_state, 0.0, a=0.1, b=0.9, Du=1.0, Dv=20.0, dx=1.0, N=N)
        self.assertEqual(len(res), 2 * N)

    def test_analyze_turing_modes(self):
        dx = 1.0
        x = np.arange(0, 50) * dx
        spatial_u = np.sin(2 * np.pi * x / 10.0)
        k_max = tasks.analyze_turing_modes(spatial_u, dx=dx)
        self.assertAlmostEqual(k_max, 2 * np.pi / 10.0, places=2)

    def test_schnakenberg_2d_pde_rhs_flat(self):
        Nx, Ny = 10, 10
        flat_state = np.ones(2 * Nx * Ny)
        res = tasks.schnakenberg_2d_pde_rhs_flat(0.0, flat_state, a=0.1, b=0.9, Du=1.0, Dv=20.0, dx=1.0, Nx=Nx, Ny=Ny)
        self.assertEqual(len(res), 2 * Nx * Ny)

    def test_turing_dispersion_relation(self):
        k_array = np.linspace(0.1, 2.0, 5)
        sigma = tasks.turing_dispersion_relation(k_array, a=0.1, b=0.9, Du=1.0, Dv=20.0)
        self.assertEqual(len(sigma), 5)
        # Should have at least one unstable mode with these parameters
        self.assertTrue(np.max(sigma) > 0)

if __name__ == '__main__':
    unittest.main()
