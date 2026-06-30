import tkinter as tk
import math
import numpy as np
from scipy.stats import norm
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import implementation_tasks
from levels.level_1_ngram import Level1NGram

class Level2Statistics(Level1NGram):
    def setup_custom_ui(self):
        super().setup_custom_ui()
        
        # Matplotlib plot
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.fig.patch.set_facecolor('#1e1e1e')
        self.ax = self.fig.add_subplot(111)
        
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.update_plot()
        
    def update_custom_ui(self):
        # Update plot every 5 characters (or every 1 if total < 20) to save CPU
        if self.total < 20 or self.total % 5 == 0:
            self.update_plot()
            
    def update_plot(self):
        if not hasattr(self, 'ax'):
            return
            
        self.ax.clear()
        self.ax.set_facecolor('#1e1e1e')
        self.ax.tick_params(colors='white')
        for spine in self.ax.spines.values():
            spine.set_color('white')
            
        if self.total < 2:
            self.plot_canvas.draw()
            return
            
        mu = self.total / 2.0
        sigma = math.sqrt(self.total) / 2.0
        x = np.linspace(max(0, mu - 4*sigma), min(self.total, mu + 4*sigma), 100)
        y = norm.pdf(x, mu, sigma)
        
        self.ax.plot(x, y, color='#007acc', linewidth=2)
        self.ax.fill_between(x, y, alpha=0.2, color='#007acc')
        self.ax.axvline(self.correct, color='red', linestyle='--', linewidth=2)
        
        p_val = implementation_tasks.calculate_p_value(self.correct, self.total)
            
        p_str = f"p-value: {p_val:.2e}" if p_val < 0.01 else f"p-value: {p_val:.3f}"
        
        title_text = f"Null Hypothesis Distribution (Random Chance)\n{p_str}"
        self.ax.set_title(title_text, color='white', fontsize=14, pad=10)
        self.ax.set_xlabel("Correct Guesses", color='white')
        self.ax.set_yticks([])
        
        self.fig.tight_layout()
        self.plot_canvas.draw()
