import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from levels.base_level import BaseView

class Level6BloomCurve(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        top = tk.Frame(self, bg=self.app.bg_color)
        top.pack(fill=tk.X, pady=10)
        
        tk.Label(top, text="Elements (n):", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT)
        self.n_var = tk.IntVar(value=1000)
        self.n_lbl = tk.Label(top, text="1000", bg=self.app.bg_color, fg=self.app.accent_color, width=5)
        self.n_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.n_var, from_=100, to=5000, command=self.update_n).pack(side=tk.LEFT, padx=5)
        
        tk.Label(top, text="Filter Bits (m):", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT, padx=15)
        self.m_var = tk.IntVar(value=10000)
        self.m_lbl = tk.Label(top, text="10000", bg=self.app.bg_color, fg=self.app.accent_color, width=5)
        self.m_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.m_var, from_=1000, to=50000, command=self.update_m).pack(side=tk.LEFT, padx=5)
        
        self.fig = Figure(figsize=(5, 4), facecolor=self.app.bg_color)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.app.text_bg)
        self.ax.tick_params(colors=self.app.fg_color)
        for spine in self.ax.spines.values():
            spine.set_color(self.app.fg_color)
            
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_plot()
        
    def update_n(self, val):
        self.n_lbl.config(text=str(int(float(val))))
        self.update_plot()
        
    def update_m(self, val):
        self.m_lbl.config(text=str(int(float(val))))
        self.update_plot()
        
    def update_plot(self):
        try:
            tasks = self.get_tasks()
            n = int(float(self.n_var.get()))
            m = int(float(self.m_var.get()))
            
            k_vals = np.arange(1, 20)
            p_vals = [tasks.bloom_false_positive(n, m, k) for k in k_vals]
            
            self.ax.clear()
            self.ax.plot(k_vals, p_vals, marker='o', color=self.app.accent_color)
            
            opt_k = math.log(2) * m / n
            self.ax.axvline(x=opt_k, color="#cca700", linestyle="--", label=f"Optimal k={opt_k:.1f}")
            
            self.ax.set_title(f"Standard Bloom Filter FP Rate (n={n}, m={m})", color=self.app.fg_color)
            self.ax.set_xlabel("Number of Hash Functions (k)", color=self.app.fg_color)
            self.ax.set_ylabel("False Positive Probability", color=self.app.fg_color)
            self.ax.grid(True, color="#333333")
            self.ax.legend()
            self.canvas.draw()
        except Exception:
            pass
