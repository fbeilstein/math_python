import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
import numpy as np
import importlib
import json
import itertools
from tkinter import filedialog
from io_manager import IOManager
from inspector import Inspector
from ray_source import ParallelRaySource, PointRaySource
from ray_tracer import RayTracer


# Ensure core student functions are available
try:
    import implementation_tasks as tasks
    from implementation_tasks import trace_ray_step
except ImportError:
    print("Warning: implementation_tasks.py not found.")

from lens_object import LensObject
from lens_architect import LensArchitect

class OpticBenchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Physics Lab: Optic Bench")
        self.geometry("1250x750")
        self.lenses = []; self.selected_lens = None; self.dragging_lens = None; self.dragging_source = False
        self.last_mouse_pos = (0, 0); self.start_mouse_angle = 0; self.start_lens_angle = 0
        self.source_type = "parallel"; self.source_pos = np.array([-120.0, 0.0])
        
        # Ruler state
        self.ruler_active = False; self.ruler_start = None; self.ruler_line = None
        
        # Physical Properties Inspector
        self.inspector = Inspector(self, self.draw_scene)

        self.setup_ui()
        self.setup_plot()

    def setup_ui(self):
        toolbar = tk.Frame(self, bg="#f0f0f0", pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(toolbar, text="+ Add Lens", command=self.open_architect).pack(side=tk.LEFT, padx=10)
        tk.Button(toolbar, text="Delete", command=self.delete_lens).pack(side=tk.LEFT, padx=5)
        self.btn_mode = tk.Button(toolbar, text="Mode: Parallel", command=self.toggle_source)
        self.btn_mode.pack(side=tk.LEFT, padx=5)
        
        self.btn_ruler = tk.Button(toolbar, text="Ruler: OFF", command=self.toggle_ruler)
        self.btn_ruler.pack(side=tk.LEFT, padx=10)

        self.fig = Figure(figsize=(8, 6), dpi=100); self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self); self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        # Refractive Index Control
        ttk.Label(toolbar, text="Index (n):").pack(side=tk.LEFT)
        self.n_var = tk.DoubleVar(value=1.52)
        self.spin_n = ttk.Spinbox(toolbar, from_=1.0, to=4.0, increment=0.01, 
                                  textvariable=self.n_var, width=6, command=self.update_n)
        self.spin_n.pack(side=tk.LEFT, padx=5)
        self.spin_n.bind('<Return>', lambda e: self.update_n())
        
        tk.Button(toolbar, text="Save Lab", command=self.dump_bench).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Load Lab", command=self.load_bench).pack(side=tk.LEFT, padx=5)

    def update_n(self):
        """Applies the UI value of n to the selected lens and re-simulates."""
        if self.selected_lens:
            self.selected_lens.n = self.n_var.get()
            self.draw_scene()      # Re-draws rays with new refraction
            self.inspector.sync_with_selected(self.selected_lens)
            #self.update_inspector() # Updates the text panel

    def setup_plot(self):
        self.ax.set_xlim(-150, 150); self.ax.set_ylim(-85, 85); self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3); self.draw_scene()

    def toggle_ruler(self):
        self.ruler_active = not self.ruler_active
        self.btn_ruler.config(text=f"Ruler: {'ON' if self.ruler_active else 'OFF'}")
        if not self.ruler_active: 
            if self.ruler_line:
                try: self.ruler_line.remove()
                except: pass
                self.ruler_line = None
            self.ax.set_title("")
            self.canvas.draw()

        
        
    def open_architect(self): 
        LensArchitect(self, self.add_lens_callback)

    # --- RESTORED ORIGINAL SPAWN LOGIC ---
    def add_lens_callback(self, geometry_data):        
        new_lens = LensObject(geometry_data, x_pos=0, y_pos=0)
        spawn_found = False
        offsets = itertools.product([0, 25, -25, 50, -50], [0, 25, -25, 50, -50])        
        for ox, oy in offsets:
            new_lens.x, new_lens.y = ox, oy
            if not any(new_lens.intersects(other) for other in self.lenses):
                spawn_found = True
                break
                
        if spawn_found: 
            self.lenses.append(new_lens)
            self.selected_lens = new_lens
            self.update_n()
            self.draw_scene()
        else: 
            messagebox.showwarning("Bench Full", "Could not find a clear spot to spawn the lens!")

    def draw_scene(self):
        # Cleanly remove old artists. Use list() to avoid mutation issues.
        all_artists = list(self.ax.patches) + list(self.ax.lines) + list(self.ax.texts)
        for artist in all_artists:
            # Only remove if it's not the active ruler line
            if artist != self.ruler_line:
                try: artist.remove()
                except: pass
        
        for lens in self.lenses:
            color = 'yellow' if lens == self.selected_lens else 'cyan'
            self.ax.add_patch(Polygon(lens.get_transformed_points(), closed=True, facecolor=color, edgecolor='blue', alpha=0.3))
        
        if self.source_type == 'point':
            self.ax.plot(self.source_pos[0], self.source_pos[1], 'go', markersize=8, zorder=30)
        
        self.run_simulation()
        self.canvas.draw()




    


    def run_simulation(self):
        importlib.reload(tasks)
        media = {0: {'n': 1.0}} #; curves = []
        for i, lens in enumerate(self.lenses):
            media[i+1] = {'n': lens.n}

        # 2. Initialize the appropriate Source
        if self.source_type == "parallel":
            source = ParallelRaySource(self.source_pos)
            rays = source.generate_rays()
        else:
            source = PointRaySource(self.source_pos)
            rays = source.generate_rays(self.lenses)

        selected_id = None
        if self.selected_lens:
            try:
                selected_id = self.lenses.index(self.selected_lens) + 1
            except ValueError:
                selected_id = None

        for ray in rays:
            RayTracer.trace(ray, self.lenses)
            # Draw the main ray path (Red)
            pts = np.array(ray.points)
            self.ax.plot(pts[:,0], pts[:,1], 'r-', lw=0.8, alpha=0.5)
            # DRAW VIRTUAL RAYS FOR THE SELECTED LENS ONLY
            if selected_id and selected_id in ray.exits:
                # Check if it's actually a diverging lens
                if self.selected_lens.get_internal_focal_length() < 0:
                    exit_p, exit_d = ray.exits[selected_id]
                    if exit_d is not None:
                        # Draw green dashed line backwards from the exit point
                        v_pts = np.array([exit_p, exit_p - exit_d * 1000])
                        self.ax.plot(v_pts[:,0], v_pts[:,1], 'g--', lw=0.6, alpha=0.3)

    

    def on_press(self, event):
        if event.xdata is None: 
            return
        self.last_mouse_pos = (event.xdata, event.ydata)
        if self.ruler_active:
            self.ruler_start = (event.xdata, event.ydata)
            return
        if self.source_type == "point":
            if np.hypot(event.xdata - self.source_pos[0], event.ydata - self.source_pos[1]) < 10:
                self.dragging_source = True; return
        self.selected_lens = None
        for lens in reversed(self.lenses):
            if lens.contains((event.xdata, event.ydata)):
                self.selected_lens = lens
                self.dragging_lens = lens
                self.n_var.set(self.selected_lens.n)
                dx, dy = event.xdata - lens.x, event.ydata - lens.y
                self.start_mouse_angle = np.degrees(np.arctan2(dy, dx))
                self.start_lens_angle = lens.angle
                break
        self.inspector.sync_with_selected(self.selected_lens)
        self.draw_scene()

    def on_drag(self, event):
        if event.xdata is None: return
        if self.ruler_active and self.ruler_start:
            if self.ruler_line:
                try: self.ruler_line.remove()
                except: pass
            dist = np.hypot(event.xdata - self.ruler_start[0], event.ydata - self.ruler_start[1])
            self.ruler_line, = self.ax.plot([self.ruler_start[0], event.xdata], [self.ruler_start[1], event.ydata], 'k--', lw=2.5)
            self.ax.set_title(f"Measured Distance: {dist:.2f} mm", color='blue')
            self.canvas.draw(); return
        if self.dragging_source:
            self.source_pos = np.array([event.xdata, event.ydata]); self.draw_scene(); return
        if self.dragging_lens:
            old_x, old_y, old_angle = self.dragging_lens.x, self.dragging_lens.y, self.dragging_lens.angle
            if event.button == 1:
                self.dragging_lens.x += event.xdata - self.last_mouse_pos[0]
                self.dragging_lens.y += event.ydata - self.last_mouse_pos[1]
            elif event.button == 3:
                dx, dy = event.xdata - self.dragging_lens.x, event.ydata - self.dragging_lens.y
                self.dragging_lens.angle = self.start_lens_angle + (np.degrees(np.arctan2(dy, dx)) - self.start_mouse_angle)
            collision = False
            for other in self.lenses:
                if other is not self.dragging_lens and self.dragging_lens.intersects(other):
                    collision = True; break
            if collision: self.dragging_lens.x, self.dragging_lens.y, self.dragging_lens.angle = old_x, old_y, old_angle
            self.last_mouse_pos = (event.xdata, event.ydata)
            self.inspector.sync_with_selected(self.selected_lens)
            self.draw_scene()

    def on_release(self, event): 
        self.dragging_lens = None
        self.dragging_source = False
        self.ruler_start = None
        if not self.ruler_active: 
            self.draw_scene()

    def delete_lens(self):
        if self.selected_lens:
            self.lenses.remove(self.selected_lens)
            self.selected_lens = None  # Clear the reference
            self.inspector.sync_with_selected(self.selected_lens)
            self.draw_scene()          # Refresh the plot                
        
    def toggle_source(self):
        self.source_type = "point" if self.source_type == "parallel" else "parallel"
        self.btn_mode.config(text=f"Mode: {self.source_type.capitalize()}"); self.draw_scene()


    def dump_bench(self):
        IOManager.save_lab(self.source_type, self.source_pos, self.lenses)

    def load_bench(self):
        data = IOManager.load_lab()
        if not data: return
        
        self.lenses = []
        self.source_type = data.get("source_type", "parallel")
        self.source_pos = np.array(data.get("source_pos"))
        
        # Delegate object creation back to the class
        for l_data in data["lenses"]:
            self.lenses.append(LensObject.from_dict(l_data))
        
        self.draw_scene()

if __name__ == "__main__":
    OpticBenchApp().mainloop()
