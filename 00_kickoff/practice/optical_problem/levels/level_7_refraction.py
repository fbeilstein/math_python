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
from level_5_segment_normal import Level5SegmentNormal

# ==========================================
# GRAPHICS & INTERACTION CLASS
# ==========================================
class Level7Refraction(Level5SegmentNormal):
    def __init__(self, ax=None):
        # Clean initialization, inheriting cleanly from Level5SegmentNormal
        super().__init__(ax)

    def draw(self):
        """Main rendering loop: Intersection -> Normal -> Refraction."""
        self.setup_axes()
        
        # 1. Geometry and Ray setup
        p1, p2 = self.draw_segment()
        r_o, ray_dir = self.get_ray()
        
        # 2. Get Intersection
        hit_pt = tasks.intersect_segment(r_o, ray_dir, p1, p2)
        self.draw_student_output(hit_pt)
        
        # 3. Guard: Proceed only if there's a hit in front of the origin
        if hit_pt is not None and np.dot(hit_pt - r_o, ray_dir) > 1e-4:
            
            # 4. Get Normal
            norm = tasks.calculate_normal_segment(ray_dir, p1, p2)
            
            if norm is not None:
                # --- NEW: SUBTLE LINE ALONG NORMAL ---
                # We draw a dashed line extending 300 units in both directions
                n_ext = 300
                p_start = hit_pt - norm * n_ext
                p_end = hit_pt + norm * n_ext
                self.ax.plot([p_start[0], p_end[0]], [p_start[1], p_end[1]], 
                             color="#ff0000", lw=1, ls='--', alpha=0.4, zorder=1)

                # Draw the actual normal arrow (shorter/cleaner)
                self.ax.quiver(hit_pt[0], hit_pt[1], norm[0], norm[1], 
                              color="#c586c0", scale=12, pivot='tail', zorder=11)
                
                # 5. Calculate Refraction (Student's Level 7 math)
                refr_dir = tasks.refract_vector(ray_dir, norm, 1.0, 1.5)
                
                if refr_dir is not None:
                    # Draw the refracted ray as a bright green line
                    refr_end = hit_pt + refr_dir * 40
                    self.ax.plot([hit_pt[0], refr_end[0]], [hit_pt[1], refr_end[1]], 
                                 color="#00ff00", lw=3, zorder=2, label="Refracted Ray")
        
        self.draw_handles()

# ==========================================
# UNIT TESTS (Isolated)
# ==========================================
class TestLevel7Refraction(unittest.TestCase):
    def test_l7_refraction(self):
        ray_dir = np.array([1.0, -1.0]) / np.sqrt(2) # 45 degrees
        normal = np.array([0.0, 1.0])
        new_dir = tasks.refract_vector(ray_dir, normal, 1.0, 1.5)
        self.assertIsNotNone(new_dir)
        self.assertAlmostEqual(np.linalg.norm(new_dir), 1.0)
        self.assertAlmostEqual(np.abs(new_dir[0]) / np.sin(np.pi/4), 1.0 / 1.5)


# ==========================================
# STANDALONE EXECUTION
# ==========================================
if __name__ == '__main__':
    if "--no-graphics" in sys.argv:
        sys.argv.remove("--no-graphics")
        unittest.main()
    else:
        lvl = Level7Refraction()
        lvl.draw()
        plt.show()
