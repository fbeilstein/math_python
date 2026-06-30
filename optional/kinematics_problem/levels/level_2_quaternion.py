import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from levels.base_level import BaseLevel
import math
from implementation_tasks import Quaternion

class Level2Quaternion(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L2: 3D Quaternions", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white").pack(pady=5)
        
        tk.Label(self.left_panel, text="Euler Angles (Degrees):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=5, pady=5)
        
        self.scale_roll = tk.Scale(self.left_panel, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label="Roll (X)", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_roll.pack(fill=tk.X, padx=5)
        
        self.scale_pitch = tk.Scale(self.left_panel, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label="Pitch (Y)", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_pitch.pack(fill=tk.X, padx=5)
        
        self.scale_yaw = tk.Scale(self.left_panel, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label="Yaw (Z)", bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_yaw.pack(fill=tk.X, padx=5)
        
        self.fig = plt.figure(figsize=(6, 5))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.calculate()
        
    def euler_to_quaternion(self, r, p, y):
        # r, p, y in radians
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
        roll = math.radians(self.scale_roll.get())
        pitch = math.radians(self.scale_pitch.get())
        yaw = math.radians(self.scale_yaw.get())
        
        q = self.euler_to_quaternion(roll, pitch, yaw)
        q_inv = q.conjugate() # Assuming normalized
        
        # Original frame axes
        pts = [
            (1, 0, 0), # X
            (0, 1, 0), # Y
            (0, 0, 1)  # Z
        ]
        
        transformed = []
        for pt in pts:
            v = Quaternion(0, pt[0], pt[1], pt[2])
            # q * v * q*
            v_rot = q * v * q_inv
            transformed.append((v_rot.x, v_rot.y, v_rot.z))
            
        self.ax.clear()
        
        # Plot coordinate frame
        colors = ['r', 'g', 'b']
        labels = ['X', 'Y', 'Z']
        
        for i in range(3):
            # Original dotted
            self.ax.plot([0, pts[i][0]], [0, pts[i][1]], [0, pts[i][2]], color=colors[i], linestyle=':', alpha=0.5)
            # Transformed solid
            self.ax.plot([0, transformed[i][0]], [0, transformed[i][1]], [0, transformed[i][2]], color=colors[i], linewidth=3, label=labels[i])
            
        self.ax.set_xlim([-1.5, 1.5])
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_zlim([-1.5, 1.5])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        # Extract and draw rotation axis
        sin_a = math.sqrt(q.x**2 + q.y**2 + q.z**2)
        if sin_a > 1e-5:
            ax_x, ax_y, ax_z = q.x/sin_a, q.y/sin_a, q.z/sin_a
            self.ax.plot([-1.5*ax_x, 1.5*ax_x], [-1.5*ax_y, 1.5*ax_y], [-1.5*ax_z, 1.5*ax_z], 'm--', label="Rotation Axis", alpha=0.7)
            
        q_str = f"Q({q.w:.2f}, {q.x:.2f}, {q.y:.2f}, {q.z:.2f})"
        self.ax.set_title(f"Quaternion Rotation\n{q_str}")
        self.ax.legend()
        
        self.canvas.draw_idle()
