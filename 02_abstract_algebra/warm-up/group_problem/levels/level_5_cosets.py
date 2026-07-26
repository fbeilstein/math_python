"""Level 5: Cosets & Normality — compute cosets, visualize partition."""
import tkinter as tk
import numpy as np
from levels.base_level import TabbedLevel
import implementation_tasks as tasks


class Level5Cosets(TabbedLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)

        tk.Label(self.left_panel, text="L5: Cosets & Normality", font=("Arial", 13, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=4)

        tk.Label(self.left_panel, text="Select elements to generate subgroup:", 
                 bg="#1e1e1e", fg="#8b949e", font=("Arial", 9)).pack(pady=2)

        self.elements_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        self.elements_frame.pack(fill=tk.X, padx=4, pady=4)
        
        self.selected_elements = set()
        self.element_buttons = {}

        self.info_label = tk.Label(self.left_panel, text="", font=("Courier", 9),
                                   bg="#1e1e1e", fg="#c9d1d9", wraplength=280, justify=tk.LEFT)
        self.info_label.pack(padx=4, fill=tk.X, pady=4)

        self.setup_matplotlib(figsize=(7, 4))

    def on_group_loaded(self, group):
        self.selected_elements.clear()
        
        # Use first group generator if available as default selection
        if hasattr(group, 'generators') and group.generators:
            self.selected_elements.add(group.generators[0])
        elif len(group.elements) > 1:
            # Fallback to the first non-identity element
            first_non_id = next(g for g in group.elements if g != group.identity_element)
            self.selected_elements.add(first_non_id)
        
        for widget in self.elements_frame.winfo_children():
            widget.destroy()
            
        self.element_buttons.clear()
        
        # Create grid of buttons for elements
        for i, g in enumerate(group.elements):
            btn = tk.Button(self.elements_frame, text=str(g), width=4,
                            bg="#58a6ff" if g in self.selected_elements else "#2d2d30",
                            fg="white", font=("Arial", 9),
                            command=lambda elem=g: self.toggle_element(elem))
            row = i // 5
            col = i % 5
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.element_buttons[g] = btn
            
        self.compute()

    def toggle_element(self, elem):
        if elem in self.selected_elements:
            self.selected_elements.remove(elem)
            self.element_buttons[elem].config(bg="#2d2d30")
        else:
            self.selected_elements.add(elem)
            self.element_buttons[elem].config(bg="#58a6ff")
        
        self.compute()

    def compute(self):
        if self._group is None:
            self.show_error("Load a group first")
            return
        try:
            if self.selected_elements:
                gen_indices = list(self.selected_elements)
            else:
                gen_indices = [self._group.identity_element]
                
            subgroup = tasks.generate_group(gen_indices)
            if subgroup is None:
                self.show_error("generate_group not implemented")
                return
                
            left = tasks.compute_left_cosets(self._group, subgroup)
            if left is None:
                self.show_error("compute_left_cosets not implemented")
                return
                
            right = tasks.compute_right_cosets(self._group, subgroup)
            if right is None:
                self.show_error("compute_right_cosets not implemented")
                return
                
            normal = tasks.is_normal(self._group, subgroup)
        except Exception as e:
            self.show_error(str(e))
            return

        sg_str = ', '.join(str(e) for e in sorted(subgroup, key=str))
        lines = [
            f"H = {{{sg_str}}}  |H|={len(subgroup)}",
            f"[G:H] = {len(left)} cosets",
            f"Normal: {'Yes ✓' if normal else 'No ✗'}",
        ]
        self.info_label.config(text='\n'.join(lines))
        self._draw_cosets(left, right, normal)

    def _draw_cosets(self, left, right, normal):
        self.ax.clear()
        colors = ['#58a6ff', '#7ee787', '#ffa657', '#d2a8ff', '#ff7b72', '#79c0ff', '#f0e68c', '#ff69b4', '#aff5b4', '#ffd8b1']

        n_cosets = len(left)
        self.ax.text(0.25, 0.95, 'Left Cosets (gH)', ha='center', fontsize=12,
                    color='#58a6ff', fontweight='bold', transform=self.ax.transAxes)
        self.ax.text(0.75, 0.95, 'Right Cosets (Hg)', ha='center', fontsize=12,
                    color='#7ee787', fontweight='bold', transform=self.ax.transAxes)

        # Sort cosets so they appear in a consistent order (subgroup first)
        left_sorted = sorted(list(left), key=lambda s: (self._group.identity_element not in s, sorted([str(x) for x in s])))
        right_sorted = sorted(list(right), key=lambda s: (self._group.identity_element not in s, sorted([str(x) for x in s])))

        y_step = 0.8 / max(n_cosets, 1)
        font_sz = max(7, min(11, int(40 / max(n_cosets, 1))))
        pad = max(0.3, min(1.2, 3.0 / max(n_cosets, 1)))

        for ci, coset in enumerate(left_sorted):
            y = 0.85 - ci * y_step
            c = colors[ci % len(colors)]
            elems = ',  '.join(str(e) for e in sorted(coset, key=str))
            self.ax.text(0.25, y, f"{{{elems}}}", fontsize=font_sz, color='black',
                        ha='center', va='center', fontweight='bold', transform=self.ax.transAxes,
                        bbox=dict(boxstyle=f"round,pad={pad}", facecolor=c, alpha=0.8, edgecolor='white', linewidth=1.5))

        for ci, coset in enumerate(right_sorted):
            y = 0.85 - ci * y_step
            # Find matching color by checking overlap with left cosets
            match_idx = ci
            for li, l_coset in enumerate(left_sorted):
                if coset == l_coset:
                    match_idx = li
                    break
            c = colors[match_idx % len(colors)]
            
            elems = ',  '.join(str(e) for e in sorted(coset, key=str))
            self.ax.text(0.75, y, f"{{{elems}}}", fontsize=font_sz, color='black',
                        ha='center', va='center', fontweight='bold', transform=self.ax.transAxes,
                        bbox=dict(boxstyle=f"round,pad={pad}", facecolor=c, alpha=0.8, edgecolor='white', linewidth=1.5))

        self.ax.axvline(x=0.5, color='#30363d', linewidth=2, linestyle='--')

        status = "Normal subgroup ✓ (Left Partitions = Right Partitions)" if normal else "NOT normal ✗ (Left Partitions ≠ Right Partitions)"
        self.ax.set_title(status, color='#7ee787' if normal else '#ff7b72', fontsize=12, pad=15)
        self.ax.axis('off')
        self.canvas.draw()
