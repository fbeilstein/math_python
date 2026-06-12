import tkinter as tk
from tkinter import messagebox
import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel

class Level4Hack(BaseLevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        tk.Label(self, text="L4: Hacking RSA (Factorization)", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="#ff5555").pack(pady=10)
        
        desc = ("RSA security relies entirely on the difficulty of factoring large numbers.\n"
                "If someone uses a weak key (e.g., 32-bit or 48-bit), we can factor 'n' back into 'p' and 'q'\n"
                "using simple Trial Division, reconstruct the private key, and read their messages!")
        tk.Label(self, text=desc, font=("Arial", 12), bg="#1e1e1e", fg="white", justify=tk.CENTER).pack(pady=10)
        
        # Intercepted Data Frame
        intercept_frame = tk.Frame(self, bg="#2d2d30", bd=2, relief=tk.SUNKEN)
        intercept_frame.pack(fill=tk.X, padx=50, pady=10)
        
        tk.Label(intercept_frame, text="Intercepted Public Key (e, n):", font=("Arial", 12, "bold"), bg="#2d2d30", fg="white").pack(pady=(10, 0))
        self.lbl_pub = tk.Label(intercept_frame, text="Generate target to intercept...", font=("Courier", 14), bg="#2d2d30", fg="#f1fa8c")
        self.lbl_pub.pack(pady=5)
        
        tk.Label(intercept_frame, text="Intercepted Ciphertext:", font=("Arial", 12, "bold"), bg="#2d2d30", fg="white").pack()
        self.lbl_cipher = tk.Label(intercept_frame, text="None", font=("Courier", 14), bg="#2d2d30", fg="#ff79c6")
        self.lbl_cipher.pack(pady=(5, 10))
        
        # Controls
        ctrl_frame = tk.Frame(self, bg="#1e1e1e")
        ctrl_frame.pack(pady=10)
        
        tk.Button(ctrl_frame, text="1. Intercept New 32-bit Target", bg="#6272a4", fg="white", font=("Arial", 12), width=25, command=lambda: self.gen_target(32)).pack(side=tk.LEFT, padx=10)
        tk.Button(ctrl_frame, text="2. Intercept New 48-bit Target", bg="#6272a4", fg="white", font=("Arial", 12), width=25, command=lambda: self.gen_target(48)).pack(side=tk.LEFT, padx=10)
        
        tk.Button(self, text="HACK THE CODE", font=("Arial", 16, "bold"), bg="#ff5555", fg="white", command=self.hack_target).pack(pady=10)
        
        self.output_text = tk.Text(self, font=("Courier", 12), bg="#2d2d30", fg="#50fa7b", height=10, width=80)
        self.output_text.pack(pady=10)
        
        self.target_pub = None
        self.target_cipher = None
        self.secret_msg = None

    def gen_target(self, bits):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"[*] Generating {bits}-bit RSA keys for target...\n")
        self.update()
        
        pub, priv = tasks.generate_keypair(bits)
        self.target_pub = pub
        
        # Create a secret message and encrypt it
        # For small keys, the message must fit within the modulus! 
        # 32 bits = 4 bytes max. 48 bits = 6 bytes max.
        if bits <= 32:
            messages = ["Hi!", "Ok", "Cat", "Dog", "Yes", "No", "007"] # Max 3 bytes
        else:
            messages = ["Hello", "Agent", "Safe", "Code", "Run!", "Math"] # Max 5 bytes
            
        import random
        self.secret_msg = random.choice(messages)
        m_int = int.from_bytes(self.secret_msg.encode('utf-8'), 'big')
        
        # Sanity check
        if m_int >= pub[1]:
            # If randomly too big, just truncate the integer slightly
            m_int = pub[1] - 1
            self.secret_msg = "[TRUNCATED]"
        
        self.target_cipher = tasks.encrypt(m_int, pub)
        
        self.lbl_pub.config(text=f"e = {pub[0]}\nn = {pub[1]}")
        self.lbl_cipher.config(text=str(self.target_cipher))
        
        self.output_text.insert(tk.END, "[*] Target generated and message intercepted successfully.\n")
        
    def hack_target(self):
        if not self.target_pub:
            messagebox.showwarning("Warning", "Generate a target first!")
            return
            
        self.output_text.insert(tk.END, f"\n[*] Commencing factorization attack on n = {self.target_pub[1]}...\n")
        self.update()
        
        import time
        start_t = time.time()
        
        try:
            m_dec_int = tasks.hack_rsa(self.target_pub, self.target_cipher)
            elapsed = time.time() - start_t
            
            self.output_text.insert(tk.END, f"[+] Factorization successful! (Time: {elapsed:.3f}s)\n")
            
            # Integer -> Bytes -> String
            dec_bytes = m_dec_int.to_bytes((m_dec_int.bit_length() + 7) // 8, 'big')
            dec_msg = dec_bytes.decode('utf-8')
            
            self.output_text.insert(tk.END, f"\n[!!!] SECRET MESSAGE RECOVERED: '{dec_msg}'\n")
            
            if dec_msg == self.secret_msg:
                self.output_text.insert(tk.END, "\n✓ SUCCESS: The hack was perfectly executed.")
            else:
                self.output_text.insert(tk.END, "\n✗ FAILED: The decrypted message is incorrect.")
                
        except Exception as e:
            self.output_text.insert(tk.END, f"\n✗ ERROR: Hack failed. {e}")

# ==========================================
# UNIT TESTS
# ==========================================
class TestLevel4Hack(unittest.TestCase):
    
    def test_l4_factorize(self):
        # 15 = 3 * 5
        res = tasks.factorize(15)
        self.assertIsNotNone(res)
        self.assertEqual(set(res), {3, 5})
        
        # Test a slightly larger number (p=101, q=103)
        res = tasks.factorize(10403)
        self.assertIsNotNone(res)
        self.assertEqual(set(res), {101, 103})

    def test_l4_hack_rsa(self):
        pub, priv = tasks.generate_keypair(32)
        m = 42069
        c = tasks.encrypt(m, pub)
        
        # Now hack it!
        m_hacked = tasks.hack_rsa(pub, c)
        self.assertEqual(m, m_hacked)

if __name__ == '__main__':
    unittest.main()
