import tkinter as tk
from tkinter import messagebox
import implementation_tasks as tasks

class SecureChat(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alice & Bob: Secure RSA Chat")
        self.geometry("1100x700")
        self.configure(bg="#1e1e1e")
        
        self.alice_pub = None
        self.alice_priv = None
        
        tk.Label(self, text="Secure RSA Chat Demo", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="white").pack(pady=10)
        
        main_frame = tk.Frame(self, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # ALICE (LEFT)
        alice_frame = tk.Frame(main_frame, bg="#2d2d30", bd=2, relief=tk.SUNKEN)
        alice_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(alice_frame, text="ALICE", font=("Arial", 18, "bold"), bg="#2d2d30", fg="#ff79c6").pack(pady=10)
        
        tk.Button(alice_frame, text="Generate 512-bit Keys", bg="#6272a4", fg="white", font=("Arial", 12), command=self.alice_gen_keys).pack(pady=5)
        
        tk.Label(alice_frame, text="My Public Key (e, n):", bg="#2d2d30", fg="white").pack()
        self.txt_alice_pub = tk.Text(alice_frame, height=3, width=45, bg="#1e1e1e", fg="white", state=tk.DISABLED)
        self.txt_alice_pub.pack(pady=5)
        
        tk.Label(alice_frame, text="My Private Key (d, n):", bg="#2d2d30", fg="white").pack()
        self.txt_alice_priv = tk.Text(alice_frame, height=3, width=45, bg="#1e1e1e", fg="#f1fa8c", state=tk.DISABLED)
        self.txt_alice_priv.pack(pady=5)
        
        tk.Label(alice_frame, text="Decrypted Message Received:", bg="#2d2d30", fg="white").pack(pady=(20,0))
        self.txt_alice_in = tk.Text(alice_frame, height=4, width=45, bg="#1e1e1e", fg="#50fa7b", font=("Arial", 14, "bold"), state=tk.DISABLED)
        self.txt_alice_in.pack(pady=5)
        
        # BOB (RIGHT)
        bob_frame = tk.Frame(main_frame, bg="#2d2d30", bd=2, relief=tk.SUNKEN)
        bob_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(bob_frame, text="BOB", font=("Arial", 18, "bold"), bg="#2d2d30", fg="#8be9fd").pack(pady=10)
        
        tk.Label(bob_frame, text="Alice's Public Key (Received):", bg="#2d2d30", fg="white").pack()
        self.txt_bob_pub = tk.Text(bob_frame, height=3, width=45, bg="#1e1e1e", fg="white", state=tk.DISABLED)
        self.txt_bob_pub.pack(pady=5)
        
        tk.Label(bob_frame, text="Write Message to Alice:", bg="#2d2d30", fg="white").pack(pady=(20,0))
        self.entry_bob_msg = tk.Entry(bob_frame, font=("Arial", 14), width=35)
        self.entry_bob_msg.pack(pady=5)
        
        tk.Button(bob_frame, text="Encrypt and Send", bg="#ffb86c", fg="black", font=("Arial", 12, "bold"), command=self.bob_send_msg).pack(pady=10)
        
        tk.Label(bob_frame, text="Raw Ciphertext Sent (Interceptable):", bg="#2d2d30", fg="white").pack()
        self.txt_bob_out = tk.Text(bob_frame, height=5, width=45, bg="#1e1e1e", fg="#ff5555", font=("Courier", 10), state=tk.DISABLED)
        self.txt_bob_out.pack(pady=5)

    def set_text(self, widget, text):
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, str(text))
        widget.config(state=tk.DISABLED)

    def alice_gen_keys(self):
        try:
            pub, priv = tasks.generate_keypair(512)
            self.alice_pub = pub
            self.alice_priv = priv
            
            self.set_text(self.txt_alice_pub, f"e={pub[0]}\nn={pub[1]}")
            self.set_text(self.txt_alice_priv, f"d={priv[0]}\n[KEEP SECRET!]")
            
            # Send pub to Bob
            self.set_text(self.txt_bob_pub, f"e={pub[0]}\nn={pub[1]}")
            self.set_text(self.txt_alice_in, "")
            self.set_text(self.txt_bob_out, "")
        except Exception as e:
            messagebox.showerror("Error", f"Key generation failed: {e}")

    def bob_send_msg(self):
        if not self.alice_pub:
            messagebox.showwarning("Warning", "Bob needs Alice's Public Key first!")
            return
            
        msg = self.entry_bob_msg.get()
        if not msg: return
        
        try:
            # String -> Bytes -> Integer
            m_int = int.from_bytes(msg.encode('utf-8'), 'big')
            
            if m_int >= self.alice_pub[1]:
                messagebox.showerror("Error", "Message too long for 512-bit RSA! Try a shorter message.")
                return
                
            c_int = tasks.encrypt(m_int, self.alice_pub)
            self.set_text(self.txt_bob_out, str(c_int))
            
            # Alice receives and decrypts
            dec_int = tasks.decrypt(c_int, self.alice_priv)
            
            # Integer -> Bytes -> String
            dec_bytes = dec_int.to_bytes((dec_int.bit_length() + 7) // 8, 'big')
            dec_msg = dec_bytes.decode('utf-8')
            
            self.set_text(self.txt_alice_in, dec_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Encryption/Decryption cycle failed: {e}")

if __name__ == "__main__":
    app = SecureChat()
    app.mainloop()
