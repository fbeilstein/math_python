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
        self.toggle_btn.pack(pady=8, fill=tk.X, padx=4)

        self.info_label = tk.Label(self.left_panel, text="", font=("Courier", 9),
                                   bg="#1e1e1e", fg="#c9d1d9", wraplength=280, justify=tk.LEFT)
        self.info_label.pack(padx=4, fill=tk.X, pady=4)

        self.setup_matplotlib(figsize=(6, 5))

    def on_group_loaded(self, group):
        self.selected_elements.clear()
        self.view_mode = "conjugacy"
        self.toggle_btn.config(text="View Abelianization G/[G,G]")
        
        # Bind canvas click
        if not hasattr(self, '_click_cid'):
            self._click_cid = self.canvas.mpl_connect('button_press_event', self.on_click)
            
        self.update_view()

    def on_click(self, event):
        if self.view_mode != "conjugacy" or not event.inaxes: return
        if not hasattr(self, '_node_pos'): return
        
        min_dist = float('inf')
        closest_node = None
        for node, (nx, ny) in self._node_pos.items():
            dist = (nx - event.xdata)**2 + (ny - event.ydata)**2
            if dist < min_dist:
                min_dist = dist
                closest_node = node
                
        if min_dist < 0.05: # threshold
            if closest_node in self.selected_elements:
                self.selected_elements.remove(closest_node)
            else:
                self.selected_elements.add(closest_node)
            self.update_view()

    def toggle_view(self):
        if self.view_mode == "conjugacy":
            self.view_mode = "abelianization"
            self.toggle_btn.config(text="View Conjugacy Classes")
        else:
            self.view_mode = "conjugacy"
            self.toggle_btn.config(text="View Abelianization G/[G,G]")
        self.update_view()

    def update_view(self):
        if self._group is None:
            self.show_error("Load a group first")
            return
        try:
            center = tasks.compute_center(self._group)
            commutator = tasks.compute_commutator_subgroup(self._group)
            conj_classes = tasks.compute_conjugacy_classes(self._group)
        except Exception as e:
            self.show_error(str(e))
            return

        # Compute Intersection of Centralizers
        centralizer = set(range(self._group.order)) if self.selected_elements else set()
        for x in self.selected_elements:
            cx = {g for g in range(self._group.order) if self._group.multiply(g, x) == self._group.multiply(x, g)}
            centralizer = centralizer.intersection(cx)

        # Compute Union of Conjugacy Classes
        union_classes = set()
        for x in self.selected_elements:
            for cls in conj_classes:
                if x in cls:
                    union_classes.update(cls)
                    break

        z_str = ', '.join(self._group.label(e) for e in sorted(center))
        c_str = ', '.join(self._group.label(e) for e in sorted(commutator))
        lines = [
            f"Z(G) = {{{z_str}}}  |Z|={len(center)}",
            f"[G,G] = {{{c_str}}}  |[G,G]|={len(commutator)}",
            f"Abelian: {'Yes' if len(center) == self._group.order else 'No'}",
        ]
        
        if self.view_mode == "conjugacy":
            lines.append(f"\nConjugacy classes: {len(conj_classes)}")
            if self.selected_elements:
                if len(self.selected_elements) == 1:
                    sel = next(iter(self.selected_elements))
                    sel_lbl = self._group.label(sel)
                    lines.append(f"|Class({sel_lbl})| * |C({sel_lbl})| = |G|")
                    lines.append(f"      {len(union_classes)}      *     {len(centralizer)}     = {self._group.order}")
                else:
                    lines.append(f"Selected: {len(self.selected_elements)} elements")
                    lines.append(f"Union of Classes size: {len(union_classes)}")
                    lines.append(f"Intersection of Centralizers size: {len(centralizer)}")
        else:
            lines.append(f"\nQuotient G/[G,G] order: {self._group.order // len(commutator)}")
            
        self.info_label.config(text='\n'.join(lines))

        if self.view_mode == "conjugacy":
            self._draw_conjugacy_partition(conj_classes)
        else:
            self._draw_abelianization_table(commutator)

    def _draw_conjugacy_partition(self, conj_classes):
        self.ax.clear()
        import networkx as nx
        
        # Sort classes by size, then min element
        sorted_classes = sorted(list(conj_classes), key=lambda s: (len(s), min(s)))
        k = len(sorted_classes)
        
        # Calculate cluster positions (circle of circles)
        self._node_pos = {}
        R = 1.0 if k > 1 else 0.0
        for i, cls in enumerate(sorted_classes):
            theta = 2 * np.pi * i / k
            cx, cy = R * np.cos(theta), R * np.sin(theta)
            r = 0.2 + 0.05 * len(cls)
            for j, e in enumerate(sorted(cls)):
                if len(cls) == 1:
                    self._node_pos[e] = (cx, cy)
                else:
                    phi = 2 * np.pi * j / len(cls)
                    self._node_pos[e] = (cx + r * np.cos(phi), cy + r * np.sin(phi))

        # Re-compute sets for coloring
        centralizer = set(range(self._group.order)) if self.selected_elements else set()
        for x in self.selected_elements:
            cx = {g for g in range(self._group.order) if self._group.multiply(g, x) == self._group.multiply(x, g)}
            centralizer = centralizer.intersection(cx)

        union_classes = set()
        for x in self.selected_elements:
            for cls in conj_classes:
                if x in cls:
                    union_classes.update(cls)
                    break

        H = nx.Graph()
        H.add_nodes_from(range(self._group.order))
        
        # Color nodes
        node_colors = []
        edge_colors = []
        line_widths = []
        for node in H.nodes():
            if node in self.selected_elements:
                node_colors.append('#ffd700') # Yellow
                edge_colors.append('white')
                line_widths.append(2.0)
            elif node in union_classes and node in centralizer:
                node_colors.append('#1f6feb') # Blue (centralizer)
                edge_colors.append('#7ee787') # Green border (class)
                line_widths.append(2.5)
            elif node in union_classes:
                node_colors.append('#7ee787') # Green
                edge_colors.append('white')
                line_widths.append(1.0)
            elif node in centralizer:
                node_colors.append('#1f6feb') # Blue
                edge_colors.append('white')
                line_widths.append(1.0)
            else:
                node_colors.append('#2d2d30') # Dark gray
                edge_colors.append('#484f58')
                line_widths.append(1.0)

        nx.draw_networkx_nodes(H, self._node_pos, ax=self.ax, node_color=node_colors, 
                               edgecolors=edge_colors, linewidths=line_widths, node_size=600)
        
        labels = {i: self._group.label(i) for i in H.nodes()}
        label_colors = {i: 'black' if (i in self.selected_elements or i in union_classes) else 'white' for i in H.nodes()}
        
        for node, (x, y) in self._node_pos.items():
            self.ax.text(x, y, labels[node], color=label_colors[node],
                         fontsize=10, fontweight='bold', ha='center', va='center')

        self.ax.set_title("Click nodes: Yellow=Selected, Green=Class, Blue=Centralizer", 
                          color='#58a6ff', fontsize=11, pad=10)
        
        # Calculate limits with margin
        xs = [p[0] for p in self._node_pos.values()]
        ys = [p[1] for p in self._node_pos.values()]
        margin = 0.5
        if xs: self.ax.set_xlim(min(xs) - margin, max(xs) + margin)
        if ys: self.ax.set_ylim(min(ys) - margin, max(ys) + margin)
        
        self.ax.axis('off')
        self.canvas.draw()

    def _draw_abelianization_table(self, commutator):
        self.ax.clear()
        
        # Elements of G/[G,G] are cosets of the commutator subgroup
        cosets = tasks.compute_left_cosets(self._group, commutator)
        sorted_cosets = sorted(list(cosets), key=lambda s: (self._group.identity not in s, min(s)))
        k = len(sorted_cosets)
        
        # Create multiplication table of cosets
        grid = np.zeros((k, k), dtype=int)
        for i in range(k):
            for j in range(k):
                # Pick representatives
                a = next(iter(sorted_cosets[i]))
                b = next(iter(sorted_cosets[j]))
                c = self._group.multiply(a, b)
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
        desc = ", ".join([f"C{i}={{{','.join(self._group.label(e) for e in sorted(sorted_cosets[i]))}}}" for i in range(min(k, 4))])
        if k > 4: desc += "..."
        self.ax.text(0.5, -0.15, desc, ha='center', va='top', fontsize=8, color='#c9d1d9', transform=self.ax.transAxes, wrap=True)
        
        self.canvas.draw()
