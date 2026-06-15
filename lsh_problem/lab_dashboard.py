import tkinter as tk
from tkinter import ttk, messagebox
import time
import hashlib
import sys
import importlib
import numpy as np
import math
import random
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from sklearn.datasets import fetch_20newsgroups
except ImportError:
    messagebox.showerror("Dependency Error", "Please install scikit-learn: pip install scikit-learn")
    sys.exit(1)

def make_hash_func(seed):
    def hash_func(shingle):
        h = hashlib.md5(f"{seed}_{shingle}".encode('utf8'))
        return int(h.hexdigest(), 16)
    return hash_func

class BaseView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.bg_color)
        self.app = app
        
    def get_tasks(self):
        if 'implementation_tasks' in sys.modules:
            importlib.reload(sys.modules['implementation_tasks'])
        import implementation_tasks as tasks
        return tasks

class Level4MinHash(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        top = tk.Frame(self, bg=self.app.bg_color)
        top.pack(fill=tk.X, pady=10)
        
        tk.Label(top, text="Target Jaccard:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT, padx=5)
        self.j_var = tk.DoubleVar(value=0.5)
        self.j_lbl = tk.Label(top, text="0.50", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.j_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.j_var, from_=0.0, to=1.0, orient=tk.HORIZONTAL, command=lambda v: self.j_lbl.config(text=f"{float(v):.2f}")).pack(side=tk.LEFT, padx=5)
        
        tk.Label(top, text="Hash Functions:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT, padx=15)
        self.h_var = tk.IntVar(value=100)
        self.h_lbl = tk.Label(top, text="100", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.h_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.h_var, from_=10, to=500, orient=tk.HORIZONTAL, command=lambda v: self.h_lbl.config(text=str(int(float(v))))).pack(side=tk.LEFT, padx=5)
        
        tk.Button(top, text="Generate Sets & MinHash", bg=self.app.accent_color, fg="white", 
                  command=self.run_sim).pack(side=tk.LEFT, padx=20)
                  
        self.score_lbl = tk.Label(top, text="Set A & B (100 shingles each)", bg=self.app.bg_color, fg="#4ec9b0", font=("Arial", 12, "bold"))
        self.score_lbl.pack(side=tk.LEFT, padx=10)
        
        text_frame = tk.Frame(self, bg=self.app.bg_color)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_a = tk.Text(text_frame, bg=self.app.text_bg, fg=self.app.fg_color, font=("Consolas", 10), width=40)
        self.text_a.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.text_a.tag_config("overlap", foreground="#4ec9b0", font=("Consolas", 10, "bold"))
        
        self.text_b = tk.Text(text_frame, bg=self.app.text_bg, fg=self.app.fg_color, font=("Consolas", 10), width=40)
        self.text_b.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.text_b.tag_config("overlap", foreground="#4ec9b0", font=("Consolas", 10, "bold"))

    def run_sim(self):
        target_j = self.j_var.get()
        num_hashes = int(float(self.h_var.get()))
        
        # J = I / (200 - I)  => I = 200J / (1+J)
        I = int((200 * target_j) / (1.0 + target_j))
        
        shared = [f"shingle_match_{i:03d}" for i in range(I)]
        unique_a = [f"shingle_a_{i:03d}" for i in range(100 - I)]
        unique_b = [f"shingle_b_{i:03d}" for i in range(100 - I)]
        
        set_a = shared + unique_a
        set_b = shared + unique_b
        
        random.shuffle(set_a)
        random.shuffle(set_b)
        
        self.text_a.config(state=tk.NORMAL)
        self.text_a.delete(1.0, tk.END)
        self.text_a.insert(tk.END, "--- SET A ---\n")
        for w in set_a:
            tag = "overlap" if w in shared else ""
            self.text_a.insert(tk.END, w + " ", tag)
        self.text_a.config(state=tk.DISABLED)
        
        self.text_b.config(state=tk.NORMAL)
        self.text_b.delete(1.0, tk.END)
        self.text_b.insert(tk.END, "--- SET B ---\n")
        for w in set_b:
            tag = "overlap" if w in shared else ""
            self.text_b.insert(tk.END, w + " ", tag)
        self.text_b.config(state=tk.DISABLED)
        
        try:
            tasks = self.get_tasks()
            s_a = set(set_a)
            s_b = set(set_b)
            
            exact_j = tasks.jaccard_similarity(s_a, s_b)
            hash_funcs = [make_hash_func(i) for i in range(num_hashes)]
            sig_a = tasks.create_signature(s_a, hash_funcs)
            sig_b = tasks.create_signature(s_b, hash_funcs)
            est_j = tasks.minhash_similarity(sig_a, sig_b)
            
            self.score_lbl.config(text=f"Exact J: {exact_j*100:.1f}%  |  MinHash Est: {est_j*100:.1f}%")
        except Exception as e:
            self.score_lbl.config(text=f"Error: {e}")

class Level5BloomSim(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        self.filter_size = 15
        self.filter_array = [None] * self.filter_size
        
        top = tk.Frame(self, bg=self.app.bg_color)
        top.pack(fill=tk.X, pady=20)
        
        tk.Button(top, text="Hash Random Word", bg=self.app.accent_color, fg="white", 
                  command=self.hash_word, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=20)
        tk.Button(top, text="Reset", bg=self.app.list_bg, fg=self.app.fg_color, 
                  command=self.reset).pack(side=tk.LEFT, padx=10)
                  
        self.info_lbl = tk.Label(top, text="Click to hash a word into the Bloom Filter", 
                                 bg=self.app.bg_color, fg="#4ec9b0", font=("Arial", 12))
        self.info_lbl.pack(side=tk.LEFT, padx=20)
        
        # Grid Container
        grid_frame = tk.Frame(self, bg=self.app.bg_color)
        grid_frame.pack(pady=40)
        
        self.cells = []
        for i in range(self.filter_size):
            col_frame = tk.Frame(grid_frame, bg=self.app.text_bg, highlightbackground="#333333", highlightthickness=1)
            col_frame.grid(row=0, column=i, padx=2)
            
            # Value label
            val_lbl = tk.Label(col_frame, text="", bg=self.app.text_bg, fg=self.app.fg_color, width=6, height=3, font=("Arial", 9, "bold"))
            val_lbl.pack(fill=tk.BOTH, expand=True)
            
            # Index label
            idx_lbl = tk.Label(col_frame, text=str(i), bg="#333333", fg="white", width=6, font=("Arial", 9))
            idx_lbl.pack(fill=tk.X)
            
            self.cells.append(val_lbl)

    def reset(self):
        self.filter_array = [None] * self.filter_size
        for lbl in self.cells:
            lbl.config(text="", bg=self.app.text_bg)
        self.info_lbl.config(text="Reset complete.", fg="#4ec9b0")
        
    def hash_word(self):
        words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "kiwi", "lemon", "mango", "orange", "papaya", "quince"]
        word = random.choice(words)
        
        # Simple string hash mod 15 for visualization
        h = sum(ord(c) for c in word) % self.filter_size
        
        if self.filter_array[h] is None:
            self.filter_array[h] = word
            self.cells[h].config(text=word, bg="#4ec9b0", fg="#1e1e1e") # Green
            self.info_lbl.config(text=f"Word '{word}' hashed to index {h}.", fg="#4ec9b0")
        else:
            old_word = self.filter_array[h]
            self.cells[h].config(text=f"{old_word}\n+\n{word}", bg="#f44747", fg="white") # Red
            self.info_lbl.config(text=f"COLLISION! '{word}' hashed to {h}, which is occupied by '{old_word}'.", fg="#f44747")

class Level6BloomCurve(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        top = tk.Frame(self, bg=self.app.bg_color)
        top.pack(fill=tk.X, pady=10)
        
        tk.Label(top, text="Elements (n):", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT)
        self.n_var = tk.IntVar(value=1000)
        self.n_lbl = tk.Label(top, text="1000", bg=self.app.bg_color, fg=self.app.accent_color, width=5)
        self.n_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.n_var, from_=100, to=5000, command=self.update_n).pack(side=tk.LEFT, padx=5)
        
        tk.Label(top, text="Filter Bits (m):", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT, padx=15)
        self.m_var = tk.IntVar(value=10000)
        self.m_lbl = tk.Label(top, text="10000", bg=self.app.bg_color, fg=self.app.accent_color, width=5)
        self.m_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.m_var, from_=1000, to=50000, command=self.update_m).pack(side=tk.LEFT, padx=5)
        
        self.fig = Figure(figsize=(5, 4), facecolor=self.app.bg_color)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.app.text_bg)
        self.ax.tick_params(colors=self.app.fg_color)
        for spine in self.ax.spines.values():
            spine.set_color(self.app.fg_color)
            
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_plot()
        
    def update_n(self, val):
        self.n_lbl.config(text=str(int(float(val))))
        self.update_plot()
        
    def update_m(self, val):
        self.m_lbl.config(text=str(int(float(val))))
        self.update_plot()
        
    def update_plot(self):
        try:
            tasks = self.get_tasks()
            n = int(float(self.n_var.get()))
            m = int(float(self.m_var.get()))
            
            k_vals = np.arange(1, 20)
            p_vals = [tasks.bloom_false_positive(n, m, k) for k in k_vals]
            
            self.ax.clear()
            self.ax.plot(k_vals, p_vals, marker='o', color=self.app.accent_color)
            
            opt_k = math.log(2) * m / n
            self.ax.axvline(x=opt_k, color="#cca700", linestyle="--", label=f"Optimal k={opt_k:.1f}")
            
            self.ax.set_title(f"Standard Bloom Filter FP Rate (n={n}, m={m})", color=self.app.fg_color)
            self.ax.set_xlabel("Number of Hash Functions (k)", color=self.app.fg_color)
            self.ax.set_ylabel("False Positive Probability", color=self.app.fg_color)
            self.ax.grid(True, color="#333333")
            self.ax.legend()
            self.canvas.draw()
        except Exception:
            pass

class Level7DocMatcher(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        top = tk.Frame(self, bg=self.app.bg_color)
        top.pack(fill=tk.X, pady=10)
        
        tk.Label(top, text="Hash Functions:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT)
        self.hash_var = tk.IntVar(value=100)
        self.hash_lbl = tk.Label(top, text="100", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.hash_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.hash_var, from_=10, to=500, command=lambda v: self.hash_lbl.config(text=str(int(float(v))))).pack(side=tk.LEFT, padx=5)
        
        tk.Label(top, text="Bands:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT, padx=15)
        self.bands_var = tk.IntVar(value=20)
        self.bands_lbl = tk.Label(top, text="20", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.bands_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.bands_var, from_=1, to=100, command=lambda v: self.bands_lbl.config(text=str(int(float(v))))).pack(side=tk.LEFT, padx=5)
        
        tk.Button(top, text="▶ Run Pipeline", bg=self.app.accent_color, fg="white", command=self.run_pipeline).pack(side=tk.LEFT, padx=20)
        self.status_lbl = tk.Label(top, text="", bg=self.app.bg_color, fg="#4ec9b0", font=("Arial", 10, "bold"))
        self.status_lbl.pack(side=tk.LEFT)
        
        main_frame = tk.Frame(self, bg=self.app.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.col_listbox = tk.Listbox(main_frame, bg=self.app.text_bg, fg=self.app.fg_color, width=45, bd=0)
        self.col_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        self.col_listbox.bind('<<ListboxSelect>>', self.on_select)
        
        text_frame = tk.Frame(main_frame, bg=self.app.bg_color)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.text_a = tk.Text(text_frame, bg=self.app.text_bg, fg=self.app.fg_color, font=("Consolas", 10), height=15)
        self.text_a.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.text_b = tk.Text(text_frame, bg=self.app.text_bg, fg=self.app.fg_color, font=("Consolas", 10), height=15)
        self.text_b.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.collisions = []

    def run_pipeline(self):
        if not self.app.docs:
            messagebox.showwarning("Warning", "Data not loaded yet.")
            return
            
        try:
            tasks = self.get_tasks()
            num_hashes = int(float(self.hash_var.get()))
            num_bands = int(float(self.bands_var.get()))
            if num_hashes % num_bands != 0:
                self.status_lbl.config(text=f"Error: {num_hashes} hashes must be perfectly divisible by {num_bands} bands.", fg="#f44747")
                return
                
            self.status_lbl.config(text="Running pipeline...", fg="#cca700")
            self.update()
            
            shingled_docs = [tasks.get_shingles(doc, k=3) for doc in self.app.docs]
            hash_funcs = [make_hash_func(i) for i in range(num_hashes)]
            signatures = [tasks.create_signature(s, hash_funcs) for s in shingled_docs]
            buckets = tasks.lsh_bloom_filter(signatures, num_bands)
            
            candidate_pairs = set()
            for doc_list in buckets.values():
                if len(doc_list) > 1:
                    for i in range(len(doc_list)):
                        for j in range(i+1, len(doc_list)):
                            d1, d2 = min(doc_list[i], doc_list[j]), max(doc_list[i], doc_list[j])
                            candidate_pairs.add((d1, d2))
                            
            self.collisions = []
            for d1, d2 in candidate_pairs:
                sim = tasks.jaccard_similarity(shingled_docs[d1], shingled_docs[d2])
                if sim > 0.4:
                    minhash_sim = tasks.minhash_similarity(signatures[d1], signatures[d2])
                    self.collisions.append((sim, minhash_sim, d1, d2))
                    
            self.collisions.sort(reverse=True)
            self.col_listbox.delete(0, tk.END)
            for sim, minhash_sim, d1, d2 in self.collisions:
                self.col_listbox.insert(tk.END, f"{sim*100:.0f}% Ex | {minhash_sim*100:.0f}% Est (D{d1}-D{d2})")
                
            self.status_lbl.config(text=f"Found {len(self.collisions)} matches.", fg="#4ec9b0")
        except Exception as e:
            self.status_lbl.config(text=f"Error: {e}", fg="#f44747")
            
    def on_select(self, event):
        sel = self.col_listbox.curselection()
        if not sel: return
        sim, minhash_sim, d1, d2 = self.collisions[sel[0]]
        
        self.text_a.config(state=tk.NORMAL)
        self.text_a.delete(1.0, tk.END)
        self.text_a.insert(tk.END, f"--- Document {d1} ---\n{self.app.docs[d1]}")
        self.text_a.config(state=tk.DISABLED)
        
        self.text_b.config(state=tk.NORMAL)
        self.text_b.delete(1.0, tk.END)
        self.text_b.insert(tk.END, f"--- Document {d2} ---\n{self.app.docs[d2]}")
        self.text_b.config(state=tk.DISABLED)

class Level8LSHCurve(BaseView):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        top = tk.Frame(self, bg=self.app.bg_color)
        top.pack(fill=tk.X, pady=10)
        
        tk.Label(top, text="Hash Functions:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT)
        self.hash_var = tk.IntVar(value=100)
        self.hash_lbl = tk.Label(top, text="100", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.hash_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.hash_var, from_=10, to=500, command=self.update_h).pack(side=tk.LEFT, padx=5)
        
        tk.Label(top, text="Bands:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT, padx=15)
        self.bands_var = tk.IntVar(value=20)
        self.bands_lbl = tk.Label(top, text="20", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.bands_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.bands_var, from_=1, to=100, command=self.update_b).pack(side=tk.LEFT, padx=5)
        
        tk.Label(top, text="Target Sim:", bg=self.app.bg_color, fg=self.app.fg_color).pack(side=tk.LEFT, padx=15)
        self.target_var = tk.DoubleVar(value=0.6)
        self.target_lbl = tk.Label(top, text="0.60", bg=self.app.bg_color, fg=self.app.accent_color, width=4)
        self.target_lbl.pack(side=tk.LEFT)
        ttk.Scale(top, variable=self.target_var, from_=0.0, to=1.0, command=self.update_t).pack(side=tk.LEFT, padx=5)
        
        self.fig = Figure(figsize=(5, 4), facecolor=self.app.bg_color)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.app.text_bg)
        self.ax.tick_params(colors=self.app.fg_color)
        for spine in self.ax.spines.values():
            spine.set_color(self.app.fg_color)
            
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_plot()
        
    def update_h(self, val):
        self.hash_lbl.config(text=str(int(float(val))))
        self.update_plot()
        
    def update_b(self, val):
        self.bands_lbl.config(text=str(int(float(val))))
        self.update_plot()
        
    def update_t(self, val):
        self.target_lbl.config(text=f"{float(val):.2f}")
        self.update_plot()
        
    def update_plot(self):
        try:
            tasks = self.get_tasks()
            hashes = int(float(self.hash_var.get()))
            bands = int(float(self.bands_var.get()))
            target_j = self.target_var.get()
            
            if bands <= 0 or hashes <= 0: return
            rows = hashes / bands
            
            j_vals = np.linspace(0, 1.0, 200)
            p_vals = [tasks.collision_probability(j, bands, rows) for j in j_vals]
            threshold = tasks.calculate_threshold(bands, rows)
            
            self.ax.clear()
            self.ax.plot(j_vals, p_vals, color=self.app.accent_color, linewidth=2)
            
            j_fp = j_vals[j_vals < target_j]
            p_fp = [tasks.collision_probability(j, bands, rows) for j in j_fp]
            self.ax.fill_between(j_fp, 0, p_fp, color="#f44747", alpha=0.3, label="False Positives")
            
            j_fn = j_vals[j_vals > target_j]
            p_fn = [tasks.collision_probability(j, bands, rows) for j in j_fn]
            self.ax.fill_between(j_fn, p_fn, 1.0, color="#007acc", alpha=0.3, label="False Negatives")
            
            self.ax.axvline(x=target_j, color="#cca700", linestyle="--", label=f"Target={target_j:.2f}")
            self.ax.axvline(x=threshold, color="#ffffff", linestyle=":", label=f"50% Thresh={threshold:.2f}")
            
            self.ax.set_title("LSH S-Curve & Errors", color=self.app.fg_color)
            self.ax.set_xlabel("Jaccard Similarity", color=self.app.fg_color)
            self.ax.set_ylabel("P(Collision)", color=self.app.fg_color)
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.grid(True, color="#333333")
            self.ax.legend(loc="upper left")
            self.canvas.draw()
        except Exception:
            pass

class LSHDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Probabilistic Document Similarity Dashboard")
        self.geometry("1200x800")
        
        self.bg_color = "#1e1e1e"
        self.fg_color = "#d4d4d4"
        self.accent_color = "#007acc"
        self.list_bg = "#252526"
        self.text_bg = "#1e1e1e"
        self.configure(bg=self.bg_color)
        
        self.docs = []
        
        self.tasks = {
            4: ("MinHash Sandbox", Level4MinHash),
            5: ("Bloom Simulator", Level5BloomSim),
            6: ("Bloom Probability", Level6BloomCurve),
            7: ("Document Matcher", Level7DocMatcher),
            8: ("LSH Probability", Level8LSHCurve)
        }
        
        self.setup_ui()
        self.after(100, self.load_data)

    def setup_ui(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=self.bg_color, bd=0, sashwidth=4)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.sidebar = tk.Frame(self.paned_window, bg=self.list_bg, width=250, bd=1, relief=tk.SUNKEN)
        self.paned_window.add(self.sidebar, minsize=200)
        
        tk.Label(self.sidebar, text="Subproblems", bg=self.list_bg, fg=self.fg_color, font=("Arial", 12, "bold")).pack(pady=10)
        
        self.buttons = {}
        for num, (name, cls) in self.tasks.items():
            btn = tk.Button(self.sidebar, text=f"L{num}: {name}", bg=self.text_bg, fg=self.fg_color, 
                            font=("Arial", 10), anchor="w", padx=10, pady=5,
                            command=lambda n=num: self.switch_view(n))
            btn.pack(fill=tk.X, padx=5, pady=2)
            self.buttons[num] = btn
            
        self.status_lbl = tk.Label(self.sidebar, text="Waiting...", bg=self.list_bg, fg="#cca700", font=("Arial", 9))
        self.status_lbl.pack(side=tk.BOTTOM, pady=10)
        
        self.main_area = tk.Frame(self.paned_window, bg=self.bg_color)
        self.paned_window.add(self.main_area)
        
        self.current_view = None
        self.switch_view(4)

    def switch_view(self, num):
        if self.current_view is not None:
            self.current_view.destroy()
            
        for n, btn in self.buttons.items():
            btn.config(bg=self.text_bg, fg=self.fg_color)
        self.buttons[num].config(bg=self.accent_color, fg="white")
        
        _, view_cls = self.tasks[num]
        self.current_view = view_cls(self.main_area, self)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def load_data(self):
        self.status_lbl.config(text="Downloading 20newsgroups...", fg="#cca700")
        self.update()
        try:
            newsgroups = fetch_20newsgroups(subset='train', categories=['sci.space'], remove=('headers', 'footers', 'quotes'))
            self.docs = newsgroups.data[:300]
            self.status_lbl.config(text=f"Loaded {len(self.docs)} docs", fg="#4ec9b0")
        except Exception as e:
            self.status_lbl.config(text="Error loading data", fg="#f44747")
            messagebox.showerror("Data Error", str(e))

if __name__ == "__main__":
    app = LSHDashboard()
    app.mainloop()
