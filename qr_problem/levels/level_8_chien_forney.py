import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel, BaseLevelUI


import itertools

def poly_to_str(poly):
    if not poly or (len(poly) == 1 and poly[0] == 0): return "0"
    terms = []
    deg = len(poly) - 1
    for i, c in enumerate(poly):
        if c == 0: continue
        power = deg - i
        term = ""
        if c != 1 or power == 0: term += str(c)
        if power > 0:
            term += "x"
            if power > 1: term += f"^{power}"
        terms.append(term)
    return " + ".join(terms)

class Level8(BaseLevel):
    def test_chien_forney(self):
        p, n = 2, 8
        poly = [1, 0, 0, 0, 1, 1, 1, 0, 1]
        exp_table, log_table = tasks.generate_gfpn_tables(p, n, poly)
        
        text = "Hello"
        bytes_arr = tasks.encode_text(text)
        
        gen = tasks.get_generator_poly(4, log_table, exp_table, p, n)
        rem = tasks.gfpn_poly_remainder(bytes_arr + [0]*4, gen, log_table, exp_table, p, n)
        encoded = bytes_arr + rem
        
        corrupted = list(encoded)
        corrupted[1] ^= 255 
        
        syn = tasks.calculate_syndromes(corrupted, 4, log_table, exp_table, p, n)
        err_loc = tasks.berlekamp_massey(syn, log_table, exp_table, p, n)
        
        err_pos = tasks.chien_search(err_loc, len(corrupted), log_table, exp_table, p, n)
        
        mags = tasks.forney_algorithm(syn, err_loc, err_pos, len(corrupted), log_table, exp_table, p, n)
        
        for p_idx, mag in mags.items():
            corrupted[p_idx] = tasks.gfpn_sub(corrupted[p_idx], mag, p, n)
            
        decoded_text = tasks.decode_text([c % 256 for c in corrupted[:len(text)]])
        self.assertEqual(decoded_text, text)


import itertools

