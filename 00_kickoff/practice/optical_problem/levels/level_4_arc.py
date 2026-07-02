import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.patches import Arc, Circle

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
class Level4Arc(BaseLevel):
    def __init__(self, ax=None):
        super().__init__(ax)
        
        self.handles.update({
            'center': np.array([15.0, 0.0]),
            'arc_p1': np.array([0.0, 15.0]),   
            'arc_p2': np.array([0.0, -15.0])
        })
        self.old_center = self.handles['center'].copy()

    def draw_arc(self):
        """Draws the arc and calculates its parameters for the physics engine."""
        c = self.handles['center']
        p1 = self.handles['arc_p1']
        p2 = self.handles['arc_p2']

        # 1. Lazy sync logic for center movement
        if np.any(c != self.old_center):
            shift = c - self.old_center
            self.handles['arc_p1'] += shift
            self.handles['arc_p2'] += shift
            self.old_center = c.copy()
            # Re-read after shift
            p1, p2 = self.handles['arc_p1'], self.handles['arc_p2']

        # 2. RADIUS FIX: The actively dragged handle dictates the radius!
        dragging = getattr(self, 'dragging', None)
        
        if dragging == 'arc_p2':
            # User is dragging p2, so p2 defines the radius; snap p1 to match
            radius = np.linalg.norm(p2 - c)
            v1_raw = p1 - c
            p1_fixed = c + radius * (v1_raw / (np.linalg.norm(v1_raw) + 1e-9))
            self.handles['arc_p1'] = p1_fixed
            p1 = p1_fixed
        else:
            # Default or dragging p1: p1 defines the radius; snap p2 to match
            radius = np.linalg.norm(p1 - c)
            v2_raw = p2 - c
            p2_fixed = c + radius * (v2_raw / (np.linalg.norm(v2_raw) + 1e-9))
            self.handles['arc_p2'] = p2_fixed
            p2 = p2_fixed

        # 3. Calculate the axis and span for rendering and physics
        mid = (p1 + p2) / 2.0
        axis_vec = mid - c
        axis_norm = np.linalg.norm(axis_vec)
        
        # Handle case where p1 and p2 are exactly 180 degrees apart
        if axis_norm < 1e-7:
            axis = np.array([-(p1[1]-c[1]), p1[0]-c[0]]) 
            axis /= (np.linalg.norm(axis) + 1e-9)
        else:
            axis = axis_vec / axis_norm
        
        vec_p1 = (p1 - c) / (radius + 1e-9)
        cos_half = np.dot(vec_p1, axis)
        
        # 4. Visualization
        span_deg = np.degrees(np.arccos(np.clip(cos_half, -1, 1))) * 2
        angle_deg = np.degrees(np.arctan2(axis[1], axis[0]))
        
        # Draw background guide circle
        self.ax.add_patch(Circle(c, radius, color="#ff0000", fill=False, lw=1, ls="--", alpha=0.3))
        
        # Draw the solid Arc surface
        self.ax.add_patch(Arc(c, radius*2, radius*2, angle=angle_deg, 
                              theta1=-span_deg/2, theta2=span_deg/2, 
                              color="#00ffff", lw=4, zorder=3))
        
        return c, radius, axis, cos_half

    def draw(self):
        """Main rendering loop."""
        self.setup_axes()
        
        c, radius, axis, cos_half = self.draw_arc()
        r_o, ray_dir = self.get_ray()
        
        hit_point = tasks.intersect_arc(r_o, ray_dir, c, radius, axis, cos_half)
        
        self.draw_student_output(hit_point)
        self.draw_handles()


# ==========================================
# STANDALONE EXECUTION
# ==========================================
if __name__ == \'__main__\':
    lvl = Level4Arc()
    lvl.draw()
    plt.show()
