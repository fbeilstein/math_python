import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from levels.base_level import BaseLevel
from implementation_tasks import Dual, sin, cos, tan, exp, log

class Level3Functions(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L3: Transcendental Functions", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=180).pack(pady=5)
        
        tk.Label(self.left_panel, text="Select Function:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=5, pady=5)
        
        self.func_var = tk.StringVar(value="sin(x)")
        funcs = ["sin(x)", "cos(x)", "tan(x)", "exp(x)", "log(x)"]
        for f in funcs:
            tk.Radiobutton(self.left_panel, text=f, variable=self.func_var, value=f, bg="#1e1e1e", fg="white", selectcolor="#2d2d30", command=self.calculate).pack(anchor=tk.W, padx=10)
            
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.calculate()
        
    def evaluate(self, func_name, x_val):
        if func_name == "sin(x)": return sin(x_val)
        if func_name == "cos(x)": return cos(x_val)
        if func_name == "tan(x)": return tan(x_val)
        if func_name == "exp(x)": return exp(x_val)
        if func_name == "log(x)": return log(x_val)

    def get_analytical_deriv(self, func_name, x_val):
        import math
        if func_name == "sin(x)": return math.cos(x_val)
        if func_name == "cos(x)": return -math.sin(x_val)
        if func_name == "tan(x)": return 1.0 / (math.cos(x_val)**2)
        if func_name == "exp(x)": return math.exp(x_val)
        if func_name == "log(x)": return 1.0 / x_val

    def calculate(self):
        func_name = self.func_var.get()
        
        if func_name == "log(x)":
            x_vals = np.linspace(0.1, 5, 100)
        elif func_name == "tan(x)":
            x_vals = np.linspace(-1.4, 1.4, 100)
        else:
            x_vals = np.linspace(-3, 3, 100)
            
        y_vals = []
        dual_y = []
        ana_dy = []
        
        for x in x_vals:
            # Dual evaluate
            d_x = Dual(x, 1.0)
            res = self.evaluate(func_name, d_x)
            
            y_vals.append(res.real)
            dual_y.append(res.dual)
            ana_dy.append(self.get_analytical_deriv(func_name, x))
            
        self.ax.clear()
        self.ax.plot(x_vals, y_vals, 'k-', label=f"f(x) = {func_name}")
        self.ax.plot(x_vals, ana_dy, 'r--', label="Analytical f'(x)", linewidth=4, alpha=0.5)
        self.ax.plot(x_vals, dual_y, 'c:', label="Dual AutoDiff (ε)", linewidth=2)
        
        self.ax.set_title(f"Chain Rule implementation for {func_name}")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw_idle()
