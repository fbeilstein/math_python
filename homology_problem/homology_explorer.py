import tkinter as tk
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import implementation_tasks as tasks

class Alphabet:
    def __init__(self):
        self.alphabet = 'אבגדהωψχϕυτσρπξνμλκθηζϵδγβαzyxwvutsrqponmkljihgfedcbaΘΞΩΨΣΛZYXWVUTRPMLKJHGFDCBA'
        self.labels = list(self.alphabet)
    def get_label(self):
        return self.labels.pop() if self.labels else '?'
    def return_label(self, label):
        if label != '?' and label not in self.labels:
            self.labels.append(label)
            self.labels.sort(key=lambda x: self.alphabet.index(x))

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

class HomologyDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Homology Explorer")
        self.geometry("1600x900")
        
        self.left_frame = tk.Frame(self, width=1100, height=900)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        self.canvas = tk.Canvas(self.left_frame, width=1100, height=900, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.show_labels = True
        self.show_negative = False
        self.show_connections = False
        
        self.right_frame = tk.Frame(self, width=500, height=900, bg="#e0e0e0")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        control_frame = tk.Frame(self.right_frame, bg="#e0e0e0")
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)
        
        btn_frame = tk.Frame(control_frame, bg="#e0e0e0")
        btn_frame.pack()
        
        self.btn1 = tk.Button(btn_frame, text="Labels: ON", command=self.toggle_labels)
        self.btn1.pack(side=tk.LEFT, padx=5)
        self.btn2 = tk.Button(btn_frame, text="Negative: OFF", command=self.toggle_negative)
        self.btn2.pack(side=tk.LEFT, padx=5)
        self.btn3 = tk.Button(btn_frame, text="Connections: OFF", command=self.toggle_connections)
        self.btn3.pack(side=tk.LEFT, padx=5)
        
        self.btn_details = tk.Button(btn_frame, text="Show Details", command=self.show_details)
        self.btn_details.pack(side=tk.LEFT, padx=5)
        
        info_text = (
            "Drag&drop vertices/triangles, close vertices glue together\n"
            "SHIFT+drag: Drag vertices without gluing\n"
            "Double click: Delete/create triangles\n"
            "SHIFT+dblclick: Create grid\n"
            "CTRL+click: Glue vertices\n"
            "ALT+click: Split glued vertices\n"
            "Right-click drag: Move entire canvas\n"
        )
        tk.Label(control_frame, text=info_text, justify=tk.LEFT, bg="#e0e0e0").pack(pady=10)
        
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
        self.bind("<KeyRelease-Control_L>", self.on_ctrl_release)
        self.bind("<KeyRelease-Control_R>", self.on_ctrl_release)
        
        self.add_grid(300, 300)
        self.draw_loop()

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
        old_label = vt_y.label
        vt_y.label = vt_x.label
        self.return_label_if_poss(old_label)

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
        
        if (event.state & 0x0008) or (event.state & 0x20000): # Alt key (Linux Mod1 is 0x0008, Windows is 0x20000)
            if self.current_point:
                self.split(self.current_point)
                self.recalculate_math()
            return
            
        if event.state & 0x0004: # Control key
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
            if not (event.state & 0x0001) and closest: # Shift key avoids gluing
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
        if event.state & 0x0001: # Shift
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
        self.canvas.delete("all")
        
        # Draw Triangles
        t_counts = {}
        for t in self.triangles:
            lbls = "".join(sorted([v.label for v in t.vertices]))
            t_counts[lbls] = t_counts.get(lbls, 0) + 1
            
        for t in reversed(self.triangles):
            lbls = "".join(sorted([v.label for v in t.vertices]))
            color = "lightgray" if self.show_negative else "#90EE90"
            if t_counts[lbls] > 1: color = "pink"
            
            pts = []
            for v in t.vertices: pts.extend([v.x, v.y])
            outline = "white" if self.show_negative else "gray"
            self.canvas.create_polygon(pts, fill=color, outline=outline)

        # Draw Connections
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

        # Draw Vertices
        if self.show_labels:
            for t in self.triangles:
                for v in t.vertices:
                    c = "gray" if self.show_negative else ("red" if v.picked else ("#778899" if v.non_dockable else "#F08080"))
                    text_color = "white" if self.show_negative else "black"
                    self.canvas.create_oval(v.x-5, v.y-5, v.x+5, v.y+5, fill=c, outline="")
                    self.canvas.create_text(v.x, v.y+15, text=v.label, fill=text_color, font=("Verdana", 12, "italic"))

        self.after(50, self.draw_loop)

    def recalculate_math(self):
        self.ax.clear()
        self.ax.axis("off")
        
        tt = ["".join(sorted([v.label for v in t.vertices])) for t in self.triangles]
        if not tt:
            self.mpl_canvas.draw()
            return
            
        if len(set(tt)) != len(tt):
            self.ax.text(0.1, 0.9, f"Duplicate triangle detected: {max(set(tt), key=tt.count)}", color="red", fontsize=14)
            self.mpl_canvas.draw()
            return

        simplices = tasks.get_complex(tt)
        ch0 = [s for s in simplices if len(s) == 1]
        ch1 = [s for s in simplices if len(s) == 2]
        ch2 = [s for s in simplices if len(s) == 3]
        
        b1 = tasks.calculate_boundary(ch1, ch0)
        b2 = tasks.calculate_boundary(ch2, ch1)
        
        h0, h1, h2, torsion = tasks.compute_homology(len(ch0), len(ch1), len(ch2), b1['rank'], b2['rank'], b2['torsion'])
        
        self.last_math_data = {
            'tt': tt, 'ch0': ch0, 'ch1': ch1, 'ch2': ch2,
            'b1': b1, 'b2': b2
        }
        
        out_txt = "Homology Groups:\n"
        out_txt += f"$H_0(K) \\cong \\mathbb{{Z}}^{h0}$\n"
        out_txt += f"$H_1(K) \\cong \\mathbb{{Z}}^{h1}$"
        if torsion:
            for t in torsion: out_txt += f"$\\oplus \\mathbb{{Z}}_{{{abs(t)}}}$"
        out_txt += "\n"
        out_txt += f"$H_2(K) \\cong \\mathbb{{Z}}^{h2}$\n\n"
        out_txt += f"Connected Components: {h0}\n"
        out_txt += f"Holes: {h1}\n"
        out_txt += f"Voids: {h2}\n"
        
        self.ax.text(0.05, 0.9, out_txt, fontsize=14, va="top", wrap=True)
        
        ch_str = (
            r"$\underset{\mathrm{dim}=0}{\emptyset} "
            r"\underset{\mathrm{rank}=0}{\overset{\partial_3}{\longrightarrow}} "
            r"\underset{\mathrm{dim}=" + str(len(ch2)) + r"}{C_2} "
            r"\underset{\mathrm{rank}=" + str(b2['rank']) + r"}{\overset{\partial_2}{\longrightarrow}} "
            r"\underset{\mathrm{dim}=" + str(len(ch1)) + r"}{C_1} "
            r"\underset{\mathrm{rank}=" + str(b1['rank']) + r"}{\overset{\partial_1}{\longrightarrow}} "
            r"\underset{\mathrm{dim}=" + str(len(ch0)) + r"}{C_0} "
            r"\underset{\mathrm{rank}=0}{\overset{\partial_0}{\longrightarrow}} "
            r"\underset{\mathrm{dim}=0}{\{0\}}$"
        )
        self.ax.text(0.05, 0.3, ch_str, fontsize=14, va="top")
        
        self.mpl_canvas.draw()

    def show_details(self):
        if not hasattr(self, 'last_math_data'):
            return
            
        data = self.last_math_data
        tt = data['tt']
        ch0, ch1, ch2 = data['ch0'], data['ch1'], data['ch2']
        b1, b2 = data['b1'], data['b2']
        
        top = tk.Toplevel(self)
        top.title("Homology Details")
        top.geometry("800x600")
        
        text = tk.Text(top, font=("Courier", 12), wrap=tk.NONE)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(top, command=text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scrollbar.set)
        
        details = f"Triangles: {', '.join(tt)}\n\n"
        details += f"0-chain: {', '.join(ch0)}\n"
        details += f"1-chain: {', '.join(ch1)}\n"
        details += f"2-chain: {', '.join(ch2)}\n\n"
        details += "0-boundary: 0\n\n"
        
        def format_matrix(m, v, k):
            if not m or not m[0]: return "0\n"
            import numpy as np
            # Create row labels
            row_labels = [f"k_{x}" for x in v]
            # Create col labels
            col_labels = "       " + " ".join([f"{x:>4}" for x in k]) + "\n"
            
            s = col_labels
            s += "-------" + "-" * (5 * len(k)) + "\n"
            for i in range(len(m)):
                row_str = " ".join([f"{val:>4}" for val in m[i]])
                s += f"{row_labels[i]:<5} | {row_str}\n"
            return s + "\n"

        details += "1-boundary:\n" + format_matrix(b1['m'], b1['v'], b1['k'])
        details += f"Smith = {b1['smith_invs']}\n\n"
        details += "2-boundary:\n" + format_matrix(b2['m'], b2['v'], b2['k'])
        details += f"Smith = {b2['smith_invs']}\n"
        
        text.insert(tk.END, details)
        text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = HomologyDashboard()
    app.mainloop()
