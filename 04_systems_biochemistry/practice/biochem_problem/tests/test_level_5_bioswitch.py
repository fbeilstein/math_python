import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel5Bioswitch(unittest.TestCase):
    def test_bioswitch_integrate(self):
        S_array = np.array([0, 50, 100])
        init_state = [0.0, 0.0]
        
        res = tasks.bioswitch_integrate(S_array, init_state)
        sol_res = np.array([0.0, 2.00995049, 4.00997512])
        
        np.testing.assert_allclose(res, sol_res, atol=1e-2, err_msg="Integrated steady states do not match theory")

if __name__ == '__main__':
    unittest.main()
