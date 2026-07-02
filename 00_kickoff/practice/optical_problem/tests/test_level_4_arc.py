import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel4Arc(unittest.TestCase):
    
    def test_l4_arc_sector(self):
        """Check if angular sector logic correctly filters circle hits."""
        center = np.array([0.0, 0.0])
        axis = np.array([-1.0, 0.0]) # Arc faces left
        cos_half = np.cos(np.radians(45)) # 90 degree total span
        
        origin = np.array([-10.0, 0.0])
        rd = np.array([1.0, 0.0])
        
        p = tasks.intersect_arc(origin, rd, center, 5.0, axis, cos_half)
        
        self.assertIsInstance(p, np.ndarray, "Should return a point for the hit on the front face.")
        np.testing.assert_allclose(p, [-5.0, 0.0], atol=1e-7)
        
        origin_back = np.array([10.0, 0.0])
        rd_back = np.array([-1.0, 0.0])
        axis_back = np.array([0.0, 1.0])
        p_miss = tasks.intersect_arc(origin_back, rd_back, center, 5.0, axis_back, cos_half)
        
        self.assertIsNone(p_miss, "Should return None if hit point is outside the angular sector.")

if __name__ == '__main__':
    unittest.main()
