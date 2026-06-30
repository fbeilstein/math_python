import tkinter as tk
import math
import collections
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Alphabet:
    def __init__(self):
        self.alphabet = 'אבגדהωψχϕυτσρπξνμλκθηζϵδγβαzyxwvutsrqponmkljihgfedcbaΘΞΩΨΣΛZYXWVUTRPMLKJHGFDCBA'
        self.labels = list(self.alphabet)
    def get_label(self):
        return self.labels.pop() if self.labels else '?'
    def return_label(self, label):
        if label != '?':
            self.labels.append(label)

class Vertex:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.picked = False
        self.non_dockable = False

class Triangle:
    def __init__(self, a, b, c):
        self.vertices = [a, b, c]

class MeshEditorLevel(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.left_frame = tk.Frame(self, width=800, height=800)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.left_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.right_frame = tk.Frame(self, width=400, height=800, bg="#e0e0e0")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        
        control_frame = tk.Frame(self.right_frame, bg="#e0e0e0")
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)
        
        self.show_labels = True
        self.show_negative = False
        self.show_connections = False
        
        self.btn1 = tk.Button(control_frame, text="Labels: ON", command=self.toggle_labels)
        self.btn1.pack(side=tk.LEFT, padx=2)
        self.btn2 = tk.Button(control_frame, text="Negative: OFF", command=self.toggle_negative)
        self.btn2.pack(side=tk.LEFT, padx=2)
        self.btn3 = tk.Button(control_frame, text="Connections: OFF", command=self.toggle_connections)
        self.btn3.pack(side=tk.LEFT, padx=2)
        
        self.fig = Figure(figsize=(5, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis("off")
        self.mpl_canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.mpl_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.allocator = Alphabet()
        self.triangles = []
        
        self.current_point = None
        self.current_triangle = None
        self.glue_candidate_1 = None
        self.forbidden = None
        self.prev_mouse_pos = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.canvas.bind("<ButtonPress-3>", self.on_right_press)
        self.canvas.bind("<B3-Motion>", self.on_right_drag)
        
        # We bind to parent (which is the main frame, maybe we should bind to canvas or self)
        # to ensure key events are caught
        self.bind_all("<KeyRelease-Control_L>", self.on_ctrl_release)
        self.bind_all("<KeyRelease-Control_R>", self.on_ctrl_release)
        
        self.draw_loop_id = None
        self.draw_loop()

    def destroy(self):
        if self.draw_loop_id:
            self.after_cancel(self.draw_loop_id)
        super().destroy()

    def toggle_labels(self):
        self.show_labels = not self.show_labels
        self.btn1.config(text=f"Labels: {'ON' if self.show_labels else 'OFF'}")
        
    def toggle_negative(self):
        self.show_negative = not self.show_negative
        self.btn2.config(text=f"Negative: {'ON' if self.show_negative else 'OFF'}")
        self.canvas.config(bg="black" if self.show_negative else "white")

    def toggle_connections(self):
        self.show_connections = not self.show_connections
        self.btn3.config(text=f"Connections: {'ON' if self.show_connections else 'OFF'}")

    def get_closest_vertice(self, x, y, rr=225):
        for i, t in enumerate(self.triangles):
            for j, v in enumerate(t.vertices):
                if (v.x - x)**2 + (v.y - y)**2 < rr:
                    return i, j
        return None

    def get_closest_vertice_except_self(self, v, rr=225):
        for i, t in enumerate(self.triangles):
            for j, u in enumerate(t.vertices):
                if u is not v and (u.x - v.x)**2 + (u.y - v.y)**2 < rr:
                    return i, j
        return None

    def return_label_if_poss(self, label):
        for t in self.triangles:
            for v in t.vertices:
                if v.label == label:
                    return
        self.allocator.return_label(label)

    def add_triangle(self, x, y):
        s = 30
        self.triangles.append(Triangle(
            Vertex(x, y + s, self.allocator.get_label()),
            Vertex(x - s, y - s, self.allocator.get_label()),
            Vertex(x + s, y - s, self.allocator.get_label())
        ))
        self.recalculate_math()

    def delete_triangle(self, i):
        t = self.triangles[i]
        labels = [v.label for v in t.vertices]
        if i + 1 != len(self.triangles):
            self.triangles[i], self.triangles[-1] = self.triangles[-1], self.triangles[i]
        self.triangles.pop()
        for lbl in labels:
            self.return_label_if_poss(lbl)
        self.recalculate_math()

    def pick_triangle(self, x, y):
        for i, t in enumerate(self.triangles):
            if self.is_inside_triangle(t, x, y):
                return i
        return None

    def is_inside_triangle(self, t, px, py):
        v0, v1, v2 = t.vertices
        denom = ((v1.y - v2.y) * (v0.x - v2.x) + (v2.x - v1.x) * (v0.y - v2.y))
        if denom == 0: return False
        a = ((v1.y - v2.y) * (px - v2.x) + (v2.x - v1.x) * (py - v2.y)) / denom
        b = ((v2.y - v0.y) * (px - v2.x) + (v0.x - v2.x) * (py - v2.y)) / denom
        c = 1 - a - b
        return a >= 0 and b >= 0 and c >= 0

    def can_glue(self, x_idx, y_idx):
        vt_x = self.triangles[x_idx[0]].vertices[x_idx[1]]
        vt_y = self.triangles[y_idx[0]].vertices[y_idx[1]]
        for i, t in enumerate(self.triangles):
            has_y = sum(1 for v in t.vertices if v is vt_y)
            has_x_label = sum(1 for v in t.vertices if v.label == vt_x.label)
            if has_y > 0 and has_x_label > 0:
                self.forbidden = x_idx
                vt_x.non_dockable = True
                return False
        return True

    def glue(self, x_idx, y_idx):
        vt_x = self.triangles[x_idx[0]].vertices[x_idx[1]]
        vt_y = self.triangles[y_idx[0]].vertices[y_idx[1]]
        vt_y.label = vt_x.label
        self.return_label_if_poss(vt_y.label)

    def change_all_v1_to_v2(self, v1, v2):
        if v1 is v2: return
        label = v1.label
        for t in self.triangles:
            common = sum(1 for v in t.vertices if v is v1 or v is v2)
            if common == 2: return
        for t in self.triangles:
            for j in range(3):
                if t.vertices[j] is v1:
                    t.vertices[j] = v2
        self.return_label_if_poss(label)

    def split(self, v_idx):
        v = self.triangles[v_idx[0]].vertices[v_idx[1]]
        label = v.label
        new_vertices = set()
        n_new = 0
        for t in self.triangles:
            for j in range(3):
                if t.vertices[j] is v:
                    new_v = Vertex(v.x, v.y, self.allocator.get_label())
                    t.vertices[j] = new_v
                    new_vertices.add(new_v)
                    n_new += 1
        self.return_label_if_poss(label)
        if n_new > 1:
            for t in self.triangles:
                for j in range(3):
                    if t.vertices[j] in new_vertices:
                        mx = sum(u.x for u in t.vertices) / 3
                        my = sum(u.y for u in t.vertices) / 3
                        dx, dy = t.vertices[j].x - mx, t.vertices[j].y - my
                        d = math.hypot(dx, dy)
                        if d != 0:
                            t.vertices[j].x -= int(20 * dx / d)
                            t.vertices[j].y -= int(20 * dy / d)

    def add_grid(self, x, y):
        d = 70
        m, n = 3, 3
        vertices = [[Vertex(x + d * i, y + d * j, self.allocator.get_label()) for j in range(n + 1)] for i in range(m + 1)]
        for i in range(m):
            for j in range(n):
                self.triangles.append(Triangle(vertices[i][j], vertices[i+1][j], vertices[i+1][j+1]))
                self.triangles.append(Triangle(vertices[i][j], vertices[i][j+1], vertices[i+1][j+1]))
        self.recalculate_math()

    def on_press(self, event):
        x, y = event.x, event.y
        self.current_point = self.get_closest_vertice(x, y)
        self.prev_mouse_pos = (x, y)
        
        if (event.state & 0x0008) or (event.state & 0x20000):
            if self.current_point:
                self.split(self.current_point)
                self.recalculate_math()
            return
            
        if event.state & 0x0004:
            if self.current_point:
                if not self.glue_candidate_1:
                    self.glue_candidate_1 = self.current_point
                    self.triangles[self.current_point[0]].vertices[self.current_point[1]].picked = True
                else:
                    if self.can_glue(self.glue_candidate_1, self.current_point):
                        self.glue(self.glue_candidate_1, self.current_point)
                        self.recalculate_math()
                    self.triangles[self.glue_candidate_1[0]].vertices[self.glue_candidate_1[1]].picked = False
                    self.glue_candidate_1 = None
        else:
            if not self.current_point:
                self.current_triangle = self.pick_triangle(x, y)

    def on_right_press(self, event):
        self.prev_mouse_pos = (event.x, event.y)

    def on_right_drag(self, event):
        dx = event.x - self.prev_mouse_pos[0]
        dy = event.y - self.prev_mouse_pos[1]
        self.prev_mouse_pos = (event.x, event.y)
        unique_vertices = set()
        for t in self.triangles:
            for v in t.vertices:
                unique_vertices.add(v)
        for v in unique_vertices:
            v.x += dx
            v.y += dy

    def on_release(self, event):
        self.current_point = None
        self.current_triangle = None
        self.recalculate_math()

    def on_drag(self, event):
        x, y = event.x, event.y
        dx = x - self.prev_mouse_pos[0]
        dy = y - self.prev_mouse_pos[1]
        self.prev_mouse_pos = (x, y)
        
        if self.forbidden:
            self.triangles[self.forbidden[0]].vertices[self.forbidden[1]].non_dockable = False
        self.forbidden = None
        
        if self.current_point:
            t_idx, v_idx = self.current_point
            v = self.triangles[t_idx].vertices[v_idx]
            v.x, v.y = x, y
            closest = self.get_closest_vertice_except_self(v)
            if not (event.state & 0x0001) and closest:
                c_idx = closest
                c_v = self.triangles[c_idx[0]].vertices[c_idx[1]]
                if v.label == c_v.label or self.can_glue(c_idx, self.current_point):
                    self.change_all_v1_to_v2(v, c_v)
        elif self.current_triangle is not None:
            t = self.triangles[self.current_triangle]
            for v in t.vertices:
                v.x += dx
                v.y += dy

    def on_double_click(self, event):
        x, y = event.x, event.y
        if event.state & 0x0001:
            self.add_grid(x, y)
            return
        picked = self.pick_triangle(x, y)
        if picked is not None:
            self.delete_triangle(picked)
        else:
            self.add_triangle(x, y)

    def on_ctrl_release(self, event):
        if self.glue_candidate_1:
            self.triangles[self.glue_candidate_1[0]].vertices[self.glue_candidate_1[1]].picked = False
        self.glue_candidate_1 = None

    def draw_loop(self):
        try:
            self.canvas.delete("all")
        except tk.TclError:
            return # Canvas was destroyed
        
        t_counts = collections.Counter("".join(sorted([v.label for v in t.vertices])) for t in self.triangles)
            
        for t in reversed(self.triangles):
            lbls = "".join(sorted([v.label for v in t.vertices]))
            color = "lightgray" if self.show_negative else "#90EE90"
            if t_counts[lbls] > 1: color = "pink"
            
            pts = []
            for v in t.vertices: pts.extend([v.x, v.y])
            outline = "white" if self.show_negative else "gray"
            self.canvas.create_polygon(pts, fill=color, outline=outline)

        if self.show_connections:
            l = {}
            for t in self.triangles:
                for v in t.vertices:
                    if v.label not in l: l[v.label] = []
                    if (v.x, v.y) not in l[v.label]:
                        l[v.label].append((v.x, v.y))
            color_idx = 0
            colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
            for lbl, pts in l.items():
                if len(pts) > 1:
                    c = colors[color_idx % len(colors)]
                    color_idx += 1
                    for i in range(len(pts)):
                        self.canvas.create_oval(pts[i][0]-6, pts[i][1]-6, pts[i][0]+6, pts[i][1]+6, fill=c, outline="black")
                        for j in range(i+1, len(pts)):
                            self.canvas.create_line(pts[i][0], pts[i][1], pts[j][0], pts[j][1], fill=c, width=3, dash=(6, 4))

        if self.show_labels:
            for t in self.triangles:
                for v in t.vertices:
                    c = "gray" if self.show_negative else ("red" if v.picked else ("#778899" if v.non_dockable else "#F08080"))
                    text_color = "white" if self.show_negative else "black"
                    self.canvas.create_oval(v.x-5, v.y-5, v.x+5, v.y+5, fill=c, outline="")
                    self.canvas.create_text(v.x, v.y+15, text=v.label, fill=text_color, font=("Verdana", 12, "italic"))

        self.draw_loop_id = self.after(50, self.draw_loop)

    def recalculate_math(self):
        # Override this in subclasses to perform specific math logic
        pass
