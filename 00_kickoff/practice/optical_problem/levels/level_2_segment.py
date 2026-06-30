import numpy as np
import matplotlib.pyplot as plt
import unittest
import os
import sys

# Simplified path appending
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from level_1_line import Level1Line 

# ==========================================
# GRAPHICS & INTERACTION CLASS
# ==========================================
class Level2Segment(Level1Line):
    def __init__(self, ax=None):
        # Clean initialization
        super().__init__(ax)

    def draw(self):
        self.setup_axes()
        p1, p2 = self.draw_segment()
        r_o, ray_dir = self.get_ray()
        
        # Use segment intersection instead of infinite line
        intersection_point = tasks.intersect_segment(r_o, ray_dir, p1, p2)
        
        self.draw_student_output(intersection_point)
        self.draw_handles()

# ==========================================
# UNIT TESTS (Isolated)
# ==========================================
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

# ==========================================
# STANDALONE EXECUTION
# ==========================================
if __name__ == '__main__':
    if "--no-graphics" in sys.argv:
        sys.argv.remove("--no-graphics")
        unittest.main()
    else:
        lvl = Level2Segment()
        lvl.draw()
        plt.show()
