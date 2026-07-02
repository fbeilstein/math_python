import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel3Circle(unittest.TestCase):
    
    def test_l3_circle_solutions(self):
        """Should return a list of coordinate points."""
        # Ray starts at x=-10, moves right. Hits circle radius 5 at center [0,0]
        pts = tasks.intersect_circle(np.array([-10.0, 0.0]), np.array([1.0, 0.0]), np.array([0.0, 0.0]), 5.0)
        
        self.assertTrue(pts is not None, "Expected a return value, got None.")
        self.assertEqual(len(pts), 2, f"Expected 2 intersection points, got {len(pts) if pts else 0}.")
        
        x_coords = sorted([p[0] for p in pts])
        self.assertAlmostEqual(x_coords[0], -5.0, msg="First intersection point incorrect.")
        self.assertAlmostEqual(x_coords[1], 5.0, msg="Second intersection point incorrect.")

if __name__ == '__main__':
    unittest.main()
