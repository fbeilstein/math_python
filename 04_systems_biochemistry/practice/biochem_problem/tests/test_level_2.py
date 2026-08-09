import unittest
import numpy as np
import implementation_tasks as tasks

class TestLevel2Ultrasensitivity(unittest.TestCase):
    def test_goldbeter_koshland(self):
        y_eq = tasks.goldbeter_koshland(v1=1.0, v2=1.0, K1=0.01, K2=0.01)
        self.assertAlmostEqual(y_eq, 0.5, places=3)
        
        y_high = tasks.goldbeter_koshland(v1=1.5, v2=1.0, K1=0.01, K2=0.01)
        self.assertTrue(y_high > 0.9)

    def test_frz_pathway_rhs(self):
        state = [0.1, 0.1, 0.1]
        res = tasks.frz_pathway_rhs(state, t=10.0)
        self.assertEqual(len(res), 3)

if __name__ == '__main__':
    unittest.main()
