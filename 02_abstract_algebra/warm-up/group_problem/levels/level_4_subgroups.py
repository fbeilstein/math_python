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
        for i in range(group.order):
            btn = tk.Button(self.elements_frame, text=group.label(i), width=4,
                            bg="#2d2d30", fg="white", font=("Arial", 9),
                            command=lambda idx=i: self.toggle_element(idx))
            row = i // 5
            col = i % 5
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.element_buttons[i] = btn
            
        self.find_subgroups()

    def toggle_element(self, idx):
        if idx in self.selected_elements:
            self.selected_elements.remove(idx)
            self.element_buttons[idx].config(bg="#2d2d30")
        else:
            self.selected_elements.add(idx)
            self.element_buttons[idx].config(bg="#58a6ff")
        
        self.find_subgroups()

    def find_subgroups(self):
        if self._group is None:
            self.show_error("Load a group first")
            return
        try:
            subgroups = tasks.find_all_subgroups(self._group)
        except Exception as e:
            self.show_error(str(e))
            return

        # Sort for stable layout across clicks
        sg_list = sorted(list(subgroups), key=lambda s: (len(s), tuple(sorted(s))))
        
        if self.selected_elements:
            generated_sg = tasks.generate_subgroup(self._group, list(self.selected_elements))
        else:
            generated_sg = {self._group.identity}
            
        highlight_idx = -1
        for i, sg in enumerate(sg_list):
            if sg == generated_sg:
                highlight_idx = i
                break

        # Info text
        elems = ', '.join(self._group.label(e) for e in sorted(generated_sg))
        lines = [f"Total Subgroups: {len(subgroups)}"]
        if self.selected_elements:
            sel_str = ', '.join(self._group.label(e) for e in sorted(self.selected_elements))
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

        # Layout: group by order
        levels = {}
        for i, sg in enumerate(sg_list):
            sz = len(sg)
            levels.setdefault(sz, []).append(i)

        pos = {}
        sorted_sizes = sorted(levels.keys())
        for y_idx, sz in enumerate(sorted_sizes):
            nodes_at_level = levels[sz]
            for x_idx, node in enumerate(nodes_at_level):
                x = (x_idx + 0.5) / max(len(nodes_at_level), 1)
                y = y_idx / max(len(sorted_sizes) - 1, 1)
                pos[node] = (x, y)

        colors = []
        edge_colors = []
        for i in range(len(sg_list)):
            if i == highlight_idx:
                colors.append('#7ee787') # highlighted subgroup
            elif len(sg_list[i]) == 1:
                colors.append('#ffd700')
            elif len(sg_list[i]) == self._group.order:
                colors.append('#ff7b72')
            else:
                colors.append('#58a6ff')
                
        nx.draw_networkx_nodes(H, pos, ax=self.ax, node_color=colors,
                               node_size=600 if i == highlight_idx else 500, 
                               edgecolors='white', linewidths=1.5)
        labels = {i: f"|{len(sg_list[i])}|" for i in range(len(sg_list))}
        nx.draw_networkx_labels(H, pos, labels=labels, ax=self.ax,
                                font_size=10, font_color='black' if i == highlight_idx else 'white', 
                                font_weight='bold')
        nx.draw_networkx_edges(H, pos, ax=self.ax, edge_color='#484f58',
                               arrows=True, arrowsize=12, width=1.5)

        divides = all(self._group.order % len(sg) == 0 for sg in sg_list)
        self.ax.set_title(f"Subgroup Lattice — Lagrange: {'✓' if divides else '?'}",
                          color='#58a6ff', fontsize=12)
        self.ax.axis('off')
        self.canvas.draw()
