import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from levels.base_level import BaseLevel
from implementation_tasks import Dual, SplitComplex

class Level12D(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L1: 2D Transforms", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white").pack(pady=5)
        
        input_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="Z = a + bX", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2)
        
        row1 = tk.Frame(input_frame, bg="#1e1e1e")
        row1.pack(fill=tk.X, padx=2, pady=2)
        tk.Label(row1, text="Start Z_1:", bg="#1e1e1e", fg="white", width=10, anchor=tk.W).pack(side=tk.LEFT)
        self.entry_a1 = tk.Entry(row1, width=5)
        self.entry_a1.pack(side=tk.LEFT, padx=2)
        self.entry_a1.insert(0, "1.0")
        self.entry_b1 = tk.Entry(row1, width=5)
        self.entry_b1.pack(side=tk.LEFT, padx=2)
        self.entry_b1.insert(0, "0.0")
        
        row2 = tk.Frame(input_frame, bg="#1e1e1e")
        row2.pack(fill=tk.X, padx=2, pady=2)
        tk.Label(row2, text="End Z_2:", bg="#1e1e1e", fg="white", width=10, anchor=tk.W).pack(side=tk.LEFT)
        self.entry_a2 = tk.Entry(row2, width=5)
        self.entry_a2.pack(side=tk.LEFT, padx=2)
        self.entry_a2.insert(0, "0.0")
        self.entry_b2 = tk.Entry(row2, width=5)
        self.entry_b2.pack(side=tk.LEFT, padx=2)
        self.entry_b2.insert(0, "1.0")
        
        tk.Label(input_frame, text="Algebra (X^2 = ?):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=(10,0))
        self.alg_var = tk.StringVar(value="Complex (-1)")
        algs = ["Complex (-1)", "Dual (0)", "Split-Complex (1)"]
        for alg in algs:
            tk.Radiobutton(input_frame, text=alg, variable=self.alg_var, value=alg, bg="#1e1e1e", fg="white", selectcolor="#2d2d30", command=self.calculate).pack(anchor=tk.W, padx=10)
            
        self.scale_t = tk.Scale(self.left_panel, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, label="Time (t)", bg="#1e1e1e", fg="#007acc", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_t.set(1.0)
        self.scale_t.pack(fill=tk.X, padx=2, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Original square
        self.square = np.array([
            [1, 1],
            [-1, 1],
            [-1, -1],
            [1, -1],
            [1, 1]
        ])
        
        self.calculate()
        
    def calculate(self):
        try:
            a1 = float(self.entry_a1.get())
            b1 = float(self.entry_b1.get())
            a2 = float(self.entry_a2.get())
            b2 = float(self.entry_b2.get())
        except ValueError:
            return
            
        t = self.scale_t.get()
        a = a1 * (1 - t) + a2 * t
        b = b1 * (1 - t) + b2 * t
            
        alg = self.alg_var.get()
        transformed = []
        
        for x, y in self.square:
            if alg == "Complex (-1)":
                # (a+bi)(x+yi) = (ax - by) + (ay + bx)i
                new_x = a*x - b*y
                new_y = a*y + b*x
            elif alg == "Dual (0)":
                # (a+be)(x+ye) = ax + (ay + bx)e
                d_point = Dual(x, y)
                d_trans = Dual(a, b)
                res = d_point * d_trans
                new_x, new_y = res.real, res.dual
            elif alg == "Split-Complex (1)":
                # (a+bj)(x+yj) = (ax + by) + (ay + bx)j
                s_point = SplitComplex(x, y)
                s_trans = SplitComplex(a, b)
                res = s_point * s_trans
                new_x, new_y = res.real, res.j
                
            transformed.append([new_x, new_y])
            
        transformed = np.array(transformed)
        
        self.ax.clear()
        
        # Plot axes
        self.ax.axhline(0, color='gray', linewidth=0.5)
        self.ax.axvline(0, color='gray', linewidth=0.5)
        
        # Plot original
        self.ax.plot(self.square[:, 0], self.square[:, 1], 'k--', label="Original")
        self.ax.fill(self.square[:, 0], self.square[:, 1], 'k', alpha=0.1)
        
        # Trace corners up to current t
        if t > 0:
            s_vals = np.linspace(0, t, max(10, int(t * 100)))
            first_trace = True
            for cx, cy in self.square:
                path_x, path_y = [], []
                for s in s_vals:
                    at = a1 * (1 - s) + a2 * s
                    bt = b1 * (1 - s) + b2 * s
                    if alg == "Complex (-1)":
                        path_x.append(at*cx - bt*cy)
                        path_y.append(at*cy + bt*cx)
                    elif alg == "Dual (0)":
                        path_x.append(at*cx)
                        path_y.append(at*cy + bt*cx)
                    elif alg == "Split-Complex (1)":
                        path_x.append(at*cx + bt*cy)
                        path_y.append(at*cy + bt*cx)
                self.ax.plot(path_x, path_y, 'b-', linewidth=2, alpha=0.6, label="Trajectory" if first_trace else "")
                first_trace = False
        
        # Plot transformed
        self.ax.plot(transformed[:, 0], transformed[:, 1], 'r-', label="Current Pos", linewidth=2)
        self.ax.fill(transformed[:, 0], transformed[:, 1], 'r', alpha=0.3)
        
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_title(f"2D Transformation: {alg}\nZ(t) = {a:.2f} + {b:.2f}X")
        self.ax.legend(loc="upper right")
        self.ax.grid(True)
        self.canvas.draw_idle()
