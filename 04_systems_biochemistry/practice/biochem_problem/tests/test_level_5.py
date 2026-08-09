import unittest
import numpy as np
import implementation_tasks as tasks

class TestLevel5Bioswitch(unittest.TestCase):
    def test_bioswitch_rhs(self):
        res = tasks.bioswitch_rhs([0.0, 0.0], 0.0, S_func=lambda t: 0.1)
        self.assertEqual(len(res), 2)

    def test_gaussian_pulse(self):
        val = tasks.gaussian_pulse(10000.0, amp=0.05, center=10000.0, width=1000.0)
        self.assertAlmostEqual(val, 0.05)

    def test_hysteresis_continuation(self):
        S_range = np.linspace(0.0, 0.5, 5)
        high_R, low_R, S_thr = tasks.hysteresis_continuation(S_range)
        self.assertEqual(len(high_R), 5)
        self.assertEqual(len(low_R), 5)

if __name__ == '__main__':
    unittest.main()
