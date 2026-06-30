import tkinter as tk
from levels.base_level import BaseLevel
import implementation_tasks

class Level1NGram(BaseLevel):
    def setup_custom_ui(self):
        tk.Label(self.top_frame, text="Markov Order (N-Gram):", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=(20, 5))
        self.order_var = tk.StringVar(value="3")
        self.order_entry = tk.Entry(self.top_frame, textvariable=self.order_var, width=5, font=("Arial", 12))
        self.order_entry.pack(side=tk.LEFT)
        tk.Button(self.top_frame, text="Reset & Update", command=self.reset, bg="#007acc", fg="white").pack(side=tk.LEFT, padx=10)
        
    def reset_model(self):
        try:
            val = int(self.order_var.get())
            if val < 1: val = 1
            self.order = val
        except ValueError:
            self.order = 3
            self.order_var.set("3")
            
        self.counts_dict = {}
        self.history = ""
        
    def update_model(self, char):
        implementation_tasks.update_markov_counts(self.history, char, self.order, self.counts_dict)
        self.history += char
        
    def make_prediction(self):
        return implementation_tasks.predict_fixed_order(self.history, self.order, self.counts_dict)
