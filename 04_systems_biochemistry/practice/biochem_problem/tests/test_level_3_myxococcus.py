import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel3Myxococcus(unittest.TestCase):
    def test_frz_pathway(self):
        # We just need to check the derivatives for a specific state
        state = [0.5, 0.5, 0.5]
        signal = 0.1
        
        # known parameters:
        k0 = 1.0; k1 = 4.0; k2 = 4.0
        kbar0 = 0.08 + signal # 0.18
        kbar1 = 2.0; kbar2 = 2.0
        K0=0.005; K1=0.005; K2=0.005
        Kbar0=0.01; Kbar1=0.005; Kbar2=0.005
        
        # dFrz = 1.0*(0.5)*(0.5)/(0.505) - 0.18*0.5/(0.51)
        # = 0.25/0.505 - 0.09/0.51 = 0.495049 - 0.17647 = 0.318579
        dFrz = k0*(1-0.5)*(1-0.5)/(1-0.5+K0) - kbar0*0.5/(0.5+Kbar0)
        
        # dFrzCD = 2.0*0.5/0.505 - 4.0*0.5*0.5/0.505
        # = 1/0.505 - 1/0.505 = 0
        dFrzCD = kbar1*(1-0.5)/(1-0.5+Kbar1) - k1*(1-0.5)*0.5/(0.5+K1)
        
        # dFrzE = 2.0*0.5/0.505 - 4.0*0.5*0.5/0.505 = 0
        dFrzE = kbar2*(1-0.5)/(1-0.5+Kbar2) - k2*(1-0.5)*0.5/(0.5+K2)
        
        res = tasks.frz_pathway_rhs(state, 0.0, signal)
        
        self.assertAlmostEqual(res[0], dFrz, places=4)
        self.assertAlmostEqual(res[1], dFrzCD, places=4)
        self.assertAlmostEqual(res[2], dFrzE, places=4)

if __name__ == '__main__':
    unittest.main()
