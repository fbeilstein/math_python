import unittest
import numpy as np
import implementation_tasks as tasks

class TestLevel4Glycolysis(unittest.TestCase):
    def test_glycolysis_rhs(self):
        res = tasks.glycolysis_rhs([10.0, 5.0], 0.0, Km=12.0, Vin=0.36, k1=0.02, kp=6.0)
        self.assertEqual(len(res), 2)
        self.assertAlmostEqual(res[0], 0.36 - 0.02 * 10.0 * 5.0)

    def test_calc_quiver_arrows(self):
        traj = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])
        arrows = tasks.calc_quiver_arrows(traj, threshold=0.5)
        self.assertTrue(arrows.shape[0] == 4)
        self.assertTrue(arrows.shape[1] > 0)

    def test_bifurcation_sweep_km(self):
        Km_range = np.array([12.0, 20.0])
        t_span = np.linspace(0.0, 600.0, 1000)
        g_max, g_min, g_fixed = tasks.bifurcation_sweep_km(Km_range, t_span=t_span)
        self.assertEqual(len(g_max), 2)
        self.assertEqual(len(g_min), 2)
        self.assertEqual(len(g_fixed), 2)

if __name__ == '__main__':
    unittest.main()
