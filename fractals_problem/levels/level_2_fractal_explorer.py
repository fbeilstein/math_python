import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from levels.base_level import BaseLevel
from implementation_tasks import render_fractal

class Level2Explorer(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L2: Fractal Explorer", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white").pack(pady=5)
        
        tk.Label(self.left_panel, text="Algebra Type:", bg="#1e1e1e", fg="white").pack(anchor=tk.W, pady=(10, 0))
        self.algebra_var = tk.StringVar(value="Complex (i^2 = -1)")
        for mode in ["Complex (i^2 = -1)", "Dual (e^2 = 0)", "Split-Complex (j^2 = 1)"]:
            tk.Radiobutton(self.left_panel, text=mode, variable=self.algebra_var, value=mode, bg="#1e1e1e", fg="white", selectcolor="#2d2d30", command=self.update_mandelbrot).pack(anchor=tk.W, padx=10)
            
        tk.Label(self.left_panel, text="Recursive Formula:", bg="#1e1e1e", fg="white").pack(anchor=tk.W, pady=(15, 0))
        self.entry_formula = tk.Entry(self.left_panel, width=25)
        self.entry_formula.pack(fill=tk.X, padx=5, pady=2)
        self.entry_formula.insert(0, "z**2 + c")
        
        tk.Button(self.left_panel, text="Render Mandelbrot", bg="#007acc", fg="white", font=("Arial", 10, "bold"), command=self.update_mandelbrot).pack(fill=tk.X, pady=15)
        
        tk.Label(self.left_panel, text="Instructions:", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white").pack(anchor=tk.W)
        tk.Label(self.left_panel, text="1. Enter a valid Python formula\nusing 'z' and 'c' (e.g., z**3 - z + c).\n2. Click Render Mandelbrot.\n3. Click anywhere on the\nMandelbrot set to generate\nits corresponding Julia set.", bg="#1e1e1e", fg="#aaaaaa", justify=tk.LEFT).pack(anchor=tk.W)
        
        self.fig, (self.ax_m, self.ax_j) = plt.subplots(1, 2, figsize=(10, 5))
        self.fig.patch.set_facecolor('#2d2d30')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.canvas.mpl_connect('button_press_event', self.on_click)
        
        # Initial clear
        self.ax_m.axis('off')
        self.ax_j.axis('off')
        self.ax_j.text(0.5, 0.5, "Click Mandelbrot to\nrender Julia set", color='white', ha='center', va='center')
        
        self.update_mandelbrot()

    def update_mandelbrot(self):
        alg = self.algebra_var.get()
        formula = self.entry_formula.get()
        
        try:
            img = render_fractal(alg, "Mandelbrot", formula, width=300, height=300)
        except Exception as e:
            print(f"Error rendering Mandelbrot: {e}")
            return
            
        self.ax_m.clear()
        self.ax_m.imshow(img, cmap="inferno", extent=[-2, 2, -2, 2], origin="lower")
        self.ax_m.set_title(f"Mandelbrot ({alg})", color='white')
        self.ax_m.axis('off')
        self.canvas.draw_idle()

    def on_click(self, event):
        if event.inaxes == self.ax_m:
            cx, cy = event.xdata, event.ydata
            self.update_julia(cx, cy)

    def update_julia(self, cx, cy):
        alg = self.algebra_var.get()
        formula = self.entry_formula.get()
        c_val = cx + 1j * cy
        
        try:
            img = render_fractal(alg, "Julia", formula, c_val=c_val, width=300, height=300)
        except Exception as e:
            print(f"Error rendering Julia: {e}")
            return
            
        self.ax_j.clear()
        self.ax_j.imshow(img, cmap="magma", extent=[-2, 2, -2, 2], origin="lower")
        self.ax_j.set_title(f"Julia Dragon c=({cx:.2f}, {cy:.2f})", color='white')
        self.ax_j.axis('off')
        self.canvas.draw_idle()
