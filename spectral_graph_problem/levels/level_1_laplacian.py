import tkinter as tk
from tkinter import ttk
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level1Laplacian(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.setup_graph_ui()
        self.add_warning()
        
        self.selected_node = None
        self.selected_edge = None
        
        tk.Label(self.left_panel, text="L1: Matrix Construction", bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.left_panel, text="Controls:\n- Click empty space: Add Node\n- Click 2 Nodes: Add Edge\n- Click Edge Midpoint: Select Edge", bg="#1e1e1e", fg="#aaaaaa", justify=tk.LEFT).pack(pady=5, anchor="w")
        
        self.weight_var = tk.DoubleVar(value=1.0)
        self.weight_slider = tk.Scale(self.left_panel, from_=0.0, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.weight_var, label="Selected Edge Weight", bg="#1e1e1e", fg="white", command=self.on_weight_change)
        self.weight_slider.pack(fill=tk.X, pady=10)
        self.weight_slider.config(state=tk.DISABLED)
        
        tk.Button(self.left_panel, text="Delete Selected (Or Right-Click)", command=self.delete_selected, bg="#8c2e2e", fg="white").pack(fill=tk.X, pady=5)
        tk.Button(self.left_panel, text="Clear Graph", command=self.clear_graph).pack(fill=tk.X, pady=5)
        
        tk.Button(self.left_panel, text="Show Adjacency Matrix", command=self.show_adjacency, bg="#2e5c2e", fg="white").pack(fill=tk.X, pady=(20, 5))
        tk.Button(self.left_panel, text="Show Laplacian Matrix", command=self.show_laplacian, bg="#2e5c2e", fg="white").pack(fill=tk.X, pady=5)
        
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.dragged_node = None
        self.press_x = None
        self.press_y = None
        self.is_dragged = False
        
        self.draw_graph()
        
    def clear_graph(self):
        self.nodes = []
        self.edges = {}
        self.selected_node = None
        self.selected_edge = None
        self.weight_slider.config(state=tk.DISABLED)
        self.draw_graph()
        
    def _pt_to_segment_dist(self, px, py, ax, ay, bx, by):
        ab_x, ab_y = bx - ax, by - ay
        ap_x, ap_y = px - ax, py - ay
        ab_dot = ab_x*ab_x + ab_y*ab_y
        if ab_dot == 0:
            return np.sqrt(ap_x**2 + ap_y**2)
        t = max(0.0, min(1.0, (ap_x*ab_x + ap_y*ab_y) / ab_dot))
        closest_x = ax + t * ab_x
        closest_y = ay + t * ab_y
        return np.sqrt((px - closest_x)**2 + (py - closest_y)**2)
        
    def delete_selected(self):
        if self.selected_node is not None:
            i = self.selected_node
            self.nodes.pop(i)
            new_edges = {}
            for (u, v), w in self.edges.items():
                if u == i or v == i: continue
                nu = u if u < i else u - 1
                nv = v if v < i else v - 1
                new_edges[(min(nu, nv), max(nu, nv))] = w
            self.edges = new_edges
            self.selected_node = None
            
        elif self.selected_edge is not None:
            if self.selected_edge in self.edges:
                del self.edges[self.selected_edge]
            self.selected_edge = None
            self.weight_slider.config(state=tk.DISABLED)
            
        self.draw_graph()

    def on_press(self, event):
        if event.inaxes != self.ax: return
        self.press_x, self.press_y = event.xdata, event.ydata
        self.is_dragged = False
        self.dragged_node = None
        
        if self.press_x is None or self.press_y is None: return
        
        for i, (nx, ny) in enumerate(self.nodes):
            if (nx - self.press_x)**2 + (ny - self.press_y)**2 < 0.05**2:
                self.dragged_node = i
                break
                
    def on_motion(self, event):
        if event.inaxes != self.ax or self.dragged_node is None: return
        x, y = event.xdata, event.ydata
        if x is None or y is None: return
        
        dist = (x - self.press_x)**2 + (y - self.press_y)**2
        if dist > 0.01**2:
            self.is_dragged = True
            
        if self.is_dragged:
            self.nodes[self.dragged_node] = (x, y)
            self.draw_graph()
            
    def on_release(self, event):
        if self.is_dragged:
            self.dragged_node = None
            return
            
        self.dragged_node = None
        self.process_click(event)

    def process_click(self, event):
        if event.inaxes != self.ax: return
        x, y = event.xdata, event.ydata
        if x is None or y is None: return
        
        clicked_node = None
        for i, (nx, ny) in enumerate(self.nodes):
            if (nx - x)**2 + (ny - y)**2 < 0.05**2: # threshold 0.05
                clicked_node = i
                break
                
        clicked_edge = None
        min_dist = 0.05
        for (u, v), w in self.edges.items():
            dist = self._pt_to_segment_dist(x, y, self.nodes[u][0], self.nodes[u][1], self.nodes[v][0], self.nodes[v][1])
            if dist < min_dist:
                min_dist = dist
                clicked_edge = (u, v)

        if event.button == 3: # Right click (Delete)
            if clicked_node is not None:
                self.selected_node = clicked_node
                self.delete_selected()
            elif clicked_edge is not None:
                self.selected_edge = clicked_edge
                self.delete_selected()
            return
            
        # Left click handling
        if clicked_node is not None:
            if self.selected_node is None:
                self.selected_node = clicked_node
                self.selected_edge = None
                self.weight_slider.config(state=tk.DISABLED)
                self.draw_graph()
            else:
                if self.selected_node != clicked_node:
                    u, v = min(self.selected_node, clicked_node), max(self.selected_node, clicked_node)
                    if (u, v) in self.edges:
                        del self.edges[(u, v)]
                    else:
                        self.edges[(u, v)] = 1.0
                self.selected_node = None
                self.draw_graph()
            return

        if clicked_edge is not None:
            self.selected_edge = clicked_edge
            self.selected_node = None
            self.weight_slider.config(state=tk.NORMAL)
            self.weight_var.set(self.edges[clicked_edge])
            self.draw_graph()
            return
            
        # Otherwise create a new node
        self.nodes.append((x, y))
        self.selected_node = None
        self.selected_edge = None
        self.weight_slider.config(state=tk.DISABLED)
        self.draw_graph()
        
    def on_weight_change(self, val):
        if self.selected_edge is not None:
            self.edges[self.selected_edge] = float(val)
            self.draw_graph()
            
    def draw_graph(self):
        colors = ['#4488ff'] * len(self.nodes)
        if self.selected_node is not None:
            colors[self.selected_node] = '#ffaa00'
            
        super().draw_graph(node_colors=colors)
        
        # Highlight selected edge
        if self.selected_edge is not None:
            u, v = self.selected_edge
            ex = [self.nodes[u][0], self.nodes[v][0]]
            ey = [self.nodes[u][1], self.nodes[v][1]]
            self.ax.plot(ex, ey, color='#ff0000', linewidth=2, zorder=2)
            self.canvas.draw()
            
    def _display_matrix(self, title, mat):
        top = tk.Toplevel(self.controls_parent)
        top.title(title)
        top.geometry("400x300")
        top.configure(bg="#2d2d30")
        text = tk.Text(top, bg="#1e1e1e", fg="white", font=("Courier", 12))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        np.set_printoptions(precision=2, suppress=True, linewidth=100)
        text.insert(tk.END, f"{title}:\n\n")
        text.insert(tk.END, str(np.array(mat)))
        text.config(state=tk.DISABLED)
        
    def show_adjacency(self):
        self.hide_warning()
        try:
            A = tasks.build_adjacency_matrix(len(self.nodes), self.get_edges_list())
            self._display_matrix("Adjacency Matrix", A)
        except Exception as e:
            self.show_warning(f"Error: {e}")
            
    def show_laplacian(self):
        self.hide_warning()
        try:
            A = tasks.build_adjacency_matrix(len(self.nodes), self.get_edges_list())
            L = tasks.build_laplacian_matrix(A)
            self._display_matrix("Laplacian Matrix", L)
        except Exception as e:
            self.show_warning(f"Error: {e}")
