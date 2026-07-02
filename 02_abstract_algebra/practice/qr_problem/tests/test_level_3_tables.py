import unittest
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel3(unittest.TestCase):
    def test_tables_gf4(self):
        exp_table, log_table = tasks.generate_gfpn_tables(2, 2, [1, 1, 1])
        self.assertEqual(exp_table[:3], [1, 2, 3])
        self.assertEqual(exp_table[3], 1)

if __name__ == '__main__':
    unittest.main()
