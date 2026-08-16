"""Level 4: Subgroups & Lagrange — find subgroups, draw Hasse diagram."""
import tkinter as tk
import networkx as nx
from levels.base_level import TabbedLevel
import implementation_tasks as tasks


class Level4Subgroups(TabbedLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)

        tk.Label(self.left_panel, text="L4: Subgroups", font=("Arial", 13, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=4)

        tk.Label(self.left_panel, text="Select elements to generate:", 
                 bg="#1e1e1e", fg="#8b949e", font=("Arial", 9)).pack(pady=2)

        self.elements_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        self.elements_frame.pack(fill=tk.X, padx=4, pady=4)
        
        self.selected_elements = set()
        self.element_buttons = {}

        self.info_label = tk.Label(self.left_panel, text="", font=("Courier", 9),
                                   bg="#1e1e1e", fg="#c9d1d9", wraplength=280, justify=tk.LEFT)
        self.info_label.pack(padx=4, fill=tk.X, pady=4)

        self.setup_matplotlib()

    def on_group_loaded(self, group):
        self.selected_elements.clear()
        
        for widget in self.elements_frame.winfo_children():
            widget.destroy()
            
        self.element_buttons.clear()
        
        # Create grid of buttons for elements
        for i, g in enumerate(group.elements):
            btn = tk.Button(self.elements_frame, text=str(g), width=4,
                            bg="#2d2d30", fg="white", font=("Arial", 9),
                            command=lambda elem=g: self.toggle_element(elem))
            row = i // 5
            col = i % 5
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.element_buttons[g] = btn
            
        self.find_subgroups()

    def toggle_element(self, elem):
        if elem in self.selected_elements:
            self.selected_elements.remove(elem)
            self.element_buttons[elem].config(bg="#2d2d30")
        else:
            self.selected_elements.add(elem)
            self.element_buttons[elem].config(bg="#58a6ff")
        
        self.find_subgroups()

    def on_node_click(self, node_id, sg_list):
        sg = sg_list[node_id]
        self.selected_elements.clear()
        for elem in self.element_buttons:
            self.element_buttons[elem].config(bg="#2d2d30")
            if elem in sg.elements and elem != self._group.identity_element:
                self.selected_elements.add(elem)
                self.element_buttons[elem].config(bg="#58a6ff")
        self.find_subgroups()

    def find_subgroups(self):
        if self._group is None:
            self.show_error("Load a group first")
            return
        try:
            subgroups = tasks.find_all_subgroups(self._group)
            if subgroups is None:
                self.show_error("find_all_subgroups not implemented")
                return
        except Exception as e:
            self.show_error(str(e))
            return

        # Sort for stable layout across clicks
        sg_list = sorted(list(subgroups), key=lambda s: (len(s), tuple(sorted([str(x) for x in s]))))
        
        if self.selected_elements:
            try:
                generated_sg = tasks.generate_group(list(self.selected_elements))
                if generated_sg is None:
                    self.show_error("generate_group not implemented")
                    return
            except Exception as e:
                self.show_error(str(e))
                return
        else:
            generated_sg = tasks.Group(elements=[self._group.identity_element])
            
        highlight_idx = -1
        for i, sg in enumerate(sg_list):
            if sg == generated_sg:
                highlight_idx = i
                break

        # Info text
        elems = ', '.join(str(e) for e in sorted(generated_sg, key=str))
        lines = [f"Total Subgroups: {len(subgroups)}"]
        if self.selected_elements:
            sel_str = ', '.join(str(e) for e in sorted(self.selected_elements, key=str))
            lines.append(f"⟨{sel_str}⟩ = \n  {{{elems}}}\nOrder: {len(generated_sg)}")
        else:
            lines.append("Select elements to generate\na subgroup.")
            
        self.info_label.config(text='\n'.join(lines))

        # Draw Hasse diagram
        self.ax.clear()
        H = nx.DiGraph()
        for i, sg in enumerate(sg_list):
            H.add_node(i, size=len(sg))

        # Edges: sg_i ⊂ sg_j (maximal containment)
        for i in range(len(sg_list)):
            for j in range(len(sg_list)):
                if i != j and sg_list[i] < sg_list[j]:
                    is_maximal = True
                    for k in range(len(sg_list)):
                        if k != i and k != j and sg_list[i] < sg_list[k] < sg_list[j]:
                            is_maximal = False
                            break
                    if is_maximal:
                        H.add_edge(i, j)

        # Compute topological layers for proper Hasse diagram height
        node_layers = {}
        for node in nx.topological_sort(H):
            preds = list(H.predecessors(node))
            if not preds:
                node_layers[node] = 0
            else:
                node_layers[node] = 1 + max(node_layers[p] for p in preds)

        levels = {}
        for node, layer in node_layers.items():
            levels.setdefault(layer, []).append(node)

        pos = {}
        sorted_layers = sorted(levels.keys())
        for y_idx in sorted_layers:
            nodes_at_level = levels[y_idx]
            for x_idx, node in enumerate(nodes_at_level):
                x = (x_idx + 0.5) / max(len(nodes_at_level), 1)
                y = y_idx / max(len(sorted_layers) - 1, 1)
                pos[node] = (x, y)

        def draw_callback(draw_pos):
            self.ax.clear()
            artists = {'nodes': [], 'labels': None, 'edges': []}
            
            colors = []
            sizes = []
            for i in range(len(sg_list)):
                sizes.append(600 if i == highlight_idx else 500)
                if i == highlight_idx:
                    colors.append('#7ee787') # highlighted subgroup
                elif len(sg_list[i]) == 1:
                    colors.append('#ffd700')
                elif len(sg_list[i]) == len(self._group.elements):
                    colors.append('#ff7b72')
                else:
                    colors.append('#58a6ff')
                    
            path_col = nx.draw_networkx_nodes(H, draw_pos, ax=self.ax, node_color=colors,
                                   node_size=sizes, edgecolors='white', linewidths=1.5)
            artists['nodes'].append((list(H.nodes()), path_col))
            
            labels = {i: f"|{len(sg_list[i])}|" for i in range(len(sg_list))}
            artists['labels'] = nx.draw_networkx_labels(H, draw_pos, labels=labels, ax=self.ax,
                                    font_size=10, font_color='black', font_weight='bold')
                                    
            patches = nx.draw_networkx_edges(H, draw_pos, ax=self.ax, edge_color='#484f58',
                                   arrows=True, arrowsize=12, width=1.5)
            if patches:
                for patch, (u, v) in zip(patches, H.edges()):
                    artists['edges'].append((u, v, patch))

            divides = all(len(self._group.elements) % len(sg) == 0 for sg in sg_list)
            msg = f"Lagrange verified: all {len(sg_list)} subgroup sizes divide {len(self._group.elements)}" if divides else "Lagrange violation!"
            self.ax.set_title(msg, color='#7ee787' if divides else '#ff7b72', fontsize=12)
            self.ax.axis('off')
            return artists

        self.update_graph(H, pos, draw_callback, on_node_click=lambda node: self.on_node_click(node, sg_list), draggable=False)
