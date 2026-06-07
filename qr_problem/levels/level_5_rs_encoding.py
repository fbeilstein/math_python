import tkinter as tk
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
from levels.base_level import BaseLevel, BaseLevelUI, poly_to_latex

class Level5(BaseLevel):
    def test_rs_encoding(self):
        text = "Hello"
        bytes_arr = tasks.encode_text(text)
        self.assertEqual(bytes_arr, [72, 101, 108, 108, 111])

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        tk.Label(self.top_frame, text="Input Text:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_txt = tk.Entry(self.top_frame, width=20)
        self.ent_txt.insert(0, "Math!")
        self.ent_txt.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.top_frame, text="EC Bytes:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_ec = tk.Entry(self.top_frame, width=5)
        self.ent_ec.insert(0, "4")
        self.ent_ec.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.top_frame, text="Encode String", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        self.update_canvas()
        
    def draw_math(self):
        try:
            text = self.ent_txt.get()
            num_ec = int(self.ent_ec.get())
            bytes_arr = tasks.encode_text(text)
            
            p, n = 2, 8
            poly = [1, 0, 0, 0, 1, 1, 1, 0, 1]
            exp_table, log_table = tasks.generate_gfpn_tables(p, n, poly)
            gen = tasks.get_generator_poly(num_ec, log_table, exp_table, p, n)
            
            msg_padded = bytes_arr + [0]*num_ec
            rem = tasks.gfpn_poly_remainder(msg_padded, gen, log_table, exp_table, p, n)
            while len(rem) < num_ec: rem.insert(0, 0)
            
            out = f"Reed-Solomon Text Encoding\n\n"
            out += f"Input Text: '{text}'\n"
            out += f"Message Polynomial $M(x)$: {poly_to_latex(bytes_arr)}\n\n"
            out += f"Generator $G(x)$: {poly_to_latex(gen)}\n\n"
            out += f"Modulo Arithmetic: $R(x) = (M(x) \\cdot x^{{{num_ec}}}) \\text{{ mod }} G(x)$\n"
            out += f"EC Remainder $R(x)$: {poly_to_latex(rem)}\n\n"
            out += f"Transmit Array: {bytes_arr + rem}\n"
            
            self.ax.text(0.5, 0.5, out, fontsize=16, ha='center', va='center', color='white')
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Error: {e}", color="red", fontsize=14, ha='center', va='center')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--no-graphics':
        import unittest
        unittest.main(argv=['first-arg-is-ignored'])
