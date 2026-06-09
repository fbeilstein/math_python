import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from levels.base_level import BaseLevel
from implementation_tasks import render_fractal

class Level3Video(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        tk.Label(self.left_panel, text="L3: Dragon Video", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white").pack(pady=5)
        
        tk.Label(self.left_panel, text="Algebra Type:", bg="#1e1e1e", fg="white").pack(anchor=tk.W, pady=(10, 0))
        self.algebra_var = tk.StringVar(value="Complex (i^2 = -1)")
        for mode in ["Complex (i^2 = -1)", "Dual (e^2 = 0)", "Split-Complex (j^2 = 1)"]:
            tk.Radiobutton(self.left_panel, text=mode, variable=self.algebra_var, value=mode, bg="#1e1e1e", fg="white", selectcolor="#2d2d30", command=self.update_mandelbrot).pack(anchor=tk.W, padx=10)
            
        tk.Label(self.left_panel, text="Recursive Formula:", bg="#1e1e1e", fg="white").pack(anchor=tk.W, pady=(15, 0))
        self.entry_formula = tk.Entry(self.left_panel, width=25)
        self.entry_formula.pack(fill=tk.X, padx=5, pady=2)
        self.entry_formula.insert(0, "z**2 + c")
        
        tk.Button(self.left_panel, text="Render Mandelbrot", bg="#007acc", fg="white", command=self.update_mandelbrot).pack(fill=tk.X, pady=10)
        
        tk.Label(self.left_panel, text="Video Path Mode:", font=("Arial", 10, "bold"), bg="#1e1e1e", fg="white").pack(anchor=tk.W, pady=(20,0))
        tk.Label(self.left_panel, text="Click multiple points on the\nMandelbrot set to trace a path.\nThen generate the Julia\ntransformation video.", bg="#1e1e1e", fg="#aaaaaa", justify=tk.LEFT).pack(anchor=tk.W)
        
        self.btn_clear = tk.Button(self.left_panel, text="Clear Path", bg="#d9534f", fg="white", command=self.clear_path)
        self.btn_clear.pack(fill=tk.X, pady=10)
        
        self.btn_vid = tk.Button(self.left_panel, text="Generate Dragon Video", bg="#28a745", fg="white", font=("Arial", 10, "bold"), command=self.generate_video)
        self.btn_vid.pack(fill=tk.X, pady=5)
        
        # Single canvas for Mandelbrot
        self.fig, self.ax_m = plt.subplots(figsize=(6, 6))
        self.fig.patch.set_facecolor('#2d2d30')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.path_points = []
        self.scatter = None
        self.line = None
        
        self.canvas.mpl_connect('button_press_event', self.on_click)
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
        self.ax_m.set_title(f"Mandelbrot Map ({alg})", color='white')
        self.ax_m.axis('off')
        
        self.scatter = self.ax_m.scatter([], [], color='cyan', zorder=5)
        self.line, = self.ax_m.plot([], [], color='white', zorder=4, linestyle='--')
        
        self.redraw_path()

    def on_click(self, event):
        if event.inaxes == self.ax_m:
            cx, cy = event.xdata, event.ydata
            self.path_points.append((cx, cy))
            self.redraw_path()

    def redraw_path(self):
        if not self.path_points:
            self.scatter.set_offsets(np.empty((0, 2)))
            self.line.set_data([], [])
        else:
            xs, ys = zip(*self.path_points)
            self.scatter.set_offsets(np.c_[xs, ys])
            self.line.set_data(xs, ys)
        self.canvas.draw_idle()

    def clear_path(self):
        self.path_points.clear()
        self.redraw_path()

    def generate_video(self):
        if len(self.path_points) < 2:
            messagebox.showwarning("Not Enough Points", "Please click at least 2 points on the Mandelbrot set to create a path.")
            return
            
        self.btn_vid.config(state=tk.DISABLED, text="Generating...")
        self.left_panel.update()
        
        # Interpolate points
        path_interp = []
        for i in range(len(self.path_points)-1):
            p1 = np.array(self.path_points[i])
            p2 = np.array(self.path_points[i+1])
            steps = 20
            for t in np.linspace(0, 1, steps):
                path_interp.append(p1 * (1-t) + p2 * t)
                
        alg = self.algebra_var.get()
        formula = self.entry_formula.get()
        max_iter = 30
        
        fig_vid, ax_vid = plt.subplots(figsize=(5,5))
        fig_vid.subplots_adjust(left=0, bottom=0, right=1, top=1)
        ax_vid.axis('off')
        
        # FIX: The black video bug occurs because when initializing imshow with np.zeros,
        # vmin and vmax are both calculated as 0, making all future arrays look uniformly dark.
        # By setting vmin=0 and vmax=max_iter, the colormap correctly maps the 0-30 iterations.
        im = ax_vid.imshow(
            np.zeros((200,200)), 
            cmap="magma", 
            extent=[-2, 2, -2, 2], 
            origin="lower", 
            animated=True,
            vmin=0, vmax=max_iter
        )
        
        def update_frame(frame_idx):
            cx, cy = path_interp[frame_idx]
            img = render_fractal(alg, "Julia", formula, c_val=cx + 1j * cy, width=200, height=200, max_iter=max_iter)
            im.set_array(img)
            return [im]
            
        ani = animation.FuncAnimation(fig_vid, update_frame, frames=len(path_interp), blit=True)
        vid_file = "dragon_wandering.mp4"
        ani.save(vid_file, fps=15, extra_args=['-vcodec', 'libx264'])
        plt.close(fig_vid)
        
        self.btn_vid.config(state=tk.NORMAL, text="Generate Dragon Video")
        messagebox.showinfo("Success", f"Video saved to {vid_file}!")
