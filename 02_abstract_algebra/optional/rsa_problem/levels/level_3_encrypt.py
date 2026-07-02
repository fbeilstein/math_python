import tkinter as tk
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level3Encrypt(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self, text="L3: Fast Modular Exponentiation", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)
        
        self.pub_key = None
        self.priv_key = None
        
        btn_frame = tk.Frame(self, bg="#1e1e1e")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="1. Generate Temporary Keypair (128-bit)", font=("Arial", 12), bg="#3e3e42", fg="white", command=self.gen_keys).pack()
        self.lbl_keys = tk.Label(self, text="No keys loaded.", font=("Arial", 12), bg="#1e1e1e", fg="gray")
        self.lbl_keys.pack()

        test_frame = tk.Frame(self, bg="#1e1e1e")
        test_frame.pack(pady=20)
        
        tk.Label(test_frame, text="Integer Message to Encrypt:", font=("Arial", 14), bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=5)
        self.entry_msg = tk.Entry(test_frame, font=("Courier", 14), width=15)
        self.entry_msg.pack(side=tk.LEFT, padx=5)
        self.entry_msg.insert(0, "42069")
        
        tk.Button(test_frame, text="2. Test Encryption Cycle", font=("Arial", 12, "bold"), bg="#007acc", fg="white", command=self.test_cycle).pack(side=tk.LEFT, padx=10)
        
        self.output_text = tk.Text(self, font=("Courier", 14), bg="#2d2d30", fg="#d4d4d4", height=15, width=70)
        self.output_text.pack(pady=10)

    def gen_keys(self):
        self.pub_key, self.priv_key = tasks.generate_keypair(128)
        self.lbl_keys.config(text=f"Keys Generated! n = {self.pub_key[1]}", fg="#4ec9b0")

    def test_cycle(self):
        if not self.pub_key:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Error: Generate keys first!")
            return
            
        try:
            m = int(self.entry_msg.get())
        except ValueError:
            return
            
        if m >= self.pub_key[1]:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Error: Message must be strictly less than n!")
            return
            
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Original Message (m) : {m}\n\n")
        
        c = tasks.encrypt(m, self.pub_key)
        self.output_text.insert(tk.END, f"Encrypted Cipher (c): {c}\n\n")
        
        m_dec = tasks.decrypt(c, self.priv_key)
        self.output_text.insert(tk.END, f"Decrypted Message (m): {m_dec}\n\n")
        
        if m == m_dec:
            self.output_text.insert(tk.END, "✓ SUCCESS: Decrypted message matches original!")
        else:
            self.output_text.insert(tk.END, "✗ FAILED: Decryption mismatch!")


if __name__ == '__main__':
    unittest.main()
