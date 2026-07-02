import tkinter as tk
import random
from levels.base_level import BaseView

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
