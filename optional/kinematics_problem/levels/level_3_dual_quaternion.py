import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from levels.base_level import BaseLevel
import math
from implementation_tasks import Quaternion, DualQuaternion

class Level3DualQuaternion(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L3: 3D Dual Quaternions", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white").pack(pady=5)
        
        # Translation Frame
        tf = tk.Frame(self.left_panel, bg="#1e1e1e")
        tf.pack(fill=tk.X, pady=5)
        tk.Label(tf, text="Translation:", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=5)
        self.scale_tx = tk.Scale(tf, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="X", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_tx.pack(fill=tk.X, padx=5)
        self.scale_ty = tk.Scale(tf, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="Y", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_ty.pack(fill=tk.X, padx=5)
        self.scale_tz = tk.Scale(tf, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="Z", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_tz.pack(fill=tk.X, padx=5)
        
        # Rotation Frame
        rf = tk.Frame(self.left_panel, bg="#1e1e1e")
        rf.pack(fill=tk.X, pady=5)
        tk.Label(rf, text="Rotation (Euler):", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=5)
        self.scale_roll = tk.Scale(rf, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label="Roll (X)", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_roll.pack(fill=tk.X, padx=5)
        self.scale_pitch = tk.Scale(rf, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label="Pitch (Y)", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_pitch.pack(fill=tk.X, padx=5)
        self.scale_yaw = tk.Scale(rf, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label="Yaw (Z)", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_yaw.pack(fill=tk.X, padx=5)
        
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

    def calculate(self):
        tx, ty, tz = self.scale_tx.get(), self.scale_ty.get(), self.scale_tz.get()
        roll = math.radians(self.scale_roll.get())
        pitch = math.radians(self.scale_pitch.get())
        yaw = math.radians(self.scale_yaw.get())
        
        qr = self.euler_to_quaternion(roll, pitch, yaw)
        dq = DualQuaternion.from_translation_rotation((tx, ty, tz), qr)
        
        # Dual conjugate for transforming lines (points are encoded as 1 + ex + ey + ez)
        # However, transforming a point P(x,y,z) is easily done by extracting translation and rotation
        # or P_new = dq * P * dq*
        # We will use the translation/rotation extraction for simplicity in plotting
        trans, rot = dq.to_translation_rotation()
        
        pts = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1)
        ]
        
        transformed = []
        rot_inv = rot.conjugate()
        for pt in pts:
            v = Quaternion(0, pt[0], pt[1], pt[2])
            v_rot = rot * v * rot_inv
            transformed.append((v_rot.x + trans[0], v_rot.y + trans[1], v_rot.z + trans[2]))
            
        self.ax.clear()
        
        colors = ['r', 'g', 'b']
        labels = ['X', 'Y', 'Z']
        
        for i in range(3):
            # Original dotted
            self.ax.plot([0, pts[i][0]], [0, pts[i][1]], [0, pts[i][2]], color=colors[i], linestyle=':', alpha=0.5)
            # Transformed solid
            self.ax.plot([trans[0], transformed[i][0]], [trans[1], transformed[i][1]], [trans[2], transformed[i][2]], color=colors[i], linewidth=3, label=labels[i])
            
        self.ax.set_xlim([-6, 6])
        self.ax.set_ylim([-6, 6])
        self.ax.set_zlim([-6, 6])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        qr_str = f"Q({dq.qr.w:.2f}, {dq.qr.x:.2f}, {dq.qr.y:.2f}, {dq.qr.z:.2f})"
        qd_str = f"Q({dq.qd.w:.2f}, {dq.qd.x:.2f}, {dq.qd.y:.2f}, {dq.qd.z:.2f})"
        self.ax.set_title(f"Dual Quaternion Rigid Transform\n{qr_str} + {qd_str}e")
        self.ax.legend()
        
        self.canvas.draw_idle()
