import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel2Inhibition(unittest.TestCase):
    def test_competitive(self):
        S = np.array([1, 2, 5, 10, 20])
        Km, Vmax = 2.0, 10.0
        Ki, I = 3.0, 6.0
        
        # competitive: Km_app = Km * (1 + I/Ki) = 2.0 * 3.0 = 6.0
        v_no = Vmax * S / (Km + S)
        v_with = Vmax * S / (6.0 + S)
        
        km_calc, vmax_calc, t, Ki_calc = tasks.analyze_inhibition(S, v_no, v_with, I)
        
        self.assertAlmostEqual(km_calc, Km, places=3)
        self.assertAlmostEqual(vmax_calc, Vmax, places=3)
        self.assertEqual(t, 'competitive')
        self.assertAlmostEqual(Ki_calc, Ki, places=3)

    def test_noncompetitive(self):
        S = np.array([1, 2, 5, 10, 20])
        Km, Vmax = 2.0, 10.0
        Ki, I = 3.0, 3.0
        
        # noncomp: Vmax_app = Vmax / (1 + I/Ki) = 10.0 / 2.0 = 5.0
        v_no = Vmax * S / (Km + S)
        v_with = 5.0 * S / (Km + S)
        
        km_calc, vmax_calc, t, Ki_calc = tasks.analyze_inhibition(S, v_no, v_with, I)
        
        self.assertEqual(t, 'noncompetitive')
        self.assertAlmostEqual(Ki_calc, Ki, places=3)

    def test_uncompetitive(self):
        S = np.array([1, 2, 5, 10, 20])
        Km, Vmax = 2.0, 10.0
        Ki, I = 3.0, 3.0
        
        # uncomp: Vmax_app = 5.0, Km_app = 1.0
        v_no = Vmax * S / (Km + S)
        v_with = 5.0 * S / (1.0 + S)
        
        km_calc, vmax_calc, t, Ki_calc = tasks.analyze_inhibition(S, v_no, v_with, I)
        
        self.assertEqual(t, 'uncompetitive')
        self.assertAlmostEqual(Ki_calc, Ki, places=3)

if __name__ == '__main__':
    unittest.main()
