"""Level 6: Center, Commutator, Conjugacy — commutator heatmap."""
import tkinter as tk
import numpy as np
from levels.base_level import TabbedLevel
import implementation_tasks as tasks


class Level6Center(TabbedLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)

        tk.Label(self.left_panel, text="L6: Center & Conjugacy", font=("Arial", 13, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=4)

        self.selected_elements = set()

        self.view_mode = "conjugacy"
        self.toggle_btn = tk.Button(self.left_panel, text="View Abelianization G/[G,G]", 
                                    bg="#238636", fg="white", font=("Arial", 10, "bold"), 
                                    command=self.toggle_view)
        self.toggle_btn.pack(pady=4, fill=tk.X, padx=4)

        # Highlight modes
        self.highlight_mode = tk.StringVar(value="conjugacy")
        modes_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        modes_frame.pack(fill=tk.X, pady=4)
        tk.Radiobutton(modes_frame, text="Interactive Conjugacy/Centralizer", variable=self.highlight_mode, 
                       value="conjugacy", bg="#1e1e1e", fg="white", selectcolor="#2d2d30", 
                       command=self.update_view).pack(anchor="w")
        tk.Radiobutton(modes_frame, text="Highlight Center Z(G) [Squares]", variable=self.highlight_mode, 
                       value="center", bg="#1e1e1e", fg="white", selectcolor="#2d2d30", 
                       command=self.update_view).pack(anchor="w")
        tk.Radiobutton(modes_frame, text="Highlight Commutator [G,G] [Diamonds]", variable=self.highlight_mode, 
                       value="commutator", bg="#1e1e1e", fg="white", selectcolor="#2d2d30", 
                       command=self.update_view).pack(anchor="w")

        self.info_label = tk.Label(self.left_panel, text="", font=("Courier", 9),
                                   bg="#1e1e1e", fg="#c9d1d9", wraplength=280, justify=tk.LEFT)
        self.info_label.pack(padx=4, fill=tk.X, pady=4)

        self.setup_matplotlib(figsize=(6, 5))
        self._node_pos = None

    def on_group_loaded(self, group):
        self.selected_elements.clear()
        self._node_pos = None
        self.view_mode = "conjugacy"
        self.toggle_btn.config(text="View Abelianization G/[G,G]")
        self.update_view()

    def on_node_click(self, node):
        if self.view_mode != "conjugacy": return
        
        if self.highlight_mode.get() == "conjugacy":
            if node in self.selected_elements:
                self.selected_elements.remove(node)
            else:
                self.selected_elements.add(node)
            self.update_view()

    def toggle_view(self):
        if self.view_mode == "conjugacy":
            self.view_mode = "abelianization"
            self.toggle_btn.config(text="View Conjugacy Classes")
        else:
            self.view_mode = "conjugacy"
            self.toggle_btn.config(text="View Abelianization G/[G,G]")
            self._node_pos = None # Force layout reset when coming back
        self.update_view()

    def update_view(self):
        if self._group is None:
            self.show_error("Load a group first")
            return
        try:
            center = tasks.compute_center(self._group)
            commutator = tasks.compute_commutator_subgroup(self._group)
            conj_classes = tasks.compute_conjugacy_classes(self._group)
            if center is None or commutator is None or conj_classes is None:
                self.show_error("One or more structural invariants not implemented (center, commutator, conjugacy)")
                return
        except Exception as e:
            self.show_error(str(e))
            return

        # Compute Intersection of Centralizers
        centralizer = set(self._group.elements) if self.selected_elements else set()
        for x in self.selected_elements:
            cx = {g for g in self._group.elements if g * x == x * g}
            centralizer = centralizer.intersection(cx)

        # Compute Union of Conjugacy Classes
        union_classes = set()
        for x in self.selected_elements:
            for cls in conj_classes:
                if x in cls:
                    union_classes.update(cls)
                    break

        z_str = ', '.join(str(e) for e in sorted(center, key=str))
        c_str = ', '.join(str(e) for e in sorted(commutator, key=str))
        lines = [
            f"Z(G) = {{{z_str}}}  |Z|={len(center)}",
            f"[G,G] = {{{c_str}}}  |[G,G]|={len(commutator)}",
            f"Abelian: {'Yes' if len(center) == len(self._group.elements) else 'No'}",
        ]
        
        if self.view_mode == "conjugacy":
            lines.append(f"\nConjugacy classes: {len(conj_classes)}")
            if self.selected_elements:
                if len(self.selected_elements) == 1:
                    sel = next(iter(self.selected_elements))
                    sel_lbl = str(sel)
                    lines.append(f"|Class({sel_lbl})| * |C({sel_lbl})| = |G|")
                    lines.append(f"      {len(union_classes)}      *     {len(centralizer)}     = {len(self._group.elements)}")
                else:
                    lines.append(f"Selected: {len(self.selected_elements)} elements")
                    lines.append(f"Union of Classes size: {len(union_classes)}")
                    lines.append(f"Intersection of Centralizers size: {len(centralizer)}")
        else:
            lines.append(f"\nQuotient G/[G,G] order: {len(self._group.elements) // len(commutator)}")
            
        self.info_label.config(text='\n'.join(lines))

        if self.view_mode == "conjugacy":
            self._draw_conjugacy_partition(conj_classes)
        else:
            self._draw_abelianization_table(commutator)

    def _draw_conjugacy_partition(self, conj_classes):
        import networkx as nx
        
        # Calculate cluster positions (circle of circles) if not already placed
        if self._node_pos is None:
            sorted_classes = sorted(list(conj_classes), key=lambda s: (len(s), min(str(x) for x in s)))
            k = len(sorted_classes)
            self._node_pos = {}
            R = 1.0 if k > 1 else 0.0
            for i, cls in enumerate(sorted_classes):
                theta = 2 * np.pi * i / k
                cx, cy = R * np.cos(theta), R * np.sin(theta)
                r = 0.2 + 0.05 * len(cls)
                for j, e in enumerate(sorted(cls, key=str)):
                    if len(cls) == 1:
                        self._node_pos[e] = (cx, cy)
                    else:
                        phi = 2 * np.pi * j / len(cls)
                        self._node_pos[e] = (cx + r * np.cos(phi), cy + r * np.sin(phi))

        mode = self.highlight_mode.get()
        center = tasks.compute_center(self._group)
        commutator = tasks.compute_commutator_subgroup(self._group)

        # Re-compute sets for coloring
        centralizer = set(self._group.elements) if self.selected_elements else set()
        for x in self.selected_elements:
            cx = {g for g in self._group.elements if g * x == x * g}
            centralizer = centralizer.intersection(cx)

        union_classes = set()
        for x in self.selected_elements:
            for cls in conj_classes:
                if x in cls:
                    union_classes.update(cls)
                    break

        H = nx.Graph()
        H.add_nodes_from(self._group.elements)

        def draw_callback(pos):
            self.ax.clear()
            artists = {'nodes': [], 'labels': {}}
            
            # Color nodes and determine shapes
            node_shapes = {'o': [], 's': [], 'd': []}
            node_colors = {'o': [], 's': [], 'd': []}
            edge_colors = {'o': [], 's': [], 'd': []}
            line_widths = {'o': [], 's': [], 'd': []}
            labels = {}
            label_colors = {}
            
            for node in H.nodes():
                labels[node] = str(node)
                
                # Determine Shape (Orthogonal to Color)
                shape = 'o'
                if mode == "center" and node in center:
                    shape = 's'
                elif mode == "commutator" and node in commutator:
                    shape = 'd'

                # Determine Color (Interactive Conjugacy)
                bg_color = '#2d2d30'
                fg_color = 'white'
                border = '#484f58'
                lw = 1.0

                if node in self.selected_elements:
                    bg_color = '#ffd700' # Yellow
                    border = 'white'
                    lw = 2.0
                    fg_color = 'black'
                elif node in union_classes and node in centralizer:
                    bg_color = '#1f6feb' # Blue (centralizer)
                    border = '#7ee787' # Green border (class)
                    lw = 2.5
                    fg_color = 'white'
                elif node in union_classes:
                    bg_color = '#7ee787' # Green
                    border = 'white'
                    fg_color = 'black'
                elif node in centralizer:
                    bg_color = '#1f6feb' # Blue
                    border = 'white'
                    
                # If a structural mode is active, slightly tint the border of structural nodes if they aren't highlighted
                if (mode == "center" and node in center) or (mode == "commutator" and node in commutator):
                    if not self.selected_elements:
                        border = '#d2a8ff' if mode == "center" else '#ff7b72'
                        lw = 2.0

                node_shapes[shape].append(node)
                node_colors[shape].append(bg_color)
                edge_colors[shape].append(border)
                line_widths[shape].append(lw)
                label_colors[node] = fg_color

            for shape, nodes in node_shapes.items():
                if not nodes: continue
                path_col = nx.draw_networkx_nodes(H, pos, nodelist=nodes, ax=self.ax, 
                                       node_shape=shape, node_color=node_colors[shape], 
                                       edgecolors=edge_colors[shape], linewidths=line_widths[shape], 
                                       node_size=600)
                artists['nodes'].append((nodes, path_col))
            
            for node in H.nodes():
                x, y = pos[node]
                text = self.ax.text(x, y, labels[node], color=label_colors[node],
                             fontsize=10, fontweight='bold', ha='center', va='center')
                artists['labels'][node] = text

            if mode == "center":
                title = "Center Z(G) (Squares)"
            elif mode == "commutator":
                title = "Commutator [G,G] (Diamonds)"
            else:
                title = "Click nodes: Yellow=Selected, Green=Class, Blue=Centralizer"
                
            self.ax.set_title(title, color='#58a6ff', fontsize=11, pad=10)
            
            # Calculate limits with margin
            xs = [p[0] for p in pos.values()]
            ys = [p[1] for p in pos.values()]
            margin = 0.5
            if xs: self.ax.set_xlim(min(xs) - margin, max(xs) + margin)
            if ys: self.ax.set_ylim(min(ys) - margin, max(ys) + margin)
            
            self.ax.axis('off')
            return artists

        # Use DraggableGraphManager
        self.update_graph(H, self._node_pos, draw_callback, on_node_click=self.on_node_click, draggable=True)

    def _draw_abelianization_table(self, commutator):
        self.ax.clear()
        
        # Elements of G/[G,G] are cosets of the commutator subgroup
        try:
            cosets = tasks.compute_left_cosets(self._group, commutator)
            if cosets is None:
                self.show_error("compute_left_cosets not implemented (needed for quotient)")
                return
        except Exception as e:
            self.show_error(str(e))
            return
            
        sorted_cosets = sorted(list(cosets), key=lambda s: (self._group.identity_element not in s, min(str(x) for x in s)))
        k = len(sorted_cosets)
        
        # Create multiplication table of cosets
        grid = np.zeros((k, k), dtype=int)
        for i in range(k):
            for j in range(k):
                # Pick representatives
                a = next(iter(sorted_cosets[i]))
                b = next(iter(sorted_cosets[j]))
                c = a * b
                # Find which coset contains c
                for m in range(k):
                    if c in sorted_cosets[m]:
                        grid[i][j] = m
                        break
                        
        # Draw the table
        from matplotlib.colors import ListedColormap
        palette = ['#0d1117', '#58a6ff', '#7ee787', '#ffa657', '#d2a8ff',
                   '#ff7b72', '#79c0ff', '#f0e68c', '#ff69b4', '#aff5b4', '#ffd8b1']
        
        cmap = ListedColormap(palette[:max(k, 1)])
        self.ax.imshow(grid, cmap=cmap, aspect='equal', interpolation='nearest',
                      vmin=0, vmax=k - 1)

        # Labels - name cosets C0, C1, etc.
        labels = [f"C{i}" for i in range(k)]
        
        for i in range(k):
            for j in range(k):
                val = grid[i][j]
                self.ax.text(j, i, labels[val],
                           ha='center', va='center', fontsize=9 if k > 8 else 11,
                           color='white' if val == 0 else '#0d1117',
                           fontweight='bold')

        self.ax.set_xticks(range(k))
        self.ax.set_xticklabels(labels, fontsize=9, color='white')
        self.ax.set_yticks(range(k))
        self.ax.set_yticklabels(labels, fontsize=9, color='white')
        
        # Draw diagonal line to emphasize symmetry
        self.ax.plot([-0.5, k-0.5], [-0.5, k-0.5], color='white', linestyle='--', linewidth=2, alpha=0.5)

        self.ax.set_title("G/[G,G] Table of Bubbles (Symmetric = Abelian)",
                          color='#58a6ff', fontsize=11, pad=10)
        self.ax.tick_params(colors='white')
        
        # Subtitle to explain bubbles
        desc = ", ".join([f"C{i}={{{','.join(str(e) for e in sorted(sorted_cosets[i], key=str))}}}" for i in range(min(k, 4))])
        if k > 4: desc += "..."
        self.ax.text(0.5, -0.15, desc, ha='center', va='top', fontsize=8, color='#c9d1d9', transform=self.ax.transAxes, wrap=True)
        
        self.canvas.draw()
