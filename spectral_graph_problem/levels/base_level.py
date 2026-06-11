import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class BaseLevel:
    def __init__(self, controls_parent, canvas_parent):
        self.controls_parent = controls_parent
        self.canvas_parent = canvas_parent
        self.left_panel = tk.Frame(controls_parent, bg="#1e1e1e")
        self.left_panel.pack(fill=tk.BOTH, expand=True)
        self.nodes = [] # List of (x, y)
        self.edges = {} # (i, j): weight (where i < j)
        
    def setup_graph_ui(self):
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.fig.patch.set_facecolor('#2d2d30')
        self.ax = self.fig.add_subplot(111)
        self._apply_dark_theme()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_parent)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def _apply_dark_theme(self):
        self.ax.set_facecolor('#2d2d30')
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('white')
            
    def add_warning(self):
        self.warning_label = tk.Label(self.left_panel, text="", bg="#1e1e1e", fg="red", wraplength=200, justify="left")
        self.warning_label.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        
    def show_warning(self, msg):
        if hasattr(self, 'warning_label'):
            self.warning_label.config(text=msg)
            
    def hide_warning(self):
        if hasattr(self, 'warning_label'):
            self.warning_label.config(text="")
            
    def get_edges_list(self):
        """Return list of (u, v, w) edges."""
        res = []
        for (u, v), w in self.edges.items():
            res.append((u, v, w))
        return res
        
    def draw_graph(self, node_colors=None):
        """Helper to draw the nodes and edges on the axis."""
        self.ax.clear()
        self._apply_dark_theme()
        
        # Lock axes so adding points doesn't cause auto-scaling collapse
        self.ax.set_xlim(0.0, 1.0)
        self.ax.set_ylim(0.0, 1.0)
        
        # Draw edges
        for (i, j), w in self.edges.items():
            x = [self.nodes[i][0], self.nodes[j][0]]
            y = [self.nodes[i][1], self.nodes[j][1]]
            # Thickness scales with weight. Clamped so it's visible.
            lw = max(0.5, w * 2.0)
            alpha = max(0.2, min(1.0, w))
            self.ax.plot(x, y, color='#aaaaaa', linewidth=lw, alpha=alpha, zorder=1)
            
        # Draw nodes
        if not self.nodes:
            self.canvas.draw()
            return
            
        xs = [p[0] for p in self.nodes]
        ys = [p[1] for p in self.nodes]
        
        if node_colors is None:
            node_colors = ['#4488ff'] * len(self.nodes)
            
        self.ax.scatter(xs, ys, s=150, c=node_colors, edgecolor='white', zorder=2)
        
        for i, (x, y) in enumerate(self.nodes):
            self.ax.text(x, y, str(i), color='black', fontsize=8, ha='center', va='center', zorder=3)
            
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()
        
    def destroy(self):
        self.left_panel.destroy()
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
