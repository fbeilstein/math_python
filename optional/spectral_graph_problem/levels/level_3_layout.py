import tkinter as tk
from tkinter import ttk
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import implementation_tasks as tasks
from levels.level_1_laplacian import Level1Laplacian

class Level3Layout(Level1Laplacian):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        # Override the title
        for widget in self.left_panel.winfo_children():
            if isinstance(widget, tk.Label) and "L1:" in widget.cget("text"):
                widget.config(text="L3: Spectral Layout")
                
        tk.Label(self.left_panel, text="Load Graph:", bg="#1e1e1e", fg="white").pack(pady=(10, 0), anchor="w")
        self.graph_type_var = tk.StringVar(value="Ring (N=20)")
        ttk.Combobox(self.left_panel, textvariable=self.graph_type_var, values=["Ring (N=20)", "Grid (5x5)", "Barbell (N=20)", "Random (N=15, p=0.3)"], state="readonly").pack(fill=tk.X, pady=5)
        
        tk.Button(self.left_panel, text="Generate Tangled Graph", command=self.generate_tangled).pack(fill=tk.X, pady=5)
        
        tk.Button(self.left_panel, text="Apply Spectral Layout", command=self.apply_layout, bg="#2e5c2e", fg="white").pack(fill=tk.X, pady=(20, 5))
        
        # Generate initial
        self.generate_tangled()
        
    def _randomize_positions(self):
        N = len(self.nodes)
        self.nodes = [(np.random.uniform(0.1, 0.9), np.random.uniform(0.1, 0.9)) for _ in range(N)]
        
    def generate_tangled(self):
        self.hide_warning()
        self.nodes = []
        self.edges = {}
        self.selected_node = None
        self.selected_edge = None
        self.weight_slider.config(state=tk.DISABLED)
        
        gtype = self.graph_type_var.get()
        if "Ring" in gtype:
            N = 20
            self.nodes = [(0, 0)] * N
            for i in range(N):
                self.edges[(i, (i+1)%N)] = 1.0
                
        elif "Grid" in gtype:
            W, H = 5, 5
            self.nodes = [(0, 0)] * (W * H)
            for y in range(H):
                for x in range(W):
                    i = y * W + x
                    if x < W - 1:
                        self.edges[(i, i + 1)] = 1.0
                    if y < H - 1:
                        self.edges[(i, i + W)] = 1.0
                        
        elif "Barbell" in gtype:
            N1, N2 = 10, 10
            N = N1 + N2
            self.nodes = [(0, 0)] * N
            # Cluster 1 (fully connected)
            for i in range(N1):
                for j in range(i+1, N1):
                    self.edges[(i, j)] = 1.0
            # Cluster 2 (fully connected)
            for i in range(N1, N):
                for j in range(i+1, N):
                    self.edges[(i, j)] = 1.0
            # Path connecting them
            self.edges[(N1-1, N1)] = 0.5
            
        elif "Random" in gtype:
            N = 15
            p = 0.3
            self.nodes = [(0, 0)] * N
            # Ensure connected by building a tree first
            for i in range(1, N):
                self.edges[(np.random.randint(0, i), i)] = 1.0
            # Add random edges
            for i in range(N):
                for j in range(i+1, N):
                    if (i, j) not in self.edges and np.random.random() < p:
                        self.edges[(i, j)] = 1.0
                        
        self._randomize_positions()
        self.draw_graph()
        
    def apply_layout(self):
        self.hide_warning()
        try:
            if not self.nodes: return
            N = len(self.nodes)
            A = tasks.build_adjacency_matrix(N, self.get_edges_list())
            L = tasks.build_laplacian_matrix(A)
            x_coords, y_coords = tasks.get_spectral_coordinates(L)
            
            # Normalize coordinates to fit perfectly in [0.1, 0.9]
            def normalize(coords):
                cmin, cmax = np.min(coords), np.max(coords)
                if cmax > cmin:
                    return 0.1 + 0.8 * (coords - cmin) / (cmax - cmin)
                return np.full_like(coords, 0.5)
                
            x_norm = normalize(x_coords)
            y_norm = normalize(y_coords)
            
            target_nodes = list(zip(x_norm, y_norm))
            initial_nodes = self.nodes.copy()
            
            def animate_step(frame=0, total_frames=30):
                if frame > total_frames:
                    self.nodes = target_nodes
                    self.draw_graph()
                    return
                t = frame / total_frames
                current_nodes = []
                for (ix, iy), (tx, ty) in zip(initial_nodes, target_nodes):
                    cx = ix + (tx - ix) * t
                    cy = iy + (ty - iy) * t
                    current_nodes.append((cx, cy))
                self.nodes = current_nodes
                self.draw_graph()
                self.controls_parent.after(30, animate_step, frame + 1, total_frames)
                
            animate_step()
            
        except Exception as e:
            self.show_warning(f"Error computing layout: {e}")
