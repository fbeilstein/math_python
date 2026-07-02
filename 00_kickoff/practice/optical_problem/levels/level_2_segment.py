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
# STANDALONE EXECUTION
# ==========================================
if __name__ == \'__main__\':
    lvl = Level2Segment()
    lvl.draw()
    plt.show()
