import numpy as np
import matplotlib.pyplot as plt
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
# STANDALONE EXECUTION
# ==========================================
if __name__ == \'__main__\':
    lvl = Level5SegmentNormal()
    lvl.draw()
    plt.show()
