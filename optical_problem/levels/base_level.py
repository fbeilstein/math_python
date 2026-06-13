import numpy as np

class BaseLevel:
    def __init__(self, ax=None):
        self.handles = {
            'ray_o': np.array([-30.0, 0.0]),
            'ray_t': np.array([-10.0, 10.0])
        }
        self.dragging = None
        self.cids = []
        
        if ax is None:
            import matplotlib.pyplot as plt
            self.fig, self.ax = plt.subplots(figsize=(7, 7))
        else:
            self.ax = ax
            self.fig = ax.figure

        self.connect_events()

    def setup_axes(self):
        """Applies consistent styling to the plotting area."""
        self.ax.set_facecolor("#1e1e1e")
        self.ax.set_xlim(-60, 60)
        self.ax.set_ylim(-50, 50)
        self.ax.set_aspect('equal')
        self.ax.grid(True, color="#333333", linestyle='--')

    def connect_events(self):
        """Binds mouse events to this specific level instance."""
        self.cids.append(self.fig.canvas.mpl_connect('button_press_event', self.on_press))
        self.cids.append(self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion))
        self.cids.append(self.fig.canvas.mpl_connect('button_release_event', self.on_release))

    def disconnect_events(self):
        """Unbinds events so this level stops listening when the dashboard switches levels."""
        for cid in self.cids:
            self.fig.canvas.mpl_disconnect(cid)
        self.cids.clear()

    # --- Interaction Logic ---
    def on_press(self, event):
        if event.inaxes != self.ax or event.xdata is None: return
        for k, v in self.handles.items():
            if np.hypot(event.xdata - v[0], event.ydata - v[1]) < 4: 
                self.dragging = k
                break

    def on_motion(self, event):
        if self.dragging and event.inaxes == self.ax and event.xdata is not None:
            # Update coordinate
            self.handles[self.dragging] = np.array([event.xdata, event.ydata])
            # Redraw
            self.ax.clear()
            self.draw()
            self.fig.canvas.draw()

    def on_release(self, event):
        self.dragging = None

    # --- Utility Methods ---
    def get_ray(self):
        r_o, r_t = self.handles['ray_o'], self.handles['ray_t']
        ray_dir = (r_t - r_o) / (np.linalg.norm(r_t - r_o) + 1e-9)
        return r_o, ray_dir

    def draw_handles(self):
        for k, v in self.handles.items():
            self.ax.scatter(v[0], v[1], c="#ffff00", s=60, edgecolors='black', zorder=20)

    def draw_student_output(self, point):
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

        # 3. Draw Points
        r_o, ray_dir = self.get_ray()
        max_reach = r_o + 150 * ray_dir
        self.ax.plot([r_o[0], max_reach[0]], [r_o[1], max_reach[1]], color="#ff8c00", lw=1, ls=':', alpha=0.4, zorder=1)

        for i, pt in enumerate(student_points):
            is_ahead = np.dot(pt - r_o, ray_dir) > 1e-4
            pt_color = "#ffd700" if is_ahead else "#ff4baf" 
            self.ax.scatter(pt[0], pt[1], color=pt_color, s=80, edgecolors='white', zorder=10)
            self.ax.text(pt[0]+3, pt[1]+1, f"({pt[0]:.1f}, {pt[1]:.1f})", color="white", fontsize=8, alpha=0.6)
            if i == 0 and is_ahead:
                self.ax.plot([r_o[0], pt[0]], [r_o[1], pt[1]], color="#ff8c00", lw=2, zorder=2)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
