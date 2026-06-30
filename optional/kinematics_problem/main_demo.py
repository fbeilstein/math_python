import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os
import math

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from levels.base_level import BaseLevel
from implementation_tasks import Quaternion, DualQuaternion, sclerp

class MainDemo(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L4: ScLERP Kinematics Demo", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=200).pack(pady=5)
        
        # Target Transform Frame
        tf = tk.Frame(self.left_panel, bg="#1e1e1e")
        tf.pack(fill=tk.X, pady=2)
        tk.Label(tf, text="Target Translation:", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2)
        self.scale_tx = tk.Scale(tf, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="X", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_tx.set(2.0)
        self.scale_tx.pack(fill=tk.X, padx=2)
        self.scale_ty = tk.Scale(tf, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="Y", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_ty.set(3.0)
        self.scale_ty.pack(fill=tk.X, padx=2)
        self.scale_tz = tk.Scale(tf, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="Z", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_tz.set(1.0)
        self.scale_tz.pack(fill=tk.X, padx=2)
        
        tk.Label(tf, text="Target Rotation (Euler):", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=(5,0))
        self.scale_roll = tk.Scale(tf, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label="Roll (X)", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_roll.set(90)
        self.scale_roll.pack(fill=tk.X, padx=2)
        self.scale_pitch = tk.Scale(tf, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label="Pitch (Y)", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_pitch.set(45)
        self.scale_pitch.pack(fill=tk.X, padx=2)
        self.scale_yaw = tk.Scale(tf, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label="Yaw (Z)", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_yaw.set(0)
        self.scale_yaw.pack(fill=tk.X, padx=2)
        
        # Interpolation Mode
        tk.Label(self.left_panel, text="Interpolation Method:", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=(10,0))
        self.method_var = tk.StringVar(value="ScLERP (Dual Quat)")
        methods = ["ScLERP (Dual Quat)", "Independent (Lerp+Slerp)", "Matrix LERP (Shrinking)"]
        for m in methods:
            tk.Radiobutton(self.left_panel, text=m, variable=self.method_var, value=m, bg="#1e1e1e", fg="white", selectcolor="#2d2d30", command=self.calculate).pack(anchor=tk.W, padx=5)
            
        # Time Slider
        self.scale_t = tk.Scale(self.left_panel, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, label="Time (t)", bg="#1e1e1e", fg="#007acc", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_t.set(0.5)
        self.scale_t.pack(fill=tk.X, padx=2, pady=10)
        
        self.fig = plt.figure(figsize=(6, 5))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.calculate()
        
    def euler_to_quaternion(self, r, p, y):
        cr = math.cos(r * 0.5)
        sr = math.sin(r * 0.5)
        cp = math.cos(p * 0.5)
        sp = math.sin(p * 0.5)
        cy = math.cos(y * 0.5)
        sy = math.sin(y * 0.5)

        qw = cr * cp * cy + sr * sp * sy
        qx = sr * cp * cy - cr * sp * sy
        qy = cr * sp * cy + sr * cp * sy
        qz = cr * cp * sy - sr * sp * cy
        return Quaternion(qw, qx, qy, qz)

    def rot_matrix(self, q):
        # Quaternion to 3x3 rotation matrix
        return np.array([
            [1 - 2*q.y**2 - 2*q.z**2, 2*q.x*q.y - 2*q.z*q.w, 2*q.x*q.z + 2*q.y*q.w],
            [2*q.x*q.y + 2*q.z*q.w, 1 - 2*q.x**2 - 2*q.z**2, 2*q.y*q.z - 2*q.x*q.w],
            [2*q.x*q.z - 2*q.y*q.w, 2*q.y*q.z + 2*q.x*q.w, 1 - 2*q.x**2 - 2*q.y**2]
        ])

    def get_matrix(self, trans, q):
        M = np.eye(4)
        M[:3, :3] = self.rot_matrix(q)
        M[:3, 3] = trans
        return M

    def calculate(self):
        t = self.scale_t.get()
        method = self.method_var.get()
        
        tx, ty, tz = self.scale_tx.get(), self.scale_ty.get(), self.scale_tz.get()
        roll = math.radians(self.scale_roll.get())
        pitch = math.radians(self.scale_pitch.get())
        yaw = math.radians(self.scale_yaw.get())
        
        # Start state (Identity)
        start_t = (0, 0, 0)
        start_q = Quaternion(1, 0, 0, 0)
        dq1 = DualQuaternion.from_translation_rotation(start_t, start_q)
        
        # End state
        end_t = (tx, ty, tz)
        end_q = self.euler_to_quaternion(roll, pitch, yaw)
        dq2 = DualQuaternion.from_translation_rotation(end_t, end_q)
        
        # Interpolate
        interp_M = None
        interp_trans = (0,0,0)
        interp_rot = Quaternion(1,0,0,0)
        
        if method == "ScLERP (Dual Quat)":
            dq_t = sclerp(dq1, dq2, t)
            interp_trans, interp_rot = dq_t.to_translation_rotation()
            
        elif method == "Independent (Lerp+Slerp)":
            # Linear translation
            interp_trans = (
                start_t[0]*(1-t) + end_t[0]*t,
                start_t[1]*(1-t) + end_t[1]*t,
                start_t[2]*(1-t) + end_t[2]*t
            )
            # Slerp rotation (shortcut using shortest path)
            dot = start_q.w*end_q.w + start_q.x*end_q.x + start_q.y*end_q.y + start_q.z*end_q.z
            if dot < 0:
                end_q = Quaternion(-end_q.w, -end_q.x, -end_q.y, -end_q.z)
            q_t = Quaternion(
                start_q.w*(1-t) + end_q.w*t,
                start_q.x*(1-t) + end_q.x*t,
                start_q.y*(1-t) + end_q.y*t,
                start_q.z*(1-t) + end_q.z*t
            ).normalized()
            interp_rot = q_t
            
        elif method == "Matrix LERP (Shrinking)":
            M1 = self.get_matrix(start_t, start_q)
            M2 = self.get_matrix(end_t, end_q)
            interp_M = M1 * (1-t) + M2 * t

        pts = np.array([
            [1, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 1, 1]
        ])
        origin = np.array([0, 0, 0, 1])
        
        if interp_M is not None:
            trans_origin = interp_M @ origin
            transformed = [(interp_M @ pt)[:3] for pt in pts]
            o_x, o_y, o_z = trans_origin[:3]
        else:
            o_x, o_y, o_z = interp_trans
            rot_inv = interp_rot.conjugate()
            transformed = []
            for pt in pts:
                v = Quaternion(0, pt[0], pt[1], pt[2])
                v_rot = interp_rot * v * rot_inv
                transformed.append((v_rot.x + o_x, v_rot.y + o_y, v_rot.z + o_z))
                
        self.ax.clear()
        
        # Plot start and end ghosts
        M2 = self.get_matrix(end_t, end_q)
        end_o = M2[:3, 3]
        end_pts = [M2[:3, :3] @ pts[i][:3] + end_o for i in range(3)]
        
        for i in range(3):
            # Start
            self.ax.plot([0, pts[i][0]], [0, pts[i][1]], [0, pts[i][2]], color='k', linestyle=':', alpha=0.3)
            # End
            self.ax.plot([end_o[0], end_pts[i][0]], [end_o[1], end_pts[i][1]], [end_o[2], end_pts[i][2]], color='k', linestyle='--', alpha=0.3)
            
        colors = ['r', 'g', 'b']
        labels = ['X', 'Y', 'Z']
        
        # Plot interpolated
        for i in range(3):
            self.ax.plot([o_x, transformed[i][0]], [o_y, transformed[i][1]], [o_z, transformed[i][2]], color=colors[i], linewidth=4, label=labels[i])
            
        # Calculate and plot path of origin
        path_x, path_y, path_z = [], [], []
        M1_s = self.get_matrix(start_t, start_q)
        M2_s = self.get_matrix(end_t, end_q)
        for t_step in np.linspace(0, 1, 50):
            if method == "ScLERP (Dual Quat)":
                dq_s = sclerp(dq1, dq2, t_step)
                trans_s, _ = dq_s.to_translation_rotation()
                path_x.append(trans_s[0])
                path_y.append(trans_s[1])
                path_z.append(trans_s[2])
            elif method == "Independent (Lerp+Slerp)":
                path_x.append(start_t[0]*(1-t_step) + end_t[0]*t_step)
                path_y.append(start_t[1]*(1-t_step) + end_t[1]*t_step)
                path_z.append(start_t[2]*(1-t_step) + end_t[2]*t_step)
            elif method == "Matrix LERP (Shrinking)":
                M_s = M1_s * (1-t_step) + M2_s * t_step
                path_x.append(M_s[0, 3])
                path_y.append(M_s[1, 3])
                path_z.append(M_s[2, 3])
                
        self.ax.plot(path_x, path_y, path_z, 'm-', alpha=0.5, label="Origin Path", linewidth=2)
            
        self.ax.set_xlim([-6, 6])
        self.ax.set_ylim([-6, 6])
        self.ax.set_zlim([-6, 6])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title(f"Kinematic Interpolation: {method}\nt = {t:.2f}")
        self.ax.legend()
        
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Kinematics Main Demo (Standalone)")
    app.geometry("1000x600")
    app.configure(bg="#1e1e1e")
    
    left = tk.Frame(app, bg="#1e1e1e", width=250)
    left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    left.pack_propagate(False)
    
    right = tk.Frame(app, bg="#2d2d30")
    right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    demo = MainDemo(left, right)
    app.mainloop()
