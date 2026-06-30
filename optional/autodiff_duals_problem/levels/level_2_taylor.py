import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from levels.base_level import BaseLevel
from implementation_tasks import Dual

class Level2Taylor(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L2: Taylor Truncation", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=180).pack(pady=5)
        
        input_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        input_frame.pack(pady=2, fill=tk.X)
        
        tk.Label(input_frame, text="Polynomial P(x):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2)
        self.entry_p = tk.Entry(input_frame, font=("Courier", 10))
        self.entry_p.pack(fill=tk.X, padx=2, pady=1)
        self.entry_p.insert(0, "x**3 + 2*x**2")
        
        tk.Label(input_frame, text="Analytical P'(x):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=(10,0))
        self.entry_dp = tk.Entry(input_frame, font=("Courier", 10))
        self.entry_dp.pack(fill=tk.X, padx=2, pady=1)
        self.entry_dp.insert(0, "3*x**2 + 4*x")
        
        tk.Label(input_frame, text="Finite Diff step log10(h):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=(10,0))
        self.scale_h = tk.Scale(input_frame, from_=-2, to=0, resolution=0.1, orient=tk.HORIZONTAL, bg="#1e1e1e", fg="white", highlightthickness=0, command=lambda _: self.calculate())
        self.scale_h.set(-0.5) # 10^-0.5
        self.scale_h.pack(fill=tk.X, padx=2)
        
        tk.Button(self.left_panel, text="Plot Derivatives", font=("Arial", 10, "bold"), bg="#007acc", fg="white", command=self.calculate).pack(pady=10, fill=tk.X, padx=2)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.calculate()
        
    def evaluate(self, expr, x_val):
        safe_dict = {'x': x_val, 'Dual': Dual}
        return eval(expr, {"__builtins__": None}, safe_dict)

    def calculate(self):
        p_str = self.entry_p.get()
        dp_str = self.entry_dp.get()
        h = 10 ** self.scale_h.get()
        
        x_vals = np.linspace(-3, 3, 100)
        ana_y = []
        fd_y = []
        dual_y = []
        
        try:
            for x in x_vals:
                # Analytical
                ana_y.append(self.evaluate(dp_str, x))
                
                # Finite difference (P(x+h) - P(x)) / h
                pxh = self.evaluate(p_str, x + h)
                px = self.evaluate(p_str, x)
                fd_y.append((pxh - px) / h)
                
                # Dual AutoDiff P(x + 1ε)
                dx = Dual(x, 1.0)
                dres = self.evaluate(p_str, dx)
                dual_y.append(dres.dual)
        except Exception as e:
            print("Eval error:", e)
            return
            
        self.ax.clear()
        self.ax.plot(x_vals, ana_y, 'k-', label="Analytical P'(x)", linewidth=4, alpha=0.5)
        self.ax.plot(x_vals, fd_y, 'r--', label=f"Finite Diff (h={h:.3f})")
        self.ax.plot(x_vals, dual_y, 'c:', label="Dual AutoDiff (ε)", linewidth=2)
        
        self.ax.set_title(f"Derivatives of {p_str}")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw_idle()
