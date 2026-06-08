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

class Level2CayleyGraph(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.add_warning()
        
        tk.Label(self.left_panel, text="L2: Cayley Graph", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=180).pack(pady=5)
        
        input_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        input_frame.pack(pady=2, fill=tk.X)
        
        tk.Label(input_frame, text="Generators (comma separated):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_gens = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_gens.pack(fill=tk.X, padx=2, pady=1)
        self.entry_gens.insert(0, "a, b")
        
        tk.Label(input_frame, text="Relations (lhs=rhs):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_rels = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_rels.pack(fill=tk.X, padx=2, pady=1)
        self.entry_rels.insert(0, "aaaa=e, bb=e, abab=e")
        
        tk.Button(self.left_panel, text="Generate Graph", font=("Arial", 10, "bold"), bg="#007acc", fg="white", command=self.generate).pack(pady=5, fill=tk.X, padx=2)
        
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
        
        self.ax.clear()
        
        self.G = nx.DiGraph()
        for n in nodes:
            self.G.add_node(n)
        for u, g, v in edges:
            self.G.add_edge(u, v, label=g)
            
        pos = nx.spring_layout(self.G, seed=42)
        
        self.nodes = nodes
        self.gens = gens
        
        vis_nodes = [{'id': n, 'label': n, 'color': 'lightblue'} for n in nodes]
        vis_edges = []
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        for u, g, v in edges:
            idx = gens.index(g) if g in gens else 0
            vis_edges.append({'from': u, 'to': v, 'label': g, 'color': colors[idx % len(colors)]})
            
        self.update_graph(self.G, pos, self.draw_graph, vis_nodes, vis_edges, title=f"Cayley Graph (Order: {len(nodes)})")

    def draw_graph(self, pos):
        self.ax.clear()
        
        artists = {'nodes': [], 'labels': None, 'edges': []}
        
        path_col = nx.draw_networkx_nodes(self.G, pos, ax=self.ax, node_color='lightblue', node_size=500)
        artists['nodes'].append((list(self.G.nodes()), path_col))
        
        artists['labels'] = nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=10)
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        for idx, gen in enumerate(self.gens):
            gen_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['label'] == gen]
            patches = nx.draw_networkx_edges(self.G, pos, edgelist=gen_edges, ax=self.ax, edge_color=colors[idx % len(colors)], arrows=True, arrowsize=15, connectionstyle="arc3,rad=0.1")
            if patches:
                for patch, (u, v) in zip(patches, gen_edges):
                    artists['edges'].append((u, v, patch))
            
        self.ax.set_title(f"Cayley Graph (Order: {len(self.nodes)})")
        self.ax.axis('off')
        
        return artists

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel2(unittest.TestCase):
    def test_cayley_graph_cyclic(self):
        nodes, edges = tasks.generate_cayley_graph(["a"], [("aaaa", "")])
        self.assertEqual(len(nodes), 4)
        
    def test_cayley_graph_klein4(self):
        nodes, edges = tasks.generate_cayley_graph(["a", "b"], [("aa", ""), ("bb", ""), ("ab", "ba")])
        self.assertEqual(len(nodes), 4)

if __name__ == '__main__':
    unittest.main()
