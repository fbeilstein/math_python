import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel3SNF(unittest.TestCase):
    
    def test_l3_snf_diagonal(self):
        m = [[2, 0], [0, 3]]
        invs = tasks.invariant_factors(m)
        # SNF of diag(2, 3) is diag(1, 6)
        self.assertEqual(invs, [1, 6])

    def test_l3_snf_zero(self):
        m = [[0, 0], [0, 0]]
        invs = tasks.invariant_factors(m)
        self.assertEqual(invs, [0, 0])

    def test_l3_snf_complex(self):
        m = [[2, 4, 4], [-6, 6, 12], [10, -4, -16]]
        invs = tasks.invariant_factors(m)
        self.assertEqual(invs, [2, 6, 12])

if __name__ == '__main__':
    unittest.main()
