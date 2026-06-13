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
class Level5SegmentNormal(Level1Line):
    def __init__(self, ax=None):
        # Clean initialization, inheriting cleanly from Level1Line
        super().__init__(ax)

    def draw(self):
        """Main rendering loop with Normal Vector visualization."""
        self.setup_axes()
        
        # 1. Draw Geometry
        p1, p2 = self.draw_segment()
        r_o, ray_dir = self.get_ray()
        
        # 2. Get Intersection
        hit_pt = tasks.intersect_segment(r_o, ray_dir, p1, p2)
        
        # 3. Calculate Normal
        norm = tasks.calculate_normal_segment(ray_dir, p1, p2)
        
        # 4. Visualization
        self.draw_student_output(hit_pt)
        
        # If there is a valid hit and a valid normal, draw the normal vector
        if isinstance(hit_pt, np.ndarray) and norm is not None:
            # Check if hit is in front of ray origin
            if np.dot(hit_pt - r_o, ray_dir) > 1e-4:
                # Draw the normal vector as a purple arrow (quiver)
                self.ax.quiver(hit_pt[0], hit_pt[1], norm[0], norm[1], 
                              color="#c586c0", scale=12, pivot='tail', zorder=11,
                              label="Surface Normal")
        
        self.draw_handles()

# ==========================================
# UNIT TESTS (Isolated)
# ==========================================
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

# ==========================================
# STANDALONE EXECUTION
# ==========================================
if __name__ == '__main__':
    if "--no-graphics" in sys.argv:
        sys.argv.remove("--no-graphics")
        unittest.main()
    else:
        lvl = Level5SegmentNormal()
        lvl.draw()
        plt.show()
