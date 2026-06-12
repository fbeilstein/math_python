import tkinter as tk
import implementation_tasks
from levels.level_4_experts import Level4Experts

class Level5Pi(Level4Experts):
    def setup_custom_ui(self):
        super().setup_custom_ui()
        
        tk.Button(self.top_frame, text="Test Against π", command=self.test_pi, bg="#cc007a", fg="white", font=("Arial", 12, "bold")).pack(side=tk.RIGHT, padx=20)
        
        self.simulating_pi = False
        self.pi_digits = []
        self.pi_index = 0
        
    def reset(self):
        self.simulating_pi = False
        super().reset()
        
    def on_key(self, event):
        if self.focus_get() == self.order_entry or self.simulating_pi:
            return
        super().on_key(event)
        
    def test_pi(self):
        self.reset()
        bits = implementation_tasks.generate_pi_binary_digits(1000)
        self.pi_digits = ['1' if b == '0' else '2' for b in bits]
        self.pi_index = 0
        self.simulating_pi = True
        self.simulate_step()
        
    def simulate_step(self):
        if not self.simulating_pi or self.pi_index >= len(self.pi_digits):
            self.simulating_pi = False
            return
            
        char = self.pi_digits[self.pi_index]
        self.pi_index += 1
        self.process_char(char)
        
        self.after(10, self.simulate_step)
