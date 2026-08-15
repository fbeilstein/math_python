import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel6Cusp(unittest.TestCase):
    def test_cell_cycle_rhs(self):
        C = 2.0
        cyclin = 5.0
        wee1 = 3.0
        
        # Cusp normal form: dC/dt = -C^3 + wee1*C + cyclin
        dC_expected = -C**3 + wee1*C + cyclin
        
        res = tasks.cell_cycle_rhs([C], 0.0, cyclin, wee1)
        self.assertAlmostEqual(res[0], dC_expected, places=4)

if __name__ == '__main__':
    unittest.main()
