"""Level 7: Homomorphisms & Kernels — funnel diagram."""
import tkinter as tk
import numpy as np
from levels.base_level import TabbedLevel
import implementation_tasks as tasks
import group_engine as ge


# Predefined homomorphisms for exploration
PRESETS = [
    ("ℤ₆ → ℤ₃ (mod 3)", lambda: (ge.from_Zn(6), ge.from_Zn(3), [i % 3 for i in range(6)])),
    ("ℤ₆ → ℤ₂ (mod 2)", lambda: (ge.from_Zn(6), ge.from_Zn(2), [i % 2 for i in range(6)])),
    ("S₃ → ℤ₂ (sign)", lambda: _s3_sign()),
    ("ℤ₄ → ℤ₂ (mod 2)", lambda: (ge.from_Zn(4), ge.from_Zn(2), [i % 2 for i in range(4)])),
]


def _s3_sign():
    G = ge.from_Sn(3)
    H = ge.from_Zn(2)
    # sign: even permutations → 0, odd → 1
    from itertools import permutations
    perms = list(permutations(range(3)))
    phi = []
    for p in perms:
        # count inversions
        inv = sum(1 for i in range(3) for j in range(i+1, 3) if p[i] > p[j])
        phi.append(inv % 2)
    return G, H, phi


