import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math_engine import SplitComplex, Dual, Quaternion, DualQuaternion, sclerp
from mpl_toolkits.mplot3d import Axes3D

class KinematicsLab(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab 2: Transformations & Kinematics")
        self.geometry("1100x700")
        self.configure(bg="#1e1e1e")
        
        self.left_panel = tk.Frame(self, bg="#1e1e1e", width=300)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.left_panel.pack_propagate(False)
        
        tk.Label(self.left_panel, text="Hypercomplex\nGeometry", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#007acc").pack(pady=10)
        
        # 2D Geometry Section
        f_2d = tk.LabelFrame(self.left_panel, text="2D Algebra Transformation", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold"))
        f_2d.pack(fill=tk.X, pady=5)
        
        tk.Label(f_2d, text="Multiply by Z = a + b*X", bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=5, pady=2)
        row1 = tk.Frame(f_2d, bg="#1e1e1e")
        row1.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(row1, text="a:", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        self.entry_a = tk.Entry(row1, width=8)
        self.entry_a.pack(side=tk.LEFT, padx=2)
        self.entry_a.insert(0, "1.0")
        
        tk.Label(row1, text="b:", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        self.entry_b = tk.Entry(row1, width=8)
        self.entry_b.pack(side=tk.LEFT, padx=2)
        self.entry_b.insert(0, "0.5")
        
        tk.Label(f_2d, text="Algebra Type (X):", bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=5, pady=2)
        self.algebra_var = tk.StringVar(value="Complex")
        for mode in ["Complex (i²=-1)", "Dual (ε²=0)", "Split-Complex (j²=1)"]:
            tk.Radiobutton(f_2d, text=mode, variable=self.algebra_var, value=mode.split()[0], bg="#1e1e1e", fg="white", selectcolor="#2d2d30").pack(anchor=tk.W, padx=10)
            
        tk.Button(f_2d, text="Apply 2D Transform", bg="#007acc", fg="white", command=self.draw_2d).pack(fill=tk.X, padx=5, pady=5)
        
        # 3D Kinematics Section
        f_3d = tk.LabelFrame(self.left_panel, text="3D Kinematics (Dual Quat)", bg="#1e1e1e", fg="white", font=("Arial", 10, "bold"))
        f_3d.pack(fill=tk.X, pady=10)
        
        tk.Label(f_3d, text="Target Translation (x,y,z):", bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=5)
        self.entry_trans = tk.Entry(f_3d)
        self.entry_trans.pack(fill=tk.X, padx=5, pady=2)
        self.entry_trans.insert(0, "2.0, 3.0, 1.0")
        
        tk.Label(f_3d, text="Target Rotation Angle (deg):", bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=5)
        self.entry_rot = tk.Entry(f_3d)
        self.entry_rot.pack(fill=tk.X, padx=5, pady=2)
        self.entry_rot.insert(0, "90")
        
        tk.Label(f_3d, text="Interpolation t [0,1]:", bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=5)
        self.scale_t = tk.Scale(f_3d, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda val: self.draw_3d())
        self.scale_t.set(0.5)
        self.scale_t.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Button(f_3d, text="Update 3D Pose", bg="#28a745", fg="white", command=self.draw_3d).pack(fill=tk.X, padx=5, pady=5)
        
        # Right Canvas (Split into 2D and 3D)
        self.right_panel = tk.Frame(self, bg="#2d2d30")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.fig = plt.figure(figsize=(10, 5))
        self.ax2d = self.fig.add_subplot(121)
        self.ax3d = self.fig.add_subplot(122, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.draw_2d()
        self.draw_3d()

    def draw_2d(self):
        self.ax2d.clear()
        
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
        except ValueError:
            return
            
        algebra = self.algebra_var.get()
        
        # Define a square
        points = [(-1,-1), (1,-1), (1,1), (-1,1), (-1,-1)]
        orig_x, orig_y = zip(*points)
        
        trans_x, trans_y = [], []
        
        for px, py in points:
            if algebra == "Complex":
                # (px + py i)(a + b i) = (px*a - py*b) + (px*b + py*a)i
                nx = px*a - py*b
                ny = px*b + py*a
            elif algebra == "Dual":
                # (px + py e)(a + b e) = px*a + (px*b + py*a)e
                nx = px*a
                ny = px*b + py*a
            elif algebra == "Split-Complex":
                # (px + py j)(a + b j) = (px*a + py*b) + (px*b + py*a)j
                nx = px*a + py*b
                ny = px*b + py*a
            trans_x.append(nx)
            trans_y.append(ny)
            
        self.ax2d.plot(orig_x, orig_y, 'k--', label="Original Square")
        self.ax2d.plot(trans_x, trans_y, 'b-', label=f"Transformed ({algebra})", linewidth=2)
        self.ax2d.fill(trans_x, trans_y, 'b', alpha=0.3)
        
        self.ax2d.set_title(f"2D {algebra} Multiplication\nZ = {a} + {b}*X")
        self.ax2d.set_xlim(-5, 5)
        self.ax2d.set_ylim(-5, 5)
        self.ax2d.axhline(0, color='black', linewidth=0.5)
        self.ax2d.axvline(0, color='black', linewidth=0.5)
        self.ax2d.grid(True, linestyle=":", alpha=0.6)
        self.ax2d.legend()
        self.canvas.draw_idle()

    def draw_3d(self):
        self.ax3d.clear()
        
        try:
            tx, ty, tz = map(float, self.entry_trans.get().split(','))
            angle_deg = float(self.entry_rot.get())
        except Exception:
            return
            
        t = self.scale_t.get()
        
        # Start Pose (Identity)
        dq1 = DualQuaternion(Quaternion(1,0,0,0), Quaternion(0,0,0,0))
        
        # End Pose
        import math
        half_angle = math.radians(angle_deg) / 2.0
        # Rotate around Z axis for simplicity
        qr = Quaternion(math.cos(half_angle), 0, 0, math.sin(half_angle))
        dq2 = DualQuaternion.from_translation_rotation((tx, ty, tz), qr)
        
        # Interpolate
        dq_t = sclerp(dq1, dq2, t)
        trans_t, rot_t = dq_t.to_translation_rotation()
        
        def apply_rot(v, q):
            # v' = q * v * q*
            vq = Quaternion(0, v[0], v[1], v[2])
            res = q * vq * q.conjugate()
            return np.array([res.x, res.y, res.z])
            
        # Draw axes
        origin = np.array([0,0,0])
        axes = [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])]
        colors = ['red', 'green', 'blue']
        
        # Draw Start
        for ax, c in zip(axes, colors):
            self.ax3d.plot([0, ax[0]], [0, ax[1]], [0, ax[2]], color=c, alpha=0.3, linestyle="--")
            
        # Draw End
        end_origin = apply_rot(origin, qr) + np.array([tx, ty, tz])
        for ax, c in zip(axes, colors):
            end_ax = apply_rot(ax, qr) + np.array([tx, ty, tz])
            self.ax3d.plot([end_origin[0], end_ax[0]], [end_origin[1], end_ax[1]], [end_origin[2], end_ax[2]], color=c, alpha=0.3)
            
        # Draw Current Interpolated
        cur_origin = apply_rot(origin, rot_t) + np.array(trans_t)
        for ax, c in zip(axes, colors):
            cur_ax = apply_rot(ax, rot_t) + np.array(trans_t)
            self.ax3d.plot([cur_origin[0], cur_ax[0]], [cur_origin[1], cur_ax[1]], [cur_origin[2], cur_ax[2]], color=c, linewidth=2)
            
        self.ax3d.set_title(f"3D Dual Quaternion ScLERP (t={t:.2f})")
        self.ax3d.set_xlim(-2, 4)
        self.ax3d.set_ylim(-2, 4)
        self.ax3d.set_zlim(-1, 3)
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = KinematicsLab()
    app.mainloop()
