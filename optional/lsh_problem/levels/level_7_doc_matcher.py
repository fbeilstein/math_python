import tkinter as tk
from tkinter import ttk, messagebox
from levels.base_level import BaseView, make_hash_func

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
