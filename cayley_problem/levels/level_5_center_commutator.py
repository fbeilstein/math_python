import tkinter as tk
import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class Level5CenterCommutator(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.add_warning()
        
        tk.Label(self.left_panel, text="L5: Center & Commutator", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=180).pack(pady=5)
        
        input_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        input_frame.pack(pady=2, fill=tk.X)
        
        tk.Label(input_frame, text="Generators:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_gens = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_gens.pack(fill=tk.X, padx=2, pady=1)
        self.entry_gens.insert(0, "a, b")
        
        tk.Label(input_frame, text="Relations:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_rels = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_rels.pack(fill=tk.X, padx=2, pady=1)
        # Dihedral group D4 (non-abelian)
        self.entry_rels.insert(0, "aaaa=e, bb=e, abab=e")
        
        tk.Button(self.left_panel, text="Analyze Subgroups", font=("Arial", 10, "bold"), bg="#007acc", fg="white", command=self.generate).pack(pady=5, fill=tk.X, padx=2)
        
        self.setup_graph_ui()

    def parse_relations(self, rels_str):
        rels = []
        for part in rels_str.split(','):
            part = part.strip()
            if '=' in part:
                lhs, rhs = part.split('=', 1)
                lhs = lhs.strip()
                rhs = rhs.strip()
                if rhs == 'e': rhs = ''
                if lhs == 'e': lhs = ''
                rels.append((lhs, rhs))
        return rels

    def generate(self):
        gens = [g.strip() for g in self.entry_gens.get().split(',') if g.strip()]
        rels = self.parse_relations(self.entry_rels.get())
        
        nodes, edges = tasks.generate_cayley_graph(gens, rels, max_depth=10)
        
        center = tasks.compute_center(nodes, rels)
        commutator = tasks.compute_commutator_subgroup(nodes, rels)
        
        self.ax.clear()
        
        self.G = nx.DiGraph()
        for n in nodes: self.G.add_node(n)
        for u, g, v in edges: self.G.add_edge(u, v)
            
        pos = nx.spring_layout(self.G, seed=42)
        
        self.nodes = nodes
        self.center = center
        self.commutator = commutator
        
        vis_nodes = []
        for n in nodes:
            if n in center and n in commutator: c = 'purple'
            elif n in center: c = 'gold'
            elif n in commutator: c = 'red'
            else: c = 'lightblue'
            vis_nodes.append({'id': n, 'label': n, 'color': c})
        vis_edges = [{'from': u, 'to': v} for u, g, v in edges]
        
        title = f"Z(G): {len(center)} | [G,G]: {len(commutator)}"
        self.update_graph(self.G, pos, self.draw_graph, vis_nodes, vis_edges, title=title)
        
    def draw_graph(self, pos):
        self.ax.clear()
        
        artists = {'nodes': [], 'labels': None, 'edges': []}
        
        node_colors = []
        for n in self.nodes:
            if n in self.center and n in self.commutator:
                node_colors.append('purple') # Both
            elif n in self.center:
                node_colors.append('gold')
            elif n in self.commutator:
                node_colors.append('red')
            else:
                node_colors.append('lightblue')
                
        path_col = nx.draw_networkx_nodes(self.G, pos, ax=self.ax, node_color=node_colors, node_size=500)
        artists['nodes'].append((list(self.nodes), path_col))
        
        artists['labels'] = nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=10)
        
        patches = nx.draw_networkx_edges(self.G, pos, ax=self.ax, arrows=True, arrowsize=10, connectionstyle="arc3,rad=0.1", alpha=0.3)
        if patches:
            for patch, (u, v) in zip(patches, self.G.edges()):
                artists['edges'].append((u, v, patch))
        
        title = f"Group Order: {len(self.nodes)}\n"
        title += f"Center Z(G) [Gold]: {len(self.center)} elements\n"
        title += f"Commutator [G,G] [Red]: {len(self.commutator)} elements"
        self.ax.set_title(title)
        self.ax.axis('off')
        
        return artists

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel5(unittest.TestCase):
    def test_center(self):
        nodes = {"e", "a", "b", "ba"} # K4 is abelian
        rels = [("aa", ""), ("bb", ""), ("ab", "ba")]
        center = tasks.compute_center(nodes, rels)
        self.assertEqual(center, nodes)
        
    def test_commutator(self):
        nodes = {"e", "a", "b", "ba"} # K4 is abelian
        rels = [("aa", ""), ("bb", ""), ("ab", "ba")]
        commutator = tasks.compute_commutator_subgroup(nodes, rels)
        self.assertEqual(commutator, {"e"})
        
if __name__ == '__main__':
    unittest.main()
