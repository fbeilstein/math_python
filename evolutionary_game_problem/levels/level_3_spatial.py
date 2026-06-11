import tkinter as tk
from tkinter import ttk
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import implementation_tasks as tasks
from levels.base_level import BaseLevel
import matplotlib.colors as mcolors

class Level3Spatial(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.setup_graph_ui()
        self.add_warning()
        
        self.strategies = {cls.__name__: cls for cls in tasks.BaseStrategy.__subclasses__()}
        strat_names = list(self.strategies.keys())
        
        colors_pool = [
            '#0000FF', '#FF0000', '#00FF00', '#FFFF00', '#FF00FF', '#00FFFF',
            '#FFA500', '#800080', '#008000', '#000080', '#800000', '#008080'
        ]
        self.strat_colors = {}
        for i, name in enumerate(strat_names):
            self.strat_colors[name] = colors_pool[i % len(colors_pool)]
            
        if 'AlwaysCooperate' in self.strat_colors: self.strat_colors['AlwaysCooperate'] = '#0000FF'
        if 'AlwaysDefect' in self.strat_colors: self.strat_colors['AlwaysDefect'] = '#FF0000'
        
        self.grid = None
        self.generation = 0
        self.matrix = None
        
        tk.Label(self.left_panel, text="Spatial Evolution", bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.left_panel, text="Grid Size (N):", bg="#1e1e1e", fg="white").pack(anchor="w")
        self.entry_N = tk.Entry(self.left_panel)
        self.entry_N.insert(0, "50")
        self.entry_N.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.left_panel, text="Initial Grid Filler:", bg="#1e1e1e", fg="white").pack(anchor="w")
        self.init_var = tk.StringVar(value="Random")
        self.init_combo = ttk.Combobox(self.left_panel, textvariable=self.init_var, values=["Random"] + strat_names, state="readonly")
        self.init_combo.pack(fill=tk.X, pady=(0, 10))
        
        matrix_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        matrix_frame.pack(fill=tk.X, pady=10)
        
        self.build_matrix_ui(matrix_frame, T_def="1.9", R_def="1", P_def="0", S_def="0")
        
        self.paint_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        self.paint_frame.pack(fill=tk.X, pady=5)
        self.paint_var = tk.StringVar()
        self.rebuild_paint_controls()
        
        tk.Button(self.left_panel, text="Initialize Grid", command=self.init_grid).pack(fill=tk.X, pady=(20, 5))
        tk.Button(self.left_panel, text="Step 1 Gen", command=self.step).pack(fill=tk.X, pady=5)
        
        self.play_button = tk.Button(self.left_panel, text="Play", command=self.toggle_play, bg="#2e5c2e", fg="white")
        self.play_button.pack(fill=tk.X, pady=5)
        
        self.is_playing = False
        
        # Connect click event to canvas
        self.canvas.mpl_connect('button_press_event', self.on_click)
        
    def toggle_play(self):
        if self.grid is None:
            self.show_warning("Please initialize grid first.")
            return
            
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_button.config(text="Pause", bg="#8c2e2e")
            self.auto_step()
        else:
            self.play_button.config(text="Play", bg="#2e5c2e")
            
    def auto_step(self):
        if self.is_playing:
            self.step()
            self.controls_parent.after(1000, self.auto_step)
            
    def rebuild_paint_controls(self):
        for widget in self.paint_frame.winfo_children():
            widget.destroy()
            
        tk.Label(self.paint_frame, text="Paint Brush:", bg="#1e1e1e", fg="white").pack(anchor="w")
        strat_names = list(self.strategies.keys())
        
        if strat_names and not self.paint_var.get() in strat_names:
            self.paint_var.set(strat_names[0])
            
        for name in strat_names:
            tk.Radiobutton(self.paint_frame, text=name, variable=self.paint_var, value=name, bg="#1e1e1e", fg="white", selectcolor="#3d3d40").pack(anchor="w")
            
    def on_click(self, event):
        if self.grid is None or event.inaxes != self.ax:
            return
            
        if event.xdata is None or event.ydata is None:
            return
            
        c = int(round(event.xdata))
        r = int(round(event.ydata))
        
        N = self.grid.shape[0]
        if 0 <= r < N and 0 <= c < N:
            selected_strat = self.paint_var.get()
            if selected_strat in self.strategies:
                self.grid[r, c] = self.strategies[selected_strat]()
                self.draw_grid()
        
    def init_grid(self):
        self.hide_warning()
        try:
            self.strategies = {cls.__name__: cls for cls in tasks.BaseStrategy.__subclasses__()}
            self.rebuild_paint_controls()
            if 'AlwaysCooperate' not in self.strategies or 'AlwaysDefect' not in self.strategies:
                raise ValueError("Need AlwaysCooperate and AlwaysDefect defined for default seeds.")
                
            N = int(self.entry_N.get())
            self.grid = np.empty((N, N), dtype=object)
            
            init_mode = self.init_var.get()
            if init_mode == "Random":
                strat_classes = list(self.strategies.values())
                for r in range(N):
                    for c in range(N):
                        self.grid[r, c] = np.random.choice(strat_classes)()
            elif init_mode in self.strategies:
                strat_class = self.strategies[init_mode]
                for r in range(N):
                    for c in range(N):
                        self.grid[r, c] = strat_class()
            else:
                raise ValueError(f"Unknown initial state: {init_mode}")
                        
            T = float(self.entry_T.get())
            R = float(self.entry_R.get())
            P = float(self.entry_P.get())
            S = float(self.entry_S.get())
            self.matrix = {'C': {'C': R, 'D': S}, 'D': {'C': T, 'D': P}}
            
            self.generation = 0
            self.draw_grid()
            
        except Exception as e:
            self.show_warning(str(e))
            
    def step(self, steps=1):
        if self.grid is None:
            self.show_warning("Please initialize grid first.")
            return
            
        self.hide_warning()
        try:
            for _ in range(steps):
                self.grid = tasks.update_grid_deterministic(self.grid, self.matrix, rounds=1)
                self.generation += 1
            self.draw_grid()
        except Exception as e:
            self.show_warning(str(e))
            
    def draw_grid(self):
        N = self.grid.shape[0]
        color_data = np.zeros((N, N, 3))
        
        self.strategies = {cls.__name__: cls for cls in tasks.BaseStrategy.__subclasses__()}
        strat_names = list(self.strategies.keys())
        colors_pool = [
            '#0000FF', '#FF0000', '#00FF00', '#FFFF00', '#FF00FF', '#00FFFF',
            '#FFA500', '#800080', '#008000', '#000080', '#800000', '#008080'
        ]
        for i, name in enumerate(strat_names):
            if name not in self.strat_colors:
                self.strat_colors[name] = colors_pool[i % len(colors_pool)]
                if name == 'AlwaysCooperate': self.strat_colors[name] = '#0000FF'
                if name == 'AlwaysDefect': self.strat_colors[name] = '#FF0000'
                
        for r in range(N):
            for c in range(N):
                name = self.grid[r, c].__class__.__name__
                hex_col = self.strat_colors.get(name, '#ffffff')
                rgb = mcolors.to_rgb(hex_col)
                color_data[r, c] = rgb
                
        if not hasattr(self, 'im_plot') or self.im_plot not in self.ax.images:
            self.ax.clear()
            self.im_plot = self.ax.imshow(color_data, interpolation='nearest')
            self.ax.axis('off')
            
            import matplotlib.patches as mpatches
            # Always show all available strategies in the legend
            legend_patches = [mpatches.Patch(color=col, label=name) for name, col in self.strat_colors.items() if name in strat_names]
            if legend_patches:
                self.ax.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
            self.fig.tight_layout()
        else:
            self.im_plot.set_data(color_data)
            
        self.ax.set_title(f"Generation: {self.generation}")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    
    def on_closing():
        root.quit()
        root.destroy()
        sys.exit(0)
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.geometry("800x600")
    controls = tk.Frame(root, width=200)
    controls.pack(side=tk.LEFT, fill=tk.Y)
    canvas = tk.Frame(root)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    app = Level3Spatial(controls, canvas)
    root.mainloop()
