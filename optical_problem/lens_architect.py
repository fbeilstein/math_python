import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
import numpy as np

class LensArchitect(tk.Toplevel):
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)
        self.title("Lens Designer Pro")
        self.geometry("950x850")
        self.on_save = on_save_callback
        self.transient(parent)
        self.grab_set()

        # Core physical parameters
        self.width = 20.0     
        self.diameter = 40.0  
        self.sag_front = 10.0 
        self.sag_back = 10.0  
        
        self.geometry_cache = {}
        self.dragging = None
        self.d_line = None 

        # UI Layout
        self.table_frame = tk.Frame(self, bg="#f5f5f5", bd=1, relief=tk.GROOVE)
        self.table_frame.pack(side=tk.TOP, fill=tk.X, padx=15, pady=15)
        self.setup_table()

        self.fig = Figure(figsize=(6, 5), facecolor="white")
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self, bg="#f0f0f0", pady=10)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(btn_frame, text="Add to Bench", bg="#007acc", fg="white", 
                  font=("Arial", 10, "bold"), command=self.finish, width=15).pack(side=tk.RIGHT, padx=20)

        self.ax.set_xlim(-60, 60); self.ax.set_ylim(-50, 50); self.ax.set_aspect('equal')
        self.ax.grid(True, color="#eee", linestyle='-')
        
        self.lens_poly = Polygon([[0,0]], closed=True, facecolor='cyan', edgecolor='#0078d7', alpha=0.3, lw=2)
        self.ax.add_patch(self.lens_poly)
        
        self.h_front, = self.ax.plot([], [], 'ro', markersize=10, picker=12)
        self.h_back, = self.ax.plot([], [], 'bo', markersize=10, picker=12)
        self.h_size, = self.ax.plot([], [], 's', color='orange', markersize=10, picker=12)

        self.canvas.mpl_connect('pick_event', self.on_pick)
        self.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        
        self.update_visuals()

    def setup_table(self):
        cols = ["Surface", "Abs Radius", "Signed Radius", "Sagitta", "Center (d)"]
        for i, c in enumerate(cols):
            tk.Label(self.table_frame, text=c, font=("Arial", 9, "bold"), bg="#e0e0e0", width=14, pady=5).grid(row=0, column=i, sticky="nsew")
        
        self.cells = {}
        for r_idx in [1, 2]:
            label = "Front (S1)" if r_idx == 1 else "Back (S2)"
            tk.Label(self.table_frame, text=label, bg="white", pady=3).grid(row=r_idx, column=0, sticky="nsew")
            for c_idx in range(1, 5):
                lbl = tk.Label(self.table_frame, text="--", bg="white")
                lbl.grid(row=r_idx, column=c_idx, sticky="nsew")
                self.cells[(r_idx, c_idx)] = lbl

    def calculate_arc(self, sagitta, aperture, is_left_side):
        h = aperture / 2.0; s = sagitta
        base_x = -self.width/2 if is_left_side else self.width/2
        if abs(s) < 0.2: # Snapping threshold for plano-surface
            return {'type': 'line', 'x': base_x, 'y_top': h, 'y_bot': -h, 'signed_R': float('inf'), 'sag': 0.0}
        
        R_signed = (s**2 + h**2) / (2 * s)
        R = abs(R_signed); direction = -1 if is_left_side else 1 
        apex_x = base_x + (direction * s); center_x = apex_x - (direction * R_signed)
        alpha = np.degrees(np.arcsin(min(1.0, h / R)))
        angle_to_apex = 0 if (apex_x > center_x) else 180
        return {'type': 'arc', 'center': (center_x, 0), 'radius': R, 'theta1': angle_to_apex - alpha, 
                'theta2': angle_to_apex + alpha, 'apex_x': apex_x, 'signed_R': R_signed * direction, 'sag': s}

    def update_visuals(self):
        # Physical Clamping to prevent semi-circles/infinity loops
        max_phys_sag = (self.diameter / 2.0) * 0.95
        self.sag_front = np.clip(self.sag_front, -max_phys_sag, max_phys_sag)
        self.sag_back = np.clip(self.sag_back, -max_phys_sag, max_phys_sag)

        # Intersection Guard: min thickness 1.0mm
        min_thick = 1.0
        if (self.width + self.sag_front + self.sag_back) < min_thick:
            adj = (min_thick - (self.width + self.sag_front + self.sag_back)) / 2
            self.sag_front -= adj; self.sag_back -= adj

        front = self.calculate_arc(self.sag_front, self.diameter, True)
        back = self.calculate_arc(self.sag_back, self.diameter, False)
        self.geometry_cache = {'front': front, 'back': back}
        actual_d = self.width + self.sag_front + self.sag_back

        def get_pts(geo, top_to_bot=True):
            if geo['type'] == 'line': 
                pts = np.array([[geo['x'], geo['y_top']], [geo['x'], geo['y_bot']]])
            else:
                alpha = np.degrees(np.arcsin(min(0.99, (self.diameter/2) / geo['radius'])))
                ang = 0 if (geo['apex_x'] > geo['center'][0]) else 180
                thetas = np.radians(np.linspace(ang - alpha, ang + alpha, 40))
                pts = np.column_stack([geo['center'][0] + geo['radius'] * np.cos(thetas), 
                                      geo['center'][1] + geo['radius'] * np.sin(thetas)])
            pts = pts[pts[:, 1].argsort()[::-1]]
            return pts if top_to_bot else pts[::-1]

        self.lens_poly.set_xy(np.vstack([get_pts(front), get_pts(back, False)]))

        fx = front['x'] if front['type'] == 'line' else front['apex_x']
        bx = back['x'] if back['type'] == 'line' else back['apex_x']
        if self.d_line: self.d_line[0].remove()
        self.d_line = self.ax.plot([fx, bx], [0, 0], color='magenta', lw=2, marker='|', markersize=10)

        self.h_front.set_data([fx], [0]); self.h_back.set_data([bx], [0])
        self.h_size.set_data([self.width/2], [self.diameter/2]) 

        # Table update
        r1_a, r2_a = abs(front['signed_R']), abs(back['signed_R'])
        r1_s = r1_a if self.sag_front >= 0 else -r1_a
        r2_s = -r2_a if self.sag_back >= 0 else r2_a
        
        self.cells[(1,1)].config(text=f"{r1_a:.1f}" if front['type']=='arc' else "inf")
        self.cells[(2,1)].config(text=f"{r2_a:.1f}" if back['type']=='arc' else "inf")
        self.cells[(1,2)].config(text=f"{r1_s:.1f}" if not np.isinf(r1_s) else "inf", fg="blue")
        self.cells[(2,2)].config(text=f"{r2_s:.1f}" if not np.isinf(r2_s) else "inf", fg="blue")
        self.cells[(1,3)].config(text=f"{self.sag_front:.1f}"); self.cells[(2,3)].config(text=f"{self.sag_back:.1f}")
        for r in [1,2]: self.cells[(r,4)].config(text=f"{actual_d:.1f}", fg="magenta")
        self.canvas.draw()

    def on_pick(self, event): self.dragging = event.artist
    def on_release(self, event): self.dragging = None

    def on_drag(self, event):
        if not self.dragging or event.xdata is None: return
        x, y = event.xdata, event.ydata
        temp_sf, temp_sb = self.sag_front, self.sag_back
        temp_w, temp_h = self.width, self.diameter
        max_s = (temp_h / 2.0) * 0.95

        if self.dragging == self.h_front:
            prop = (-temp_w / 2) - x
            temp_sf = 0.0 if abs(prop) < 1.5 else np.clip(prop, -max_s, max_s)
        elif self.dragging == self.h_back:
            prop = x - (temp_w / 2)
            temp_sb = 0.0 if abs(prop) < 1.5 else np.clip(prop, -max_s, max_s)
        elif self.dragging == self.h_size:
            temp_w, temp_h = max(4, abs(x)*2), max(4, abs(y)*2)

        if (temp_w + temp_sf + temp_sb) >= 1.0:
            self.sag_front, self.sag_back = temp_sf, temp_sb
            self.width, self.diameter = temp_w, temp_h
        self.update_visuals()

    def finish(self):
        f, b = self.geometry_cache['front'], self.geometry_cache['back']
        f['physics'] = {
            'R1_abs': abs(f['signed_R']), 'R2_abs': abs(b['signed_R']),
            'd': max(0.5, self.width + self.sag_front + self.sag_back),
            'is_convex_front': self.sag_front >= 0, 'is_convex_back': self.sag_back >= 0,
            'is_slab': (abs(self.sag_front) < 0.2 and abs(self.sag_back) < 0.2)
        }
        if self.on_save: self.on_save([f, b])
        self.destroy()
