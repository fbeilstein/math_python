import tkinter as tk
from tkinter import ttk
import sys, os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import group_engine as ge


class BaseLevel:
    """Base class for all levels."""

    def __init__(self, controls_parent, canvas_parent):
        self.controls_parent = controls_parent
        self.canvas_parent = canvas_parent

        self.left_panel = tk.Frame(controls_parent, bg="#1e1e1e")
        self.left_panel.pack(fill=tk.BOTH, expand=True)

        self.right_panel = tk.Frame(canvas_parent, bg="#2d2d30")
        self.right_panel.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        self.left_panel.destroy()
        self.right_panel.destroy()

    def setup_matplotlib(self, figsize=(7, 5)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.fig.patch.set_facecolor('#2d2d30')
        self.ax.set_facecolor('#2d2d30')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_error(self, msg):
        self.ax.clear()
        self.ax.text(0.5, 0.5, f"Error:\n{msg}", color="red", fontsize=12,
                     ha='center', va='center', wrap=True)
        self.ax.axis('off')
        self.canvas.draw()


class TabbedLevel(BaseLevel):
    """Base for Phase 2 levels: adds a group-input tab bar."""

    def __init__(self, controls_parent, canvas_parent):
        super().__init__(controls_parent, canvas_parent)
        self._group = None

        # Tab notebook for group input
        tab_frame = tk.LabelFrame(self.left_panel, text="Group Input", font=("Arial", 9, "bold"),
                                  bg="#1e1e1e", fg="#58a6ff", bd=1)
        tab_frame.pack(fill=tk.X, padx=2, pady=2)

        self.tabs = ttk.Notebook(tab_frame)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("TNotebook", background="#1e1e1e")
        style.configure("TNotebook.Tab", background="#3e3e42", foreground="white", padding=[6, 2])

        # ── Catalog tab ──
        cat_frame = tk.Frame(self.tabs, bg="#1e1e1e")
        self.tabs.add(cat_frame, text="Catalog")
        self.catalog_var = tk.StringVar(value=ge.CATALOG[0][0])
        self.catalog_combo = ttk.Combobox(cat_frame, textvariable=self.catalog_var,
                                          values=[f"{c[0]}: {c[1]}" for c in ge.CATALOG],
                                          state="readonly", width=30)
        self.catalog_combo.pack(padx=4, pady=6)
        self.catalog_combo.current(0)
        self.create_action_buttons(cat_frame, self._load_catalog, "Load")

        # ── Permutations (Visual) tab ──
        vis_frame = tk.Frame(self.tabs, bg="#1e1e1e")
        self.tabs.add(vis_frame, text="Permutations")
        
        from levels.perm_widget import PermutationInput
        self._vis_pool = []
        
        self.perm_input = PermutationInput(vis_frame, n=4, on_submit=self._add_vis_gen, canvas_h=90)
        self.perm_input.pack(fill=tk.X, padx=2, pady=2)
        
        self.vis_pool_label = tk.Label(vis_frame, text="Generators: None", bg="#1e1e1e", fg="#8b949e", font=("Arial", 8))
        self.vis_pool_label.pack(anchor=tk.W, padx=4)
        
        btn_row = tk.Frame(vis_frame, bg="#1e1e1e")
        btn_row.pack(fill=tk.X, pady=2)
        tk.Button(btn_row, text="Clear", bg="#6e3630", fg="white", font=("Arial", 8),
                  command=self._clear_vis_pool).pack(side=tk.LEFT, padx=4)
        self.create_action_buttons(btn_row, self._load_vis_group, "Build Group", side=tk.RIGHT)

        # ── Presentation tab ──
        pres_frame = tk.Frame(self.tabs, bg="#1e1e1e")
        self.tabs.add(pres_frame, text="Presentation")
        r1 = tk.Frame(pres_frame, bg="#1e1e1e")
        r1.pack(fill=tk.X, padx=2, pady=2)
        tk.Label(r1, text="Gen:", bg="#1e1e1e", fg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.pres_gens = tk.Entry(r1, width=12, font=("Courier", 9))
        self.pres_gens.insert(0, "a, b")
        self.pres_gens.pack(side=tk.LEFT, padx=2)
        r2 = tk.Frame(pres_frame, bg="#1e1e1e")
        r2.pack(fill=tk.X, padx=2, pady=2)
        tk.Label(r2, text="Rel:", bg="#1e1e1e", fg="white", font=("Arial", 9)).pack(side=tk.LEFT)
        self.pres_rels = tk.Entry(r2, width=20, font=("Courier", 9))
        self.pres_rels.insert(0, "aaa=e, bb=e, abab=e")
        self.pres_rels.pack(side=tk.LEFT, padx=2)
        self.create_action_buttons(pres_frame, self._load_presentation, "Go")

        # Status label
        self.status_label = tk.Label(self.left_panel, text="No group loaded",
                                     font=("Arial", 9), bg="#1e1e1e", fg="#8b949e")
        self.status_label.pack(pady=2)

    def _load_catalog(self):
        idx = self.catalog_combo.current()
        try:
            self._group = ge.CATALOG[idx][2]()
            self.status_label.config(text=f"Loaded: {ge.CATALOG[idx][0]} (order {self._group.order})", fg="#7ee787")
            self.on_group_loaded(self._group)
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="#ff7b72")

    def _add_vis_gen(self, perm):
        t = tuple(perm)
        if t not in self._vis_pool:
            self._vis_pool.append(t)
            from levels.perm_widget import perm_to_cycle_str
            pool_str = ", ".join(perm_to_cycle_str(list(p)) for p in self._vis_pool)
            self.vis_pool_label.config(text=f"Generators: {pool_str}")

    def _clear_vis_pool(self):
        self._vis_pool = []
        self.vis_pool_label.config(text="Generators: None")

    def _load_vis_group(self):
        if not self._vis_pool:
            self.status_label.config(text="Error: No generators added.", fg="#ff7b72")
            return
        try:
            n = len(self._vis_pool[0])
            self._group = ge.from_permutation_generators(self._vis_pool, n)
            self.status_label.config(text=f"Visual group, order {self._group.order}", fg="#7ee787")
            self.on_group_loaded(self._group)
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="#ff7b72")

    def create_action_buttons(self, parent, load_command, text="Load", side=tk.TOP):
        tk.Button(parent, text=text, bg="#238636", fg="white", font=("Arial", 9, "bold"),
                  command=load_command).pack(side=side, pady=2, padx=4)

    def _load_presentation(self):
        try:
            gens = [g.strip() for g in self.pres_gens.get().split(',') if g.strip()]
            rels = []
            for part in self.pres_rels.get().split(','):
                part = part.strip()
                if '=' in part:
                    lhs, rhs = part.split('=', 1)
                    rels.append((lhs.strip(), rhs.strip() if rhs.strip() != 'e' else ''))

            self._group = ge.from_presentation(gens, rels)
            self.status_label.config(text=f"Presented group, order {self._group.order}", fg="#7ee787")
            self.on_group_loaded(self._group)
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="#ff7b72")



    def on_group_loaded(self, group):
        """Override in subclass to handle group loading."""
        pass
    def update_graph(self, G, pos, draw_callback, title=None, on_node_click=None):
        # Apply a good spring layout once to uncrowd the graph
        import networkx as nx
        if pos is None:
            pos = nx.spring_layout(G, k=1.0, iterations=50)
        
        artists = draw_callback(pos)
        
        if not hasattr(self, 'graph_manager') or self.graph_manager is None:
            self.graph_manager = DraggableGraphManager(self.canvas, self.ax, G, pos, artists, on_node_click)
        else:
            self.graph_manager.G = G
            self.graph_manager.pos = pos
            self.graph_manager.artists = artists
            self.graph_manager.on_node_click = on_node_click
        self.canvas.draw_idle()


