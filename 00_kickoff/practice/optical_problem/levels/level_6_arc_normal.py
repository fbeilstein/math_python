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
# STANDALONE EXECUTION
# ==========================================
if __name__ == \'__main__\':
    lvl = Level6ArcNormal()
    lvl.draw()
    plt.show()
