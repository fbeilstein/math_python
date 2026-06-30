import numpy as np
from matplotlib.path import Path

class LensObject:
    def __init__(self, geometry_data, x_pos=0, y_pos=0, angle=0, n=1.52):
        self.geo = geometry_data
        self.x = x_pos
        self.y = y_pos
        self.angle = angle
        self.n = n
        
        # Extract the student-friendly physics data
        self.phys = self.geo[0].get('physics', {})

    def get_transformed_points(self):
        front, back = self.geo[0], self.geo[1]
        def get_arc_pts(g, n=20):
            if g['type'] == 'line': return np.array([[g['x'], g['y_top']], [g['x'], g['y_bot']]])
            thetas = np.radians(np.linspace(g['theta1'], g['theta2'], n))
            cx, cy = g['center']
            xs = cx + g['radius'] * np.cos(thetas)
            ys = cy + g['radius'] * np.sin(thetas)
            return np.column_stack([xs, ys])

        pts_f = get_arc_pts(front); pts_f = pts_f[pts_f[:,1].argsort()[::-1]] 
        pts_b = get_arc_pts(back); pts_b = pts_b[pts_b[:,1].argsort()] 
        pts = np.vstack([pts_f, pts_b])
        theta = np.radians(self.angle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array([[c, -s], [s, c]])
        return (pts @ R.T) + [self.x, self.y]

    def contains(self, point):
        return Path(self.get_transformed_points()).contains_point(point)

    def intersects(self, other_lens):
        pts1 = self.get_transformed_points(); pts2 = other_lens.get_transformed_points()
        if (np.max(pts1[:,0]) < np.min(pts2[:,0]) or np.min(pts1[:,0]) > np.max(pts2[:,0]) or
            np.max(pts1[:,1]) < np.min(pts2[:,1]) or np.min(pts1[:,1]) > np.max(pts2[:,1])): return False
        path1 = Path(pts1); path2 = Path(pts2)
        if path1.intersects_path(path2, filled=True): return True
        if any(path2.contains_points(pts1)): return True
        if any(path1.contains_points(pts2)): return True
        if path2.contains_point(np.mean(pts1, axis=0)): return True
        if path1.contains_point(np.mean(pts2, axis=0)): return True
        return False

    def get_internal_focal_length(self):
        p = self.phys
        # Proper sign convention: R1 positive if convex, R2 negative if convex
        r1 = p['R1_abs'] if p['is_convex_front'] else -p['R1_abs']
        r2 = -p['R2_abs'] if p['is_convex_back'] else p['R2_abs']
        d, n = p['d'], self.n
        
        # Power = (n-1) * (1/r1 - 1/r2 + (n-1)*d / (n*r1*r2))
        try:
            inv_f = (n - 1) * (1/r1 - 1/r2 + ((n - 1) * d) / (n * r1 * r2))
            return 1.0 / inv_f if abs(inv_f) > 1e-9 else float('inf')
        except ZeroDivisionError:
            return float('inf')

    def get_curves(self, medium_id):
        curves = []
        theta = np.radians(self.angle); c, s = np.cos(theta), np.sin(theta)
        R_mat = np.array([[c, -s], [s, c]])
        
        def transform(p): return (np.array(p) @ R_mat.T) + [self.x, self.y]
        def rotate_vec(v): return np.array(v) @ R_mat.T

        def get_local_endpoints(part):
            if part['type'] == 'line': return [part['x'], part['y_top']], [part['x'], part['y_bot']]
            c_local = np.array(part['center']); r = part['radius']
            p1 = c_local + r * np.array([np.cos(np.radians(part['theta1'])), np.sin(np.radians(part['theta1']))])
            p2 = c_local + r * np.array([np.cos(np.radians(part['theta2'])), np.sin(np.radians(part['theta2']))])
            return (p1, p2) if p1[1] > p2[1] else (p2, p1)

        corners = []
        for part in self.geo:
            # Skip non-geometric metadata dictionary to avoid KeyError
            if 'type' not in part: 
                continue
            
            top_local, bot_local = get_local_endpoints(part)
            corners.append((transform(top_local), transform(bot_local)))

            if part['type'] == 'line':
                curves.append({'type': 'line', 'p1': transform(top_local), 'p2': transform(bot_local), 'medium_id': medium_id})
            elif part['type'] == 'arc':
                center = transform(part['center'])
                axis = rotate_vec((np.array([part['apex_x'], 0]) - np.array(part['center'])) / part['radius'])
                cos_phi = np.cos(np.radians(abs(part['theta2'] - part['theta1']) / 2.0))
                curves.append({'type': 'arc', 'center': center, 'radius': part['radius'], 'axis': axis, 'cos_half_angle': cos_phi, 'medium_id': medium_id})

        # Add top and bottom edge lines
        curves.append({'type': 'line', 'p1': corners[0][0], 'p2': corners[1][0], 'medium_id': medium_id})
        curves.append({'type': 'line', 'p1': corners[0][1], 'p2': corners[1][1], 'medium_id': medium_id})
        return curves
        
        
    def to_dict(self):
        """Returns a JSON-serializable representation of this lens."""
        return {
            "x": float(self.x),
            "y": float(self.y),
            "angle": float(self.angle),
            "n": float(self.n),
            "geo": self.geo # This contains the 'physics' dict with convex/back info
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a new LensObject instance from a dictionary."""
        # We pass n to the constructor so self.n is set correctly on load
        obj = cls(data["geo"], x_pos=data["x"], y_pos=data["y"], 
                  angle=data["angle"], n=data["n"])
        return obj
        
        
        
        
        
        
        