class DraggableGraphManager:
    def __init__(self, canvas, ax, G, pos, artists, on_node_click=None):
        self.canvas = canvas
        self.ax = ax
        self.G = G
        self.pos = pos
        self.artists = artists
        self.on_node_click = on_node_click
        self.dragging_node = None
        self.has_moved = False
        
        if hasattr(canvas, '_interactive_cids'):
            for cid in canvas._interactive_cids:
                canvas.mpl_disconnect(cid)
                
        self.cid_press = canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = canvas.mpl_connect('motion_notify_event', self.on_motion)
        canvas._interactive_cids = [self.cid_press, self.cid_release, self.cid_motion]

    def update_artists(self):
        if 'nodes' in self.artists:
            for nodelist, path_col in self.artists['nodes']:
                path_col.set_offsets([self.pos[n] for n in nodelist])
        if 'labels' in self.artists:
            for n, text in self.artists['labels'].items():
                if n in self.pos:
                    text.set_position(self.pos[n])
        if 'edges' in self.artists:
            for u, v, patch in self.artists['edges']:
                if u in self.pos and v in self.pos:
                    patch.set_positions(self.pos[u], self.pos[v])
        
    def on_press(self, event):
        if event.inaxes != self.ax: return
        min_dist = float('inf')
        closest_node = None
        
        if self.canvas.toolbar and self.canvas.toolbar.mode != '': return
        
        for n, (x, y) in self.pos.items():
            dist = (x - event.xdata)**2 + (y - event.ydata)**2
            if dist < min_dist:
                min_dist = dist
                closest_node = n
                
        if min_dist < 0.05:
            self.dragging_node = closest_node
            self.has_moved = False
            self.press_x = event.xdata
            self.press_y = event.ydata
            
    def on_motion(self, event):
        if self.dragging_node is None: return
        if event.inaxes != self.ax: return
        if self.canvas.toolbar and self.canvas.toolbar.mode != '': return
        
        if not self.has_moved:
            dist = (event.xdata - self.press_x)**2 + (event.ydata - self.press_y)**2
            if dist > 0.001:
                self.has_moved = True
                
        self.pos[self.dragging_node] = (event.xdata, event.ydata)
        self.update_artists()
        self.canvas.draw_idle()
        
    def on_release(self, event):
        if self.dragging_node is not None and not self.has_moved and self.on_node_click:
            self.on_node_click(self.dragging_node)
        self.dragging_node = None
