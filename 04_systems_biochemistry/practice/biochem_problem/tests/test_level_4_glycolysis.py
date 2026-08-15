import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel4Glycolysis(unittest.TestCase):
    def test_glycolysis_rhs(self):
        state = [1.0, 2.0]
        Km = 10.0
        Vin = 0.36; k1 = 0.02; kp = 6.0
        
        dG = Vin - k1*1.0*2.0
        dATP = 2*k1*1.0*2.0 - kp*2.0/(2.0+Km)
        
        res = tasks.glycolysis_rhs(state, 0.0, Km)
        self.assertAlmostEqual(res[0], dG, places=4)
        self.assertAlmostEqual(res[1], dATP, places=4)

    def test_glycolysis_fixed_point(self):
        Km = 13.0
        Vin = 0.36; k1 = 0.02; kp = 6.0
        ATP_eq = (2*Vin*Km)/(kp - 2*Vin)
        G_eq = Vin/(k1*ATP_eq)
        
        g, a = tasks.glycolysis_fixed_point(Km)
        self.assertAlmostEqual(g, G_eq, places=4)
        self.assertAlmostEqual(a, ATP_eq, places=4)

if __name__ == '__main__':
    unittest.main()