class Level7Homomorphisms(TabbedLevel):
    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)

        tk.Label(self.left_panel, text="L7: Kernels & Images", font=("Arial", 13, "bold"),
                 bg="#1e1e1e", fg="white").pack(pady=4)

        self._group_G = None
        self._group_H = None
        self.partial_phi = {}
        self.mapping_start_node = None



        tk.Label(self.left_panel, text="Mapping Controls:", bg="#1e1e1e", fg="#8b949e", font=("Arial", 9)).pack(pady=(10,0))
        ctrl_row = tk.Frame(self.left_panel, bg="#1e1e1e")
        ctrl_row.pack(fill=tk.X, padx=4, pady=2)
        tk.Button(ctrl_row, text="Deduce Rest", bg="#a371f7", fg="white", font=("Arial", 9, "bold"),
                  command=self.deduce_rest).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(ctrl_row, text="Clear Arrows", bg="#da3633", fg="white", font=("Arial", 9, "bold"),
                  command=self.clear_arrows).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.info_label = tk.Label(self.left_panel, text="Load G and H to begin.", font=("Courier", 9),
                                   bg="#1e1e1e", fg="#c9d1d9", wraplength=280, justify=tk.LEFT)
        self.info_label.pack(padx=4, fill=tk.X, pady=8)

        self.setup_matplotlib(figsize=(7, 5))
        
        if not hasattr(self, '_click_cid'):
            self._click_cid = self.canvas.mpl_connect('button_press_event', self.on_click)

    def create_action_buttons(self, parent, load_command, text="Load", side=tk.TOP):
        btn_row = tk.Frame(parent, bg="#1e1e1e")
        btn_row.pack(side=side, fill=tk.X, pady=2)
        tk.Button(btn_row, text="Set as Source (G)", bg="#1f6feb", fg="white", font=("Arial", 9, "bold"),
                  command=lambda: self.set_source_cmd(load_command)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(btn_row, text="Set as Target (H)", bg="#238636", fg="white", font=("Arial", 9, "bold"),
                  command=lambda: self.set_target_cmd(load_command)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    def on_group_loaded(self, group):
        pass # Group is loaded into self._group by TabbedLevel. Wait for user to set as G or H.

    def set_source_cmd(self, load_command):
        load_command()
        if self._group is None: return
        self._group_G = self._group
        self.partial_phi.clear()
        self.mapping_start_node = None
        self.update_view()

    def set_target_cmd(self, load_command):
        load_command()
        if self._group is None: return
        self._group_H = self._group
        self.partial_phi.clear()
        self.mapping_start_node = None
        self.update_view()

    def clear_arrows(self):
        self.partial_phi.clear()
        self.mapping_start_node = None
        self.update_view()

    def check_consistency(self, phi):
        _, err = tasks.deduce_homomorphism(self._group_G, self._group_H, phi)
        return err

    def deduce_rest(self):
        if not self._group_G or not self._group_H: return
        phi, err = tasks.deduce_homomorphism(self._group_G, self._group_H, self.partial_phi)
        self.partial_phi = phi
        self.mapping_start_node = None
        if err:
            self.show_error(err)
            # Re-draw the partial map after 2 seconds or let the user see the error
            self.canvas.get_tk_widget().after(4000, self.update_view)
        else:
            self.update_view()

    def on_click(self, event):
        if not self._group_G or not self._group_H or not event.inaxes: return
        
        # Check if clicked G node
        clicked_g = None
        min_dist_g = float('inf')
        for g, (nx, ny) in self._node_pos_G.items():
            d = (nx - event.xdata)**2 + (ny - event.ydata)**2
            if d < min_dist_g:
                min_dist_g = d
                clicked_g = g
                
        # Check if clicked H node
        clicked_h = None
        min_dist_h = float('inf')
        for h, (nx, ny) in self._node_pos_H.items():
            d = (nx - event.xdata)**2 + (ny - event.ydata)**2
            if d < min_dist_h:
                min_dist_h = d
                clicked_h = h
                
        threshold = 0.01 # squared distance
        
        if min_dist_g < threshold:
            if event.button == 3:  # Right-click
                if clicked_g in self.partial_phi:
                    del self.partial_phi[clicked_g]
                self.mapping_start_node = None
                self.update_view()
            else:
                self.mapping_start_node = clicked_g
                self.update_view()
        elif min_dist_h < threshold and event.button == 1:
            if self.mapping_start_node is not None:
                start_node = self.mapping_start_node
                old_val = self.partial_phi.get(start_node)
                
                self.partial_phi[start_node] = clicked_h
                self.mapping_start_node = None
                
                err = self.check_consistency(self.partial_phi)
                if err:
                    if old_val is not None:
                        self.partial_phi[start_node] = old_val
                    else:
                        del self.partial_phi[start_node]
                    self.show_error(err)
                    self.canvas.get_tk_widget().after(4000, self.update_view)
                    return
                    
                self.update_view()
            else:
                self.mapping_start_node = None
                self.update_view()
        else:
            self.mapping_start_node = None
            self.update_view()

    def update_view(self):
        self.ax.clear()
        if not self._group_G or not self._group_H:
            self.ax.text(0.5, 0.5, "Please set both Source (G) and Target (H)\nusing the Group Input tab.", 
                         color="#8b949e", fontsize=12, ha='center', va='center')
            self.ax.axis('off')
            self.canvas.draw()
            return

        is_complete = len(self.partial_phi) == self._group_G.order
        is_homo = False
        if is_complete:
            is_homo = tasks.is_homomorphism(self._group_G, self._group_H, self.partial_phi)

        kernel = tasks.compute_kernel(self._group_G, self._group_H, self.partial_phi)
        image = tasks.compute_image(self._group_G, self._group_H, self.partial_phi)

        # Update info panel
        lines = [
            f"Source G: order {self._group_G.order}",
            f"Target H: order {self._group_H.order}",
            f"Arrows drawn: {len(self.partial_phi)} / {self._group_G.order}",
        ]
        if is_complete:
            lines.append(f"Homomorphism: {'✓' if is_homo else '✗'}")
            k_str = ', '.join(self._group_G.label(e) for e in sorted(kernel))
            i_str = ', '.join(self._group_H.label(e) for e in sorted(image))
            lines.append(f"ker(φ) = {{{k_str}}}  |ker|={len(kernel)}")
            lines.append(f"im(φ) = {{{i_str}}}  |im|={len(image)}")
            
        self.info_label.config(text='\n'.join(lines))

        # ── Canvas Drawing ──
        colors = ['#58a6ff', '#7ee787', '#ffa657', '#d2a8ff', '#ff7b72', '#79c0ff', '#f0e68c', '#ff69b4']
        
        # Sort elements in G based on their mapped target in H (to create fibers/bubbles)
        # Unmapped elements go to the bottom
        def sort_key_g(g):
            if g in self.partial_phi:
                return (0, self.partial_phi[g], g)
            return (1, 0, g)
            
        g_elements = sorted(range(self._group_G.order), key=sort_key_g)
        
        x_g, x_h = 0.2, 0.8
        g_spacing = min(0.8 / max(self._group_G.order, 1), 0.08)
        h_spacing = min(0.8 / max(self._group_H.order, 1), 0.1)
        g_y_start = 0.5 + (self._group_G.order - 1) * g_spacing / 2
        h_y_start = 0.5 + (self._group_H.order - 1) * h_spacing / 2

        self._node_pos_G = {}
        self._node_pos_H = {}
        h_colors = {i: colors[i % len(colors)] for i in range(self._group_H.order)}

        # Draw Fibers (Bubbles) for G
        current_target = None
        bubble_start_y = None
        for i, g in enumerate(g_elements):
            y = g_y_start - i * g_spacing
            target = self.partial_phi.get(g)
            
            # Draw bubble background
            if target != current_target or i == 0:
                if bubble_start_y is not None and current_target is not None:
                    bubble_end_y = g_y_start - (i-1) * g_spacing
                    mid_y = (bubble_start_y + bubble_end_y) / 2
                    height = bubble_start_y - bubble_end_y + g_spacing
                    import matplotlib.patches as patches
                    rect = patches.FancyBboxPatch((x_g - 0.08, mid_y - height/2), 0.16, height,
                                                  boxstyle="round,pad=0.02",
                                                  facecolor=h_colors[current_target], alpha=0.3, edgecolor='none')
                    self.ax.add_patch(rect)
                current_target = target
                bubble_start_y = y
                
        # Last bubble
        if bubble_start_y is not None and current_target is not None:
            bubble_end_y = g_y_start - (len(g_elements)-1) * g_spacing
            mid_y = (bubble_start_y + bubble_end_y) / 2
            height = bubble_start_y - bubble_end_y + g_spacing
            import matplotlib.patches as patches
            rect = patches.FancyBboxPatch((x_g - 0.08, mid_y - height/2), 0.16, height,
                                          boxstyle="round,pad=0.02",
                                          facecolor=h_colors[current_target], alpha=0.3, edgecolor='none')
            self.ax.add_patch(rect)

        # Draw G nodes
        for i, g in enumerate(g_elements):
            y = g_y_start - i * g_spacing
            self._node_pos_G[g] = (x_g, y)
            target = self.partial_phi.get(g)
            c = h_colors[target] if target is not None else '#484f58'
            
            is_kern = g in kernel
            marker = '●' if is_kern else '○'
            fontw = 'bold' if is_kern else 'normal'
            
            if self.mapping_start_node == g:
                c = '#ffd700' # Yellow when selected
                marker = '●'
                
            self.ax.text(x_g, y, f"{marker} {self._group_G.label(g)}", ha='center', va='center',
                        fontsize=10, color=c, fontweight=fontw)

            # Draw arrow
            if target is not None:
                y_target = h_y_start - target * h_spacing
                self.ax.annotate('', xy=(x_h - 0.08, y_target), xytext=(x_g + 0.08, y),
                               arrowprops=dict(arrowstyle='->', color=c, alpha=0.5, lw=1.5))

        # Draw H nodes
        for h in range(self._group_H.order):
            y = h_y_start - h * h_spacing
            self._node_pos_H[h] = (x_h, y)
            c = h_colors[h]
            in_img = h in image
            marker = '■' if in_img else '□'
            self.ax.text(x_h, y, f"{self._group_H.label(h)} {marker}", ha='center', va='center',
                        fontsize=11, color=c, fontweight='bold')

        # Labels
        self.ax.text(x_g, 0.97, 'Source G', ha='center', fontsize=14, color='#58a6ff',
                    fontweight='bold', transform=self.ax.transAxes)
        self.ax.text(x_h, 0.97, 'Target H', ha='center', fontsize=14, color='#7ee787',
                    fontweight='bold', transform=self.ax.transAxes)
                    
        subtitle = "Click an element in G, then an element in H to draw an arrow.\nRight-click a mapped element in G to remove its arrow."
        if self.mapping_start_node is not None:
            subtitle = f"Mapping {self._group_G.label(self.mapping_start_node)} → ... (click a Target)"
        self.ax.text(0.5, 0.02, subtitle, ha='center', fontsize=10, color='#8b949e', transform=self.ax.transAxes)

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        self.canvas.draw()
