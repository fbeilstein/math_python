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
from base_level import BaseLevel 

# ==========================================
# GRAPHICS & INTERACTION CLASS
# ==========================================
class Level1Line(BaseLevel):
    def __init__(self, ax=None):
        # Clean initialization without unittest baggage
        super().__init__(ax)
        self.handles.update({
            'p1': np.array([10.0, -20.0]), 
            'p2': np.array([10.0, 20.0])
        })

    def draw_segment(self):
        """Draws the infinite line based on p1 and p2."""
        p1, p2 = self.handles['p1'], self.handles['p2']
        slope = p2 - p1
        
        # Draw infinite guide
        self.ax.plot([p1[0]-100*slope[0], p1[0]+100*slope[0]], 
                     [p1[1]-100*slope[1], p1[1]+100*slope[1]], 
                     color="#ff0000", linestyle="--", alpha=0.5, lw=1)
        
        # Draw segment
        self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#00ffff", lw=3, zorder=3)
        return p1, p2

    def draw(self):
        self.setup_axes()
        p1, p2 = self.draw_segment()
        r_o, ray_dir = self.get_ray()
        
        intersection_point = tasks.intersect_line_infinite(r_o, ray_dir, p1, p2)
        
        self.draw_student_output(intersection_point)
        self.draw_handles()


# ==========================================
# STANDALONE EXECUTION
# ==========================================
if __name__ == '__main__':
    lvl = Level1Line()
    lvl.draw()
    plt.show()
