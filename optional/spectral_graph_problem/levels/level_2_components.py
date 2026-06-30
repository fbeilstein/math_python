import tkinter as tk
from tkinter import ttk
import sys
import os
import numpy as np
import matplotlib.colors as mcolors

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import implementation_tasks as tasks
# We reuse Level1Laplacian for the drawing mechanism
from levels.level_1_laplacian import Level1Laplacian

class Level2Components(Level1Laplacian):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        
        # Override the title
        for widget in self.left_panel.winfo_children():
            if isinstance(widget, tk.Label) and "L1:" in widget.cget("text"):
                widget.config(text="L2: Null Space & Connectivity")
                
        tk.Button(self.left_panel, text="Find Components (Null Space)", command=self.find_components, bg="#2e5c2e", fg="white").pack(fill=tk.X, pady=(20, 5))
        
        self.num_components_var = tk.StringVar(value="Components: ?")
        tk.Label(self.left_panel, textvariable=self.num_components_var, bg="#1e1e1e", fg="#00ff00", font=("Arial", 12, "bold")).pack(pady=5)
        
    def find_components(self):
        self.hide_warning()
        try:
            if not self.nodes:
                return
                
            N = len(self.nodes)
            A = tasks.build_adjacency_matrix(N, self.get_edges_list())
            L = tasks.build_laplacian_matrix(A)
            
            evals, evecs = tasks.compute_spectrum(L)
            
            # The number of components is the number of 0 eigenvalues
            zero_evecs = tasks.find_zero_eigenvectors(L, tol=1e-4)
            num_comps = zero_evecs.shape[1]
            self.num_components_var.set(f"Components: {num_comps}")
            
            # Print spectrum to console/subwindow
            top = tk.Toplevel(self.controls_parent)
            top.title("Eigendecomposition")
            top.geometry("500x400")
            top.configure(bg="#2d2d30")
            text = tk.Text(top, bg="#1e1e1e", fg="white", font=("Courier", 10))
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            np.set_printoptions(precision=3, suppress=True)
            text.insert(tk.END, f"Eigenvalues:\n{np.round(evals, 3)}\n\n")
            text.insert(tk.END, f"Zero Eigenvectors (Null Space):\n{np.round(zero_evecs, 3)}\n")
            text.config(state=tk.DISABLED)
            
            if num_comps > 0:
                # Nodes in the same component have identical rows in the zero-eigenvector matrix
                # Round to avoid floating point mismatch
                rounded_rows = np.round(zero_evecs, 4)
                unique_rows, labels = np.unique(rounded_rows, axis=0, return_inverse=True)
                
                colors_pool = list(mcolors.TABLEAU_COLORS.values())
                node_colors = [colors_pool[label % len(colors_pool)] for label in labels]
            else:
                node_colors = ['#4488ff'] * N
                
            super().draw_graph(node_colors=node_colors)
            
        except Exception as e:
            self.show_warning(f"Error: {e}")
