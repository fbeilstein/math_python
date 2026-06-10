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

class Level3SubgroupsCosets(BaseLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self.add_warning()
        
        tk.Label(self.left_panel, text="L3: Subgroups", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white", wraplength=180).pack(pady=5)
        
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
        
        tk.Label(input_frame, text="Subgroup Gen:", font=("Arial", 10), bg="#1e1e1e", fg="white").pack(anchor=tk.W, padx=2, pady=1)
        self.entry_sub = tk.Entry(input_frame, font=("Courier", 10), width=20)
        self.entry_sub.pack(fill=tk.X, padx=2, pady=1)
        self.entry_sub.insert(0, "b")
        
        tk.Button(self.left_panel, text="Draw Subgroups", font=("Arial", 10, "bold"), bg="#007acc", fg="white", command=self.generate).pack(pady=5, fill=tk.X, padx=2)
        
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
        sub_subset = [g.strip() for g in self.entry_sub.get().split(',') if g.strip()]
        
        try:
            from group_engine import Group
            group = Group(gens, rels)
            nodes, edges = tasks.generate_cayley_graph(group, gens)
            
            # Validate subset
            valid_subset = []
            for x in sub_subset:
                try:
                    valid_subset.append(group.parse(x))
                except ValueError:
                    pass
                
            subgroup = tasks.generate_subgroup(group, sub_subset)
            cosets = tasks.compute_left_cosets(group, subgroup)
            
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Error:\n{str(e)}", color="red", fontsize=14, ha='center', va='center')
            self.canvas.draw()
            return
        
        self.ax.clear()
        
        self.G = nx.DiGraph()
        for n in nodes: self.G.add_node(n)
        for u, g, v in edges: self.G.add_edge(u, v)
            
        pos = nx.spring_layout(self.G, seed=42)
        
        self.nodes = nodes
        self.subgroup = subgroup
        self.cosets = cosets
        
        colors = ['gold', 'lightblue', 'lightgreen', 'pink', 'violet', 'cyan', 'lightcoral']
        vis_nodes = []
        for n in nodes:
            c = 'white'
            for idx, coset in enumerate(cosets):
                if n in coset:
                    c = colors[idx % len(colors)]
                    break
            vis_nodes.append({'id': n, 'label': n, 'color': c})
        vis_edges = [{'from': u, 'to': v} for u, g, v in edges]
        
        title = f"Group Order: {len(nodes)} | Subgroup: {len(subgroup)} | Index: {len(cosets)}"
        self.update_graph(self.G, pos, self.draw_graph, vis_nodes, vis_edges, title=title)
        
    def draw_graph(self, pos):
        self.ax.clear()
        
        artists = {'nodes': [], 'labels': None, 'edges': []}
        
        colors = ['gold', 'lightblue', 'lightgreen', 'pink', 'violet', 'cyan', 'lightcoral']
        for idx, coset in enumerate(self.cosets):
            valid_nodes = [n for n in coset if n in self.nodes]
            if valid_nodes:
                path_col = nx.draw_networkx_nodes(self.G, pos, nodelist=valid_nodes, ax=self.ax, node_color=colors[idx % len(colors)], node_size=500, label=f"Coset {idx}" if idx > 0 else "Subgroup H")
                artists['nodes'].append((valid_nodes, path_col))
            
        artists['labels'] = nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=10)
        
        patches = nx.draw_networkx_edges(self.G, pos, ax=self.ax, arrows=True, arrowsize=10, connectionstyle="arc3,rad=0.1", alpha=0.3)
        if patches:
            for patch, (u, v) in zip(patches, self.G.edges()):
                artists['edges'].append((u, v, patch))
        
        self.ax.set_title(f"Group Order: {len(self.nodes)} | Subgroup Order: {len(self.subgroup)} | Index: {len(self.cosets)}")
        self.ax.axis('off')
        self.ax.legend(loc="upper right", fontsize='small')
        
        return artists

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel3(unittest.TestCase):
    def test_subgroup_generation(self):
        # Z4 = <a | aaaa=e>. Subgroup generated by a^2 is {e, aa}
        nodes = {"e", "a", "aa", "aaa"}
        subgroup = tasks.generate_subgroup({"aa"}, nodes, [("aaaa", "")])
        self.assertEqual(subgroup, {"e", "aa"})
        
    def test_cosets(self):
        # Z4. H = {e, aa}. Cosets: {e, aa}, {a, aaa}
        nodes = {"e", "a", "aa", "aaa"}
        cosets = tasks.compute_left_cosets({"e", "aa"}, nodes, [("aaaa", "")])
        self.assertEqual(len(cosets), 2)
        
if __name__ == '__main__':
    unittest.main()
