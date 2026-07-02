import tkinter as tk
from tkinter import ttk
import random
from levels.base_level import BaseView, make_hash_func

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
