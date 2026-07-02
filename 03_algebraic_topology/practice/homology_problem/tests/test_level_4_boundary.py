import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel4Boundary(unittest.TestCase):
    
    def test_l4_get_complex(self):
        simplices = tasks.get_complex(["ABC"])
        self.assertIn("A", simplices)
        self.assertIn("AB", simplices)
        self.assertIn("ABC", simplices)
        self.assertEqual(len(simplices), 3 + 3 + 1) # 3 vertices, 3 edges, 1 face

    def test_l4_calculate_boundary_1(self):
        b = tasks.calculate_boundary(["AB", "BC"], ["A", "B", "C"])
        # Columns correspond to AB, BC. Rows to A, B, C.
        # AB -> -A + B
        # BC -> -B + C
        self.assertEqual(b['dim'], 3)
        self.assertIn([ -1, 0 ], b['m']) # Row A
        self.assertIn([ 1, -1 ], b['m']) # Row B
        self.assertIn([ 0, 1 ], b['m'])  # Row C

if __name__ == '__main__':
    unittest.main()
