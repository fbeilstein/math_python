import tkinter as tk
import implementation_tasks
from levels.level_3_smoothing import Level3Smoothing

class Level4Experts(Level3Smoothing):
    def setup_custom_ui(self):
        super().setup_custom_ui()
        
        # Expert Dashboard
        self.expert_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.expert_frame.pack(side=tk.LEFT, padx=30)
        
    def reset_model(self):
        super().reset_model()
        self.expert_counts = [{} for _ in range(self.order)]
        self.expert_scores = [0.0] * self.order
        self.active_expert_idx = -1
        
    def make_prediction(self):
        self.expert_predictions = []
        for i in range(self.order):
            # Predict using each expert using fallback logic up to their individual order
            pred = implementation_tasks.predict_with_fallback(self.history, i + 1, self.expert_counts[i])
            self.expert_predictions.append(pred)
            
        self.active_expert_idx = implementation_tasks.get_best_expert(self.expert_scores)
        return self.expert_predictions[self.active_expert_idx]
        
    def update_model(self, char):
        # Update scores first based on previous predictions
        self.expert_scores = implementation_tasks.update_expert_scores(self.expert_scores, self.expert_predictions, char, 0.95)
        
        # Then update counts
        for i in range(self.order):
            implementation_tasks.update_markov_counts(self.history, char, i + 1, self.expert_counts[i])
            
        self.history += char
        
    def update_custom_ui(self):
        super().update_custom_ui()
        
        # Redraw expert dashboard
        for widget in self.expert_frame.winfo_children():
            widget.destroy()
            
        tk.Label(self.expert_frame, text="Expert Scores:", bg="#1e1e1e", fg="gray", font=("Arial", 10)).pack(side=tk.LEFT, padx=(5, 5))
        
        for i in range(self.order):
            score = self.expert_scores[i]
            color = "#00ff00" if i == self.active_expert_idx else "white"
            bg_color = "#3e3e42" if i == self.active_expert_idx else "#1e1e1e"
            lbl = tk.Label(self.expert_frame, text=f"Ord {i+1}: {score:.1f}", bg=bg_color, fg=color, font=("Courier", 12, "bold" if i == self.active_expert_idx else "normal"))
            lbl.pack(side=tk.LEFT, padx=5)
