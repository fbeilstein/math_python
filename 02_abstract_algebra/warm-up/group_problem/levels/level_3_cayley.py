"""Level 3: Cayley Graph — BFS traversal from identity."""
import tkinter as tk
import networkx as nx
from levels.base_level import TabbedLevel
import implementation_tasks as tasks


class Level3Cayley(TabbedLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)

        tk.Label(self.left_panel, text="L3: Cayley Graph", font=("Arial", 13, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=4)
                 
        tk.Label(self.left_panel, text="Initial generators taken from input.\nClick nodes to toggle generators!",
                 bg="#1e1e1e", fg="#8b949e", font=("Arial", 9)).pack(pady=4)

        self._active_gens = []
        self.setup_matplotlib()

    def on_group_loaded(self, group):
        if hasattr(group, 'generators') and group.generators:
            self._active_gens = list(group.generators)
        else:
            self._active_gens = [g for g in list(group.elements)[:3] if g != group.identity_element][:2]
            if not self._active_gens:
                self._active_gens = [group.identity_element]
        self.generate()

    def on_node_click(self, node):
        if node == self._group.identity_element:
            return
            
        if node in self._active_gens:
            self._active_gens.remove(node)
        else:
            self._active_gens.append(node)
            
        self.generate()

    def generate(self):
        if self._group is None:
            self.show_error("Load a group first (use tabs above)")
            return
            
        try:
            nodes, edges = tasks.generate_cayley_graph(self._group, self._active_gens)
        except Exception as e:
            self.show_error(str(e))
            return

        G = nx.DiGraph()
        
        for n in nodes:
            G.add_node(n)
            
        for u, g, v in edges:
            G.add_edge(u, v, gen=g)

        def draw_callback(pos):
            self.ax.clear()
            artists = {'nodes': [], 'labels': None, 'edges': []}
            
            path_col = nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color='#58a6ff',
                                   node_size=400, edgecolors='#79c0ff', linewidths=1.5)
            artists['nodes'].append((list(G.nodes()), path_col))
            
            labels = {n: str(n) for n in G.nodes()}
            artists['labels'] = nx.draw_networkx_labels(G, pos, labels=labels, ax=self.ax, font_size=8,
                                    font_color='white', font_weight='bold')
                                    
            colors_list = ['#ff7b72', '#7ee787', '#58a6ff', '#ffa657', '#d2a8ff']
            unique_gens = sorted(set(d['gen'] for u, v, d in G.edges(data=True)))
            for idx, g in enumerate(unique_gens):
                gen_edges = [(u, v) for u, v, d in G.edges(data=True) if d['gen'] == g]
                patches = nx.draw_networkx_edges(G, pos, edgelist=gen_edges, ax=self.ax,
                                       edge_color=colors_list[idx % len(colors_list)],
                                       arrows=True, arrowsize=12,
                                       connectionstyle="arc3,rad=0.15", alpha=0.7)
                if patches:
                    for patch, (u, v) in zip(patches, gen_edges):
                        artists['edges'].append((u, v, patch))
                        
            gen_names = ", ".join(str(g) for g in self._active_gens)
            self.ax.set_title(f"Cayley Graph (order {len(nodes)})\nGenerators: {gen_names}", color='#58a6ff', fontsize=12)
            self.ax.axis('off')
            return artists
            
        existing_pos = self.graph_manager.pos if (hasattr(self, 'graph_manager') and self.graph_manager and set(self.graph_manager.G.nodes()) == set(G.nodes())) else None
        self.update_graph(G, existing_pos, draw_callback, on_node_click=self.on_node_click)
