import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel2Segment(unittest.TestCase):
    
    def test_l2_segment_bounds(self):
        """Check that a point is returned only if within the [0, 1] segment bounds."""
        
        # HIT: Segment directly crosses the ray path
        p_hit = tasks.intersect_segment(np.array([0, 0]), np.array([1, 0]), np.array([5, -1]), np.array([5, 1]))
        self.assertIsInstance(p_hit, np.ndarray, "Expected output to be a numpy array for a valid hit.")
        np.testing.assert_allclose(p_hit, [5.0, 0.0], atol=1e-7)
        
        # MISS: Segment is too high, parallel to ray path
        p_miss = tasks.intersect_segment(np.array([0, 0]), np.array([1, 0]), np.array([5, 2]), np.array([5, 4]))
        self.assertIsNone(p_miss, "Expected None because the segment is out of bounds.")

if __name__ == '__main__':
    unittest.main()
