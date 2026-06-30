import tkinter as tk
from tkinter import messagebox
import implementation_tasks as tasks
import re

class SecureChat(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alice & Bob: Secure RSA Chat")
        self.geometry("1200x800")
        self.configure(bg="#1e1e1e")
        
        tk.Label(self, text="Secure RSA Chat Demo", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)
        
        main_frame = tk.Frame(self, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # --- ALICE (LEFT) ---
        alice_frame = tk.Frame(main_frame, bg="#2d2d30", bd=2, relief=tk.SUNKEN)
        alice_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(alice_frame, text="ALICE", font=("Arial", 18, "bold"), bg="#2d2d30", fg="#ff79c6").pack(pady=10)
        
        gen_frame = tk.Frame(alice_frame, bg="#2d2d30")
        gen_frame.pack(pady=5)
        
        self.bit_length_var = tk.StringVar(value="512")
        tk.Label(gen_frame, text="Key Size (bits):", bg="#2d2d30", fg="white").pack(side=tk.LEFT)
        tk.OptionMenu(gen_frame, self.bit_length_var, "16", "32", "48", "64", "128", "256", "512", "1024", "2048").pack(side=tk.LEFT, padx=5)
        tk.Button(gen_frame, text="Generate Keys", bg="#6272a4", fg="white", font=("Arial", 12), command=self.alice_gen_keys).pack(side=tk.LEFT, padx=5)
        
        tk.Label(alice_frame, text="My Public Key (e, n):", bg="#2d2d30", fg="white").pack()
        self.txt_alice_pub = tk.Text(alice_frame, height=3, width=45, bg="#1e1e1e", fg="white")
        self.txt_alice_pub.pack(pady=5)
        
        tk.Label(alice_frame, text="My Private Key (d, n):", bg="#2d2d30", fg="white").pack()
        self.txt_alice_priv = tk.Text(alice_frame, height=3, width=45, bg="#1e1e1e", fg="#f1fa8c")
        self.txt_alice_priv.pack(pady=5)
        
        tk.Label(alice_frame, text="Ciphertext Received (Paste here):", bg="#2d2d30", fg="white").pack(pady=(20,0))
        self.txt_alice_cipher = tk.Text(alice_frame, height=5, width=45, bg="#1e1e1e", fg="#ff5555", font=("Courier", 10))
        self.txt_alice_cipher.pack(pady=5)
        
        tk.Button(alice_frame, text="Decrypt Message", bg="#50fa7b", fg="black", font=("Arial", 12, "bold"), command=self.alice_decrypt).pack(pady=10)
        
        tk.Label(alice_frame, text="Decrypted Message:", bg="#2d2d30", fg="white").pack()
        self.txt_alice_in = tk.Text(alice_frame, height=3, width=45, bg="#1e1e1e", fg="#50fa7b", font=("Arial", 14, "bold"))
        self.txt_alice_in.pack(pady=5)
        
        # --- BOB (RIGHT) ---
        bob_frame = tk.Frame(main_frame, bg="#2d2d30", bd=2, relief=tk.SUNKEN)
        bob_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(bob_frame, text="BOB", font=("Arial", 18, "bold"), bg="#2d2d30", fg="#8be9fd").pack(pady=10)
        
        tk.Label(bob_frame, text="Alice's Public Key (Paste here):", bg="#2d2d30", fg="white").pack()
        self.txt_bob_pub = tk.Text(bob_frame, height=3, width=45, bg="#1e1e1e", fg="white")
        self.txt_bob_pub.pack(pady=5)
        
        tk.Label(bob_frame, text="Write Message to Alice:", bg="#2d2d30", fg="white").pack(pady=(20,0))
        self.entry_bob_msg = tk.Entry(bob_frame, font=("Arial", 14), width=35)
        self.entry_bob_msg.pack(pady=5)
        
        tk.Button(bob_frame, text="Encrypt and Send", bg="#ffb86c", fg="black", font=("Arial", 12, "bold"), command=self.bob_send_msg).pack(pady=10)
        
        tk.Label(bob_frame, text="Raw Ciphertext Sent (Copy to send):", bg="#2d2d30", fg="white").pack()
        self.txt_bob_out = tk.Text(bob_frame, height=5, width=45, bg="#1e1e1e", fg="#ff5555", font=("Courier", 10))
        self.txt_bob_out.pack(pady=5)

    def set_text(self, widget, text):
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, str(text))

    def parse_key_text(self, text):
        e_match = re.search(r'[ed]\s*=\s*(\d+)', text)
        n_match = re.search(r'n\s*=\s*(\d+)', text)
        if not e_match or not n_match:
            raise ValueError("Could not find 'e=...' or 'd=...' and 'n=...' in the text field.")
        return int(e_match.group(1)), int(n_match.group(1))

    def alice_gen_keys(self):
        try:
            bits = int(self.bit_length_var.get())
            pub, priv = tasks.generate_keypair(bits)
            
            self.set_text(self.txt_alice_pub, f"e={pub[0]}\nn={pub[1]}")
            self.set_text(self.txt_alice_priv, f"d={priv[0]}\nn={priv[1]}")
            
            # Auto-fill Bob's side for convenience
            self.set_text(self.txt_bob_pub, f"e={pub[0]}\nn={pub[1]}")
            
            # Clear previous messages
            self.set_text(self.txt_alice_cipher, "")
            self.set_text(self.txt_alice_in, "")
            self.set_text(self.txt_bob_out, "")
            self.entry_bob_msg.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Key generation failed: {e}")

    def bob_send_msg(self):
        msg = self.entry_bob_msg.get()
        if not msg: return
        
        try:
            # Parse Bob's Pub Key text field
            pub_text = self.txt_bob_pub.get("1.0", tk.END)
            pub_key = self.parse_key_text(pub_text)
            
            # String -> Bytes -> Integer
            m_int = int.from_bytes(msg.encode('utf-8'), 'big')
            
            if m_int >= pub_key[1]:
                messagebox.showerror("Error", f"Message too long! Integer representation {m_int} is larger than modulus {pub_key[1]}. Try a shorter message or larger key.")
                return
                
            c_int = tasks.encrypt(m_int, pub_key)
            self.set_text(self.txt_bob_out, str(c_int))
            
            # Auto-fill Alice's receiving box for convenience
            self.set_text(self.txt_alice_cipher, str(c_int))
            self.set_text(self.txt_alice_in, "")
            
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    def alice_decrypt(self):
        try:
            priv_text = self.txt_alice_priv.get("1.0", tk.END)
            priv_key = self.parse_key_text(priv_text)
            
            cipher_text = self.txt_alice_cipher.get("1.0", tk.END).strip()
            if not cipher_text:
                return
            c_int = int(cipher_text)
            
            # Decrypt
            dec_int = tasks.decrypt(c_int, priv_key)
            
            # Integer -> Bytes -> String
            dec_bytes = dec_int.to_bytes((dec_int.bit_length() + 7) // 8, 'big')
            dec_msg = dec_bytes.decode('utf-8')
            
            self.set_text(self.txt_alice_in, dec_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")

if __name__ == "__main__":
    app = SecureChat()
    app.mainloop()
