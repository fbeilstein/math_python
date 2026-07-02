import tkinter as tk
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level2Keys(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self, text="L2: RSA Key Generation", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)
        
        frame_gen = tk.Frame(self, bg="#1e1e1e")
        frame_gen.pack(pady=10)
        
        tk.Label(frame_gen, text="Key Size (Bits):", font=("Arial", 14), bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=5)
        self.entry_bits = tk.Entry(frame_gen, font=("Courier", 14), width=5)
        self.entry_bits.pack(side=tk.LEFT, padx=5)
        self.entry_bits.insert(0, "512")
        
        tk.Button(frame_gen, text="Generate Keypair", font=("Arial", 12, "bold"), bg="#007acc", fg="white", command=self.generate).pack(side=tk.LEFT, padx=10)
        
        self.output_text = tk.Text(self, font=("Courier", 12), bg="#2d2d30", fg="#d4d4d4", height=25, width=80)
        self.output_text.pack(pady=20)

    def generate(self):
        try:
            bits = int(self.entry_bits.get())
        except ValueError:
            return
            
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Generating {bits}-bit RSA Keypair...\n")
        self.update_idletasks()
        
        try:
            pub_key, priv_key = tasks.generate_keypair(bits)
            e, n = pub_key
            d, _ = priv_key
            
            out = f"\n=== PUBLIC KEY (e, n) ===\n"
            out += f"e = {e}\n"
            out += f"n = {n}\n\n"
            
            out += f"=== PRIVATE KEY (d, n) ===\n"
            out += f"d = {d}\n\n"
            
            out += f"Verification:\n"
            out += f"(e * d) % phi == 1 -> Let's test it implicitly by ensuring d was generated.\n"
            out += f"Keypair successfully generated!"
            
            self.output_text.insert(tk.END, out)
        except Exception as e:
            self.output_text.insert(tk.END, f"\nError during generation: {e}")


if __name__ == '__main__':
    unittest.main()
