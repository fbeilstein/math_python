import numpy as np
from ray import Ray

class ParallelRaySource:
    def __init__(self, pos):
        self.pos = pos

    def generate_rays(self):
        rays = []
        # Standard parallel grid
        for y in np.linspace(-85, 85, 50):
            rays.append(Ray(start_pos=[-250.0, y], direction=[1.0, 0.0], start_medium=0))
        return rays

class PointRaySource:
    def __init__(self, pos):
        self.pos = np.array(pos)

    def generate_rays(self, lenses):
        rays = []
        # Check if point source is submerged in a lens
        start_medium = 0
        for i, lens in enumerate(lenses):
            if lens.contains(self.pos):
                start_medium = i + 1
                break
        
        # 120 radial rays
        for angle in np.linspace(0, 2*np.pi, 120, endpoint=False):
            direction = [np.cos(angle), np.sin(angle)]
            rays.append(Ray(start_pos=self.pos, direction=direction, start_medium=start_medium))
        return rays
