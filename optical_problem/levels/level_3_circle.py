import numpy as np
import matplotlib.pyplot as plt
import unittest
import os
import sys
from matplotlib.patches import Circle

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
class Level3Circle(BaseLevel):
    def __init__(self, ax=None):
        super().__init__(ax)
        
        self.handles.update({
            'center': np.array([15.0, 0.0]), 
            'radius_h': np.array([30.0, 0.0])
        })
        # Use .copy() so we store the value, not the reference!
        self.old_center = self.handles['center'].copy()

    def draw_circle(self):
        c = self.handles['center']
        if np.any(c != self.old_center):
            self.handles['radius_h'] += c - self.old_center
            # Again, use .copy() to decouple the memory references
            self.old_center = c.copy()
            
        radius = np.linalg.norm(self.handles['radius_h'] - c)
        
        # Draw the circle surface
        self.ax.add_patch(Circle(c, radius, color="#00ffff", fill=False, lw=3, zorder=3))
        
        return c, radius

    def draw_student_output(self, point):
        super().draw_student_output(point)
        
        student_points = []
        if isinstance(point, np.ndarray):
            if point.ndim == 1: 
                student_points.append(point)
            elif point.ndim == 2: 
                student_points.extend(point)
        elif isinstance(point, (list, tuple)):
            for p in point:
                if isinstance(p, np.ndarray): 
                    student_points.append(p)

        circled_nums = ["①", "②", "③", "④"]
        r_o, ray_dir = self.get_ray()
        
        for i, pt in enumerate(student_points):
            is_ahead = np.dot(pt - r_o, ray_dir) > 1e-4
            marker_char = circled_nums[i] if i < len(circled_nums) else str(i)            
            self.ax.scatter(pt[0], pt[1], marker=f'${marker_char}$', s=250, color='blue', zorder=11)

    def draw(self):
        """Main entry point for rendering."""
        self.setup_axes()
        
        c, radius = self.draw_circle()
        r_o, ray_dir = self.get_ray()
        
        # Call the circle intersection function
        intersection_points = tasks.intersect_circle(r_o, ray_dir, c, radius)
        
        self.draw_student_output(intersection_points)
        self.draw_handles()


# ==========================================
# UNIT TESTS (Isolated)
# ==========================================
class TestLevel3Circle(unittest.TestCase):
    
    def test_l3_circle_solutions(self):
        """Should return a list of coordinate points."""
        # Ray starts at x=-10, moves right. Hits circle radius 5 at center [0,0]
        pts = tasks.intersect_circle(np.array([-10.0, 0.0]), np.array([1.0, 0.0]), np.array([0.0, 0.0]), 5.0)
        
        self.assertTrue(pts is not None, "Expected a return value, got None.")
        self.assertEqual(len(pts), 2, f"Expected 2 intersection points, got {len(pts) if pts else 0}.")
        
        x_coords = sorted([p[0] for p in pts])
        self.assertAlmostEqual(x_coords[0], -5.0, msg="First intersection point incorrect.")
        self.assertAlmostEqual(x_coords[1], 5.0, msg="Second intersection point incorrect.")


# ==========================================
# STANDALONE EXECUTION
# ==========================================
if __name__ == '__main__':
    if "--no-graphics" in sys.argv:
        sys.argv.remove("--no-graphics")
        unittest.main()
    else:
        lvl = Level3Circle()
        lvl.draw()
        plt.show()
