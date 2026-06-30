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
from level_4_arc import Level4Arc

# ==========================================
# GRAPHICS & INTERACTION CLASS
# ==========================================
class Level6ArcNormal(Level4Arc):
    def __init__(self, ax=None):
        # Reuse Arc handles and initialization cleanly
        super().__init__(ax)

    def draw(self):
        """Main rendering loop with Arc Normal visualization."""
        self.setup_axes()
        
        # 1. Geometry and Physics parameters from Level 4 logic
        c, radius, axis, cos_half = self.draw_arc()
        r_o, ray_dir = self.get_ray()
        
        # 2. Get Intersection
        hit_pt = tasks.intersect_arc(r_o, ray_dir, c, radius, axis, cos_half)
        
        # 3. Visualization of standard output
        self.draw_student_output(hit_pt)
        
        # 4. GUARD: Only calculate and draw normal if we have a hit
        if hit_pt is not None:
            # Calculate Normal
            norm = tasks.calculate_normal_arc(hit_pt, ray_dir, c)
            
            if norm is not None:
                # Check if hit is in front of ray origin
                if np.dot(hit_pt - r_o, ray_dir) > 1e-4:
                    # Draw purple normal arrow
                    self.ax.quiver(hit_pt[0], hit_pt[1], norm[0], norm[1], 
                                  color="#c586c0", scale=12, pivot='tail', zorder=11)
        
        self.draw_handles()

# ==========================================
# UNIT TESTS (Isolated)
# ==========================================
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
        
        
# ==========================================
# STANDALONE EXECUTION
# ==========================================
if __name__ == '__main__':
    if "--no-graphics" in sys.argv:
        sys.argv.remove("--no-graphics")
        unittest.main()
    else:
        lvl = Level6ArcNormal()
        lvl.draw()
        plt.show()
