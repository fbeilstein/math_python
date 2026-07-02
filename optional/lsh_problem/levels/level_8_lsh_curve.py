import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from levels.base_level import BaseView

class Level8LSHCurve(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        top = tk.Frame(self, bg=self.app.bg_color)
        top.pack(fill=tk.X, pady=10)
        
        tk.Label(top, text="Hash Functions:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT)
        self.hash_var = tk.IntVar(value=100)
        self.hash_lbl = tk.Label(top, text="100", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.hash_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.hash_var, from_=10, to=500, command=self.update_h).pack(side=tk.LEFT, padx=5)
        
        tk.Label(top, text="Bands:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT, padx=15)
        self.bands_var = tk.IntVar(value=20)
        self.bands_lbl = tk.Label(top, text="20", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.bands_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.bands_var, from_=1, to=100, command=self.update_b).pack(side=tk.LEFT, padx=5)
        
        tk.Label(top, text="Target Sim:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT, padx=15)
        self.target_var = tk.DoubleVar(value=0.6)
        self.target_lbl = tk.Label(top, text="0.60", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.target_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.target_var, from_=0.0, to=1.0, command=self.update_t).pack(side=tk.LEFT, padx=5)
        
        self.fig = Figure(figsize=(5, 4), facecolor=self.app.bg_color)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.app.text_bg)
        self.ax.tick_params(colors=self.app.fg_color)
        for spine in self.ax.spines.values():
            spine.set_color(self.app.fg_color)
            
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_plot()
        
    def update_h(self, val):
        self.hash_lbl.config(text=str(int(float(val))))
        self.update_plot()
        
    def update_b(self, val):
        self.bands_lbl.config(text=str(int(float(val))))
        self.update_plot()
        
    def update_t(self, val):
        self.target_lbl.config(text=f"{float(val):.2f}")
        self.update_plot()
        
    def update_plot(self):
        try:
            tasks = self.get_tasks()
            hashes = int(float(self.hash_var.get()))
            bands = int(float(self.bands_var.get()))
            target_j = self.target_var.get()
            
            if bands <= 0 or hashes <= 0: return
            rows = hashes / bands
            
            j_vals = np.linspace(0, 1.0, 200)
            p_vals = [tasks.collision_probability(j, bands, rows) for j in j_vals]
            threshold = tasks.calculate_threshold(bands, rows)
            
            self.ax.clear()
            self.ax.plot(j_vals, p_vals, color=self.app.accent_color, linewidth=2)
            
            j_fp = j_vals[j_vals < target_j]
            p_fp = [tasks.collision_probability(j, bands, rows) for j in j_fp]
            self.ax.fill_between(j_fp, 0, p_fp, color="#f44747", alpha=0.3, label="False Positives")
            
            j_fn = j_vals[j_vals > target_j]
            p_fn = [tasks.collision_probability(j, bands, rows) for j in j_fn]
            self.ax.fill_between(j_fn, p_fn, 1.0, color="#007acc", alpha=0.3, label="False Negatives")
            
            self.ax.axvline(x=target_j, color="#cca700", linestyle="--", label=f"Target={target_j:.2f}")
            self.ax.axvline(x=threshold, color="#ffffff", linestyle=":", label=f"50% Thresh={threshold:.2f}")
            
            self.ax.set_title("LSH S-Curve & Errors", color=self.app.fg_color)
            self.ax.set_xlabel("Jaccard Similarity", color=self.app.fg_color)
            self.ax.set_ylabel("P(Collision)", color=self.app.fg_color)
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.grid(True, color="#333333")
            self.ax.legend(loc="upper left")
            self.canvas.draw()
        except Exception:
            pass
