import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel4(unittest.TestCase):
    def test_gfpn_math(self):
        p, n = 2, 8
        poly = [1, 0, 0, 0, 1, 1, 1, 0, 1]
        exp_table, log_table = tasks.generate_gfpn_tables(p, n, poly)
        
        a = [2, 3] 
        b = [4]
        res = tasks.gfpn_poly_multiply(a, b, log_table, exp_table, p, n)
        self.assertEqual(res, [8, 12])

if __name__ == '__main__':
    unittest.main()
