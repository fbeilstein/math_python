import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel5SegmentNormal(unittest.TestCase):
    
    def test_l5_segment_normal_direction(self):
        """Verify the normal is perpendicular and faces the incoming ray."""
        rd = np.array([1.0, 0.0]) # Ray moving right
        p1 = np.array([5.0, -10.0])
        p2 = np.array([5.0, 10.0]) # Vertical line at x=5
        
        n = tasks.calculate_normal_segment(rd, p1, p2)
        
        self.assertIsNotNone(n, "Normal should not be None.")
        # Normal should be [-1, 0] to face the ray coming from the left
        np.testing.assert_allclose(n, [-1.0, 0.0], atol=1e-7)
        self.assertAlmostEqual(np.linalg.norm(n), 1.0, msg="Normal must be a unit vector.")
        
        # Perpendicularity check: dot product with the line direction (p2-p1) should be 0
        line_vec = p2 - p1
        self.assertAlmostEqual(np.dot(n, line_vec), 0.0, places=7)

if __name__ == '__main__':
    unittest.main()
