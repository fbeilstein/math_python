import unittest
import numpy as np
import implementation_tasks as tasks

class TestLevel3Slaving(unittest.TestCase):
    def test_synergetic_2d_rhs(self):
        res = tasks.synergetic_2d_rhs([1.0, 0.5], 0.0, gamma_u=0.1, gamma_v=2.0)
        self.assertEqual(len(res), 2)
        self.assertAlmostEqual(res[0], 0.1 * 1.0 - 1.0 * 0.5)
        self.assertAlmostEqual(res[1], -2.0 * 0.5 + 1.0**2)

    def test_slaved_order_parameter_rhs(self):
        res = tasks.slaved_order_parameter_rhs([1.0], 0.0, gamma_u=0.1, gamma_v=2.0)
        val = res[0] if isinstance(res, (list, np.ndarray)) else res
        expected = 0.1 * 1.0 - (1.0 / 2.0) * (1.0**3)
        self.assertAlmostEqual(val, expected)

    def test_verify_manifold_collapse(self):
        inits = [(1.0, 2.0), (0.5, 0.1)]
        dists = tasks.verify_manifold_collapse(inits, gamma_u=0.1, gamma_v=2.0)
        self.assertEqual(len(dists), 2)
        self.assertTrue(np.all(dists < 0.1))

if __name__ == '__main__':
    unittest.main()
