import unittest
import numpy as np
import implementation_tasks as tasks

class TestLevel1QSSA(unittest.TestCase):
    def test_full_enzyme_system_rhs(self):
        state = [1.0, 0.0]
        res = tasks.full_enzyme_system_rhs(state, 0.0, k1=1.0, k_minus1=1.0, kcat=1.0, Etot=0.1)
        self.assertEqual(len(res), 2)
        self.assertAlmostEqual(res[0], -0.1)
        self.assertAlmostEqual(res[1], 0.1)

    def test_qssa_reduced_rhs(self):
        state = [1.0]
        res = tasks.qssa_reduced_rhs(state, 0.0, k1=1.0, k_minus1=1.0, kcat=1.0, Etot=0.1)
        val = res[0] if isinstance(res, (list, np.ndarray)) else res
        Km = (1.0 + 1.0) / 1.0
        expected = -(1.0 * 0.1 * 1.0) / (Km + 1.0)
        self.assertAlmostEqual(val, expected)

    def test_compute_boundary_layer_error(self):
        eps_array = np.array([0.001, 0.01, 0.1])
        errors = tasks.compute_boundary_layer_error(eps_array)
        self.assertEqual(len(errors), 3)
        self.assertTrue(errors[0] < errors[1] < errors[2])

if __name__ == '__main__':
    unittest.main()
