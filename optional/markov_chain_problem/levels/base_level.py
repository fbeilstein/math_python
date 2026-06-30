import tkinter as tk
import implementation_tasks

class BaseLevel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")
        
        self.user_sequence = []
        self.pred_sequence = []
        self.correct = 0
        self.total = 0
        self.current_prediction = "1"
        
        self.setup_ui()
        
        # Enable keyboard focus
        self.bind("<Key>", self.on_key)
        self.bind("<Button-1>", lambda e: self.focus_set())
        
        self.reset()
        
    def setup_ui(self):
        # Top frame for controls (levels will add things here)
        self.top_frame = tk.Frame(self, bg="#1e1e1e")
        self.top_frame.pack(fill=tk.X, pady=10)
        
        self.score_label = tk.Label(self, text="Accuracy: 0.0% (0/0)", bg="#1e1e1e", fg="#00ff00", font=("Arial", 36, "bold"))
        self.score_label.pack(pady=10)
        
        # Display sequences
        self.canvas = tk.Canvas(self, bg="#2d2d30", height=150, highlightthickness=1, highlightbackground="#444")
        self.canvas.pack(fill=tk.X, padx=20, pady=10)
        
        # Subclass UI hook
        self.setup_custom_ui()
        
    def setup_custom_ui(self):
        pass

    def reset(self):
        self.user_sequence = []
        self.pred_sequence = []
        self.correct = 0
        self.total = 0
        self.reset_model()
        self.current_prediction = self.make_prediction()
        self.update_ui()
        self.focus_set()
        
    def reset_model(self):
        pass
        
    def make_prediction(self):
        return "1"
        
    def update_model(self, char):
        pass

    def on_key(self, event):
        char = event.char
        if char in ['1', '2']:
            self.process_char(char)
            
    def process_char(self, char):
        self.total += 1
        is_correct = (char == self.current_prediction)
        if is_correct:
            self.correct += 1
            
        self.user_sequence.append(char)
        self.pred_sequence.append((self.current_prediction, is_correct))
        
        self.update_model(char)
        self.current_prediction = self.make_prediction()
        self.update_ui()
        
    def update_ui(self):
        acc = (self.correct / self.total) * 100 if self.total > 0 else 0
        self.score_label.config(text=f"Accuracy: {acc:.1f}% ({self.correct}/{self.total})")
        if acc >= 50 or self.total == 0:
            self.score_label.config(fg="#00ff00")
        else:
            self.score_label.config(fg="#ff4444")
            
        self.draw_sequences()
        self.update_custom_ui()
        
    def update_custom_ui(self):
        pass

    def draw_sequences(self):
        self.canvas.delete("all")
        max_chars = 32
        
        disp_user = self.user_sequence[-max_chars:]
        disp_pred = self.pred_sequence[-max_chars:]
        
        start_x = 100
        y_user = 50
        y_pred = 100
        spacing = 25
        
        self.canvas.create_text(start_x - 10, y_user, text="You: ", fill="white", font=("Courier", 24, "bold"), anchor="e")
        self.canvas.create_text(start_x - 10, y_pred, text="AI: ", fill="white", font=("Courier", 24, "bold"), anchor="e")
        
        for i in range(len(disp_user)):
            x = start_x + i * spacing
            self.canvas.create_text(x, y_user, text=disp_user[i], fill="white", font=("Courier", 24, "bold"))
            
            p_char, p_correct = disp_pred[i]
            color = "#00ff00" if p_correct else "#ff4444"
            self.canvas.create_text(x, y_pred, text=p_char, fill=color, font=("Courier", 24, "bold"))
            
        next_i = len(disp_user)
        next_x = start_x + next_i * spacing
        self.canvas.create_text(next_x, y_user, text="?", fill="#888888", font=("Courier", 24, "bold"))
        self.canvas.create_text(next_x, y_pred, text=self.current_prediction, fill="yellow", font=("Courier", 24, "bold"))
