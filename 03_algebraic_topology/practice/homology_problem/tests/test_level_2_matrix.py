import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel2Matrix(unittest.TestCase):
    
    def test_l2_add_columns(self):
        m = [[1, 2], [3, 4]]
        tasks.add_columns(m, 0, 1, 1, 1, 0, 1) # col0 = col0 + col1, col1 = col1
        self.assertEqual(m, [[3, 2], [7, 4]])

    def test_l2_add_rows(self):
        m = [[1, 2], [3, 4]]
        tasks.add_rows(m, 0, 1, 1, 1, 0, 1) # row0 = row0 + row1, row1 = row1
        self.assertEqual(m, [[4, 6], [3, 4]])

    def test_l2_clear_column(self):
        m = [[2, 1], [3, 2], [4, 5]]
        m = tasks.clear_column(m)
        self.assertNotEqual(m[0][0], 0, "Pivot shouldn't be zeroed if it was nonzero")
        for i in range(1, len(m)):
            self.assertEqual(m[i][0], 0, f"Element m[{i}][0] was not cleared")

    def test_l2_clear_row(self):
        m = [[2, 3, 4], [1, 2, 5]]
        m = tasks.clear_row(m)
        self.assertNotEqual(m[0][0], 0, "Pivot shouldn't be zeroed if it was nonzero")
        for j in range(1, len(m[0])):
            self.assertEqual(m[0][j], 0, f"Element m[0][{j}] was not cleared")

if __name__ == '__main__':
    unittest.main()
