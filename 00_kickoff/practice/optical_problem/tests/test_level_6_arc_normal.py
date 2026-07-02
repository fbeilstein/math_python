import unittest
import numpy as np
import sys, os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks

class TestLevel6ArcNormal(unittest.TestCase):
    
    def test_l6_arc_normal_orientation(self):
        """Verify normal is radial AND flips correctly for both outside and inside hits."""
        center = np.array([0.0, 0.0])
        
        # -----------------------------------------------------
        # Case 1: EXTERNAL hit (Left side of circle)
        # -----------------------------------------------------
        hit_ext = np.array([-5.0, 0.0]) 
        rd_ext = np.array([1.0, 0.0])   # Ray moving right
        n_ext = tasks.calculate_normal_arc(hit_ext, rd_ext, center)
        
        self.assertIsNotNone(n_ext)
        # Raw normal is [-1, 0]. It opposes the ray [1, 0]. No flip needed.
        np.testing.assert_allclose(n_ext, [-1.0, 0.0], atol=1e-7, 
                                   err_msg="Failed on external hit. Did you flip when you shouldn't have?")
        self.assertAlmostEqual(np.linalg.norm(n_ext), 1.0)
        
        # -----------------------------------------------------
        # Case 2: INTERNAL hit (Right side of circle, trying to exit)
        # -----------------------------------------------------
        hit_int = np.array([5.0, 0.0])
        rd_int = np.array([1.0, 0.0])   # Ray still moving right, from inside the glass
        n_int = tasks.calculate_normal_arc(hit_int, rd_int, center)
        
        self.assertIsNotNone(n_int)
        # Raw outward normal is [1, 0]. The ray is [1, 0]. They point the same way!
        # The student's logic MUST catch this and flip it to face the ray.
        np.testing.assert_allclose(n_int, [-1.0, 0.0], atol=1e-7, 
                                   err_msg="Failed to flip normal on an internal hit! Did you check the dot product?")
        self.assertAlmostEqual(np.linalg.norm(n_int), 1.0)

if __name__ == '__main__':
    unittest.main()
