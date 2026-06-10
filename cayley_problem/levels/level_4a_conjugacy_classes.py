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

class Level4aConjugacy(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.add_warning()
        
        tk.Label(self.left_panel, text="L4a: Conjugacy Classes", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=180).pack(pady=5)
        
        input_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        input_frame.pack(pady=2, fill=tk.X)
        
        tk.Label(input_frame, text="Generators:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_gens = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_gens.pack(fill=tk.X, padx=2, pady=1)
        self.entry_gens.insert(0, "a, b")
        
        tk.Label(input_frame, text="Relations:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_rels = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_rels.pack(fill=tk.X, padx=2, pady=1)
        self.entry_rels.insert(0, "aaaa=e, bb=e, abab=e")
        
        tk.Label(input_frame, text="Focus Element (x):", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_elem = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_elem.pack(fill=tk.X, padx=2, pady=1)
        self.entry_elem.insert(0, "a")
        
        tk.Button(self.left_panel, text="Calc Conjugacy Class", font=("Arial", 10, "bold"), bg="#007acc", fg="white", command=self.generate).pack(pady=5, fill=tk.X, padx=2)
        
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
        
        try:
            from group_engine import Group
            group = Group(gens, rels)
            nodes, edges = tasks.generate_cayley_graph(group, gens)
            
            try:
                elem = group.parse(self.entry_elem.get().strip())
                conj_class = tasks.compute_conjugacy_class(group, elem)
            except ValueError:
                elem = "Invalid"
                conj_class = set()
                
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Error:\n{str(e)}", color="red", fontsize=14, ha='center', va='center')
            self.canvas.draw()
            return
            
        self.G = nx.DiGraph()
        for n in nodes: self.G.add_node(n)
        for u, g, v in edges: self.G.add_edge(u, v)
            
        pos = nx.spring_layout(self.G, seed=42)
        
        self.nodes = nodes
        self.conj_class = conj_class
        self.elem = elem
        
        vis_nodes = []
        for n in nodes:
            c = 'red' if n in conj_class else 'lightblue'
            vis_nodes.append({'id': n, 'label': n, 'color': c})
        vis_edges = [{'from': u, 'to': v} for u, g, v in edges]
        
        title = f"Conjugacy Class of '{elem}': {len(conj_class)} elements"
        self.update_graph(self.G, pos, self.draw_graph, vis_nodes, vis_edges, title=title)
        
    def draw_graph(self, pos):
        self.ax.clear()
        
        artists = {'nodes': [], 'labels': None, 'edges': []}
        
        node_colors = []
        for n in self.nodes:
            if n in self.conj_class:
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
        
        title = f"Conjugacy Class of '{self.elem}': {len(self.conj_class)} elements\n"
        self.ax.set_title(title)
        self.ax.axis('off')
        
        return artists

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel4a(unittest.TestCase):
    def test_conjugacy(self):
        nodes = {"e", "a", "b", "ba"} # K4
        rels = [("aa", ""), ("bb", ""), ("ab", "ba")]
        # In abelian group, conjugacy class of a is just {a}
        c_class = tasks.compute_conjugacy_class("a", nodes, rels)
        self.assertEqual(c_class, {"a"})
        
if __name__ == '__main__':
    unittest.main()