def poly_to_str(poly):
    if not poly or (len(poly) == 1 and poly[0] == 0): return "0"
    terms = []
    deg = len(poly) - 1
    for i, c in enumerate(poly):
        if c == 0: continue
        power = deg - i
        term = ""
        if c != 1 or power == 0: term += str(c)
        if power > 0:
            term += "x"
            if power > 1: term += f"^{power}"
        terms.append(term)
    return " + ".join(terms)

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        self.encoded_bytes = []
        self.corrupted_bytes = []
        
        self.param_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.param_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(self.param_frame, text="Prime p:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_p = tk.Entry(self.param_frame, width=5)
        self.ent_p.insert(0, "2")
        self.ent_p.pack(side=tk.LEFT, padx=5)
        self.ent_p.bind("<KeyRelease>", lambda e: self.update_primitives())
        
        tk.Label(self.param_frame, text="Degree n:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_n = tk.Entry(self.param_frame, width=5)
        self.ent_n.insert(0, "8")
        self.ent_n.pack(side=tk.LEFT, padx=5)
        self.ent_n.bind("<KeyRelease>", lambda e: self.update_primitives())
        
        tk.Label(self.param_frame, text="Primitive Poly:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.poly_combo = ttk.Combobox(self.param_frame, state="readonly", width=25)
        self.poly_combo.pack(side=tk.LEFT, padx=5)
        self.poly_combo.bind("<<ComboboxSelected>>", lambda e: self.init_encode())
        
        tk.Label(self.param_frame, text="EC Bytes:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_ec = tk.Entry(self.param_frame, width=5)
        self.ent_ec.insert(0, "4")
        self.ent_ec.pack(side=tk.LEFT, padx=5)
        
        self.primitives_list = []
        
        f = tk.Frame(self.top_frame, bg="#1e1e1e")
        f.pack(fill=tk.X, pady=2)
        
        tk.Label(f, text="Input Text:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_txt = tk.Entry(f, width=20)
        self.ent_txt.insert(0, "Chien")
        self.ent_txt.pack(side=tk.LEFT, padx=5)
        
        tk.Button(f, text="Encode & Initialize", command=self.init_encode).pack(side=tk.LEFT, padx=10)
        
        self.blocks_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.blocks_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(self.blocks_frame, text="Click below to introduce errors:", fg="gray", bg="#1e1e1e").pack()
        self.btn_frame = tk.Frame(self.blocks_frame, bg="#1e1e1e")
        self.btn_frame.pack()
        
        self.update_primitives()
        
    def update_primitives(self):
        try:
            p = int(self.ent_p.get())
            n = int(self.ent_n.get())
            if p < 2 or n < 1: return
            for i in range(2, int(p**0.5) + 1):
                if p % i == 0: return
                
            primitives = []
            for coefs in itertools.product(range(p), repeat=n):
                poly = [1] + list(coefs)
                if tasks.is_primitive(poly, p, n):
                    primitives.append(poly)
            
            self.primitives_list = primitives
            str_list = [poly_to_str(p) for p in primitives]
            self.poly_combo['values'] = str_list
            if str_list:
                
                if p == 2 and n == 8:
                    try:
                        idx = self.primitives_list.index([1, 0, 0, 0, 1, 1, 1, 0, 1])
                        self.poly_combo.current(idx)
                    except ValueError:
                        self.poly_combo.current(0)
                else:
                    self.poly_combo.current(0)
            else:
                self.poly_combo.set('')
                
            self.init_encode()
        except:
            pass

    def init_encode(self):
        try:
            text = self.ent_txt.get()
            bytes_arr = tasks.encode_text(text)
            
            p = int(self.ent_p.get())
            n = int(self.ent_n.get())
            num_ec = int(self.ent_ec.get())
            idx = self.poly_combo.current()
            if idx < 0 or not self.primitives_list: return
            poly = self.primitives_list[idx]
            
            exp_table, log_table = tasks.generate_gfpn_tables(p, n, poly)
            gen = tasks.get_generator_poly(num_ec, log_table, exp_table, p, n)
            
            msg_padded = bytes_arr + [0]*num_ec
            rem = tasks.gfpn_poly_remainder(msg_padded, gen, log_table, exp_table, p, n)
            while len(rem) < num_ec: rem.insert(0, 0)
            
            self.encoded_bytes = bytes_arr + rem
            self.corrupted_bytes = list(self.encoded_bytes)
            
            self.render_blocks()
            self.update_canvas()
        except:
            pass

    def render_blocks(self):
        for w in self.btn_frame.winfo_children(): w.destroy()
        
        for i, val in enumerate(self.corrupted_bytes):
            color = "#007acc" if val == self.encoded_bytes[i] else "#cc0000"
            btn = tk.Button(self.btn_frame, text=f"{val}", bg=color, fg="white", font=("Arial", 12, "bold"),
                            command=lambda idx=i: self.corrupt_byte(idx))
            btn.pack(side=tk.LEFT, padx=2)
            
    def corrupt_byte(self, idx):
        new_val = simpledialog.askinteger("Corrupt", f"New value for byte {idx}:", initialvalue=self.corrupted_bytes[idx])
        if new_val is not None:
            self.corrupted_bytes[idx] = new_val % 256
            self.render_blocks()
            self.update_canvas()

    def draw_math(self):
        try:
            p = int(self.ent_p.get())
            n = int(self.ent_n.get())
            num_ec = int(self.ent_ec.get())
            idx = self.poly_combo.current()
            if idx < 0 or not self.primitives_list: raise ValueError("Invalid Poly")
            poly = self.primitives_list[idx]
            exp_table, log_table = tasks.generate_gfpn_tables(p, n, poly)
            
            text = self.ent_txt.get()
            
            syn = tasks.calculate_syndromes(self.corrupted_bytes, num_ec, log_table, exp_table, p, n)
            err_loc = tasks.berlekamp_massey(syn, log_table, exp_table, p, n)
            err_pos = tasks.chien_search(err_loc, len(self.corrupted_bytes), log_table, exp_table, p, n)
            mags = tasks.forney_algorithm(syn, err_loc, err_pos, len(self.corrupted_bytes), log_table, exp_table, p, n)
            
            repaired = list(self.corrupted_bytes)
            for p_idx, mag in mags.items():
                repaired[p_idx] = tasks.gfpn_sub(repaired[p_idx], mag, p, n)
                
            corrupted_str = tasks.decode_text([c % 256 for c in self.corrupted_bytes[:len(text)]])
            recovered_str = tasks.decode_text([c % 256 for c in repaired[:len(text)]])
            
            out = f"Chien Search & Forney Algorithm\n\n"
            out += f"Original Input: '{text}'\n"
            out += f"Corrupted Read: '{corrupted_str}'\n\n"
            out += f"Chien Search (Find roots $\\Lambda(\\alpha^{{-i}}) = 0$):\n"
            out += f"Errors Located at indices: {err_pos}\n\n"
            out += f"Forney Alg ($Y_k = -X_k \\frac{{\\Omega(X_k^{{-1}})}}{{\\Lambda'(X_k^{{-1}})}}$):\n"
            out += f"Error Magnitudes: {mags}\n\n"
            out += f"Recovered String: '{recovered_str}'\n"
            
            self.ax.text(0.5, 0.5, out, fontsize=18, ha='center', va='center', color='white')
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Error: {e}", color="red", fontsize=14, ha='center', va='center')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--no-graphics':
        import unittest
        unittest.main(argv=['first-arg-is-ignored'])
