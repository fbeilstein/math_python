import tkinter as tk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import numpy as np

class BaseLevel:
    def __init__(self, controls_parent, canvas_parent):
        self.controls_parent = controls_parent
        self.canvas_parent = canvas_parent
        self.graph_manager = None
        
        self.left_panel = tk.Frame(controls_parent, bg="#1e1e1e")
        self.left_panel.pack(fill=tk.BOTH, expand=True)
        
        self.right_panel = tk.Frame(canvas_parent, bg="#2d2d30")
        self.right_panel.pack(fill=tk.BOTH, expand=True)
        
    def destroy(self):
        self.left_panel.destroy()
        self.right_panel.destroy()
        
    def add_warning(self):
        warning_frame = tk.Frame(self.left_panel, bg="#4a0000", bd=2, relief=tk.RAISED)
        warning_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(warning_frame, text="⚠️ WARNING", font=("Arial", 10, "bold"), bg="#4a0000", fg="white").pack(pady=(2,0))
        tk.Label(warning_frame, text="Word Problem Undecidable.\nDepth limits enforced.", font=("Arial", 8), bg="#4a0000", fg="#ffcccc").pack(pady=(0,2))

    def setup_graph_ui(self):
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.right_panel)
        self.toolbar.update()
        
        self.graph_manager = None

    def update_graph(self, G, pos, draw_callback, vis_nodes=None, vis_edges=None, title=None):
        # Apply a good spring layout once to uncrowd the graph
        import networkx as nx
        pos = nx.spring_layout(G, pos=pos, k=1.0, iterations=50)
        
        artists = draw_callback(pos)
        
        if self.graph_manager is None:
            self.graph_manager = DraggableGraphManager(self.canvas, self.ax, G, pos, artists)
        else:
            self.graph_manager.G = G
            self.graph_manager.pos = pos
            self.graph_manager.artists = artists
        self.canvas.draw_idle()

class DraggableGraphManager:
    def __init__(self, canvas, ax, G, pos, artists):
        self.canvas = canvas
        self.ax = ax
        self.G = G
        self.pos = pos
        self.artists = artists
        self.dragging_node = None
        
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
            
    def on_motion(self, event):
        if not self.dragging_node: return
        if event.inaxes != self.ax: return
        if self.canvas.toolbar and self.canvas.toolbar.mode != '': return
        
        self.pos[self.dragging_node] = (event.xdata, event.ydata)
        self.update_artists()
        self.canvas.draw_idle()
        
    def on_release(self, event):
        self.dragging_node = None
