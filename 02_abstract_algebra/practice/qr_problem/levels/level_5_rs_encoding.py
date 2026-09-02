import tkinter as tk
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import implementation_tasks as tasks
import algebra_utils as utils
from levels.base_level import BaseLevelUI, poly_to_latex

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        f1 = tk.Frame(self.top_frame, bg="#1e1e1e")
        f1.pack(fill=tk.X, pady=2)
        
        tk.Label(f1, text="Message:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_msg = tk.Entry(f1, width=30)
        self.ent_msg.insert(0, "Hello")
        self.ent_msg.pack(side=tk.LEFT, padx=5)
        self.ent_msg.bind("<Return>", lambda e: self.update_canvas())
        
        tk.Label(f1, text="EC Bytes:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_ec = tk.Entry(f1, width=5)
        self.ent_ec.insert(0, "4")
        self.ent_ec.pack(side=tk.LEFT, padx=5)
        self.ent_ec.bind("<Return>", lambda e: self.update_canvas())
        
        tk.Button(f1, text="Encode", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        self.update_canvas()
        
    def update_canvas(self):
        self.ax.clear()
        self.ax.axis('off')
        
        try:
            msg_str = self.ent_msg.get()
            msg = [ord(c) for c in msg_str]
            ec = int(self.ent_ec.get())
            
            poly_obj = utils.make_poly([1, 0, 0, 0, 1, 1, 1, 0, 1][::-1], 2)
            gf = tasks.ExtensionField(poly_obj)
            gen = tasks.get_generator_poly(ec, gf)
            if not gen: raise NotImplementedError("get_generator_poly not implemented")
            
            # --- Root Verification Table ---
            root_checks = []
            all_zero = True
            for i in range(ec):
                root = gf.alpha ** i
                val = gen(root)
                val_int = utils.ext_to_int(val)
                is_zero = not bool(val)
                if not is_zero:
                    all_zero = False
                root_checks.append((i, val_int, is_zero))
            
            # --- Systematic Encoding ---
            # Reverse message for Low-to-High math
            msg_poly = tasks.Polynomial([utils.int_to_ext(c, gf) for c in reversed(msg)])
            codeword_poly = tasks.rs_encode(msg_poly, ec, gf)
            
            # Extract Low-to-High up to the exact expected degree
            deg = len(msg) + ec - 1
            coeffs_lth = [utils.ext_to_int(codeword_poly[i]) for i in range(deg + 1)]
            
            # Reverse for High-to-Low UI (so message reads left-to-right)
            encoded = coeffs_lth[::-1]
            
            # --- Render ---
            gen_coeffs_htl = [utils.ext_to_int(gen[i]) for i in range(gen.degree() + 1)][::-1]
            
            text = "Reed-Solomon Encoding\n\n"
            text += f"Generator $g(x) = {poly_to_latex(gen_coeffs_htl).strip('$')}$\n\n"
            
            # Root verification table
            text += "Root Verification:\n"
            for i, val_int, is_zero in root_checks:
                sym = f"$\\alpha^{{{i}}}$" if i > 1 else ("$\\alpha$" if i == 1 else "$1$")
                status = "$= 0$ ✓" if is_zero else f"$= {val_int}$ ✗"
                text += f"  $g($  {sym}  $)$ {status}\n"
            
            if all_zero:
                text += "All roots verified! ✓\n\n"
            else:
                text += "WARNING: Not all roots are zero! ✗\n\n"
            
            # Encoding result
            text += f"Message: {msg}\n"
            text += f"Parity:  {encoded[len(msg):]}\n"
            text += f"Encoded: {encoded[:len(msg)]} | {encoded[len(msg):]}\n\n"
            
            # Codeword root verification
            text += "Codeword Verification:\n"
            cw_all_zero = True
            for i in range(ec):
                root = gf.alpha ** i
                val = codeword_poly(root)
                val_int = utils.ext_to_int(val)
                is_zero = not bool(val)
                if not is_zero:
                    cw_all_zero = False
                sym = f"$\\alpha^{{{i}}}$" if i > 1 else ("$\\alpha$" if i == 1 else "$1$")
                status = "$= 0$ ✓" if is_zero else f"$= {val_int}$ ✗"
                text += f"  $c($  {sym}  $)$ {status}\n"
            
            if cw_all_zero:
                text += "Encoding verified! ✓"
            else:
                text += "WARNING: Codeword does not vanish at roots! ✗"
            
            color = 'white' if (all_zero and cw_all_zero) else '#ff6666'
            self.ax.text(0.5, 0.5, text, fontsize=13, ha='center', va='center', 
                        color=color, wrap=True, family='monospace')
            
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Error: {e}", color="red", fontsize=14, ha='center', va='center')
        
        self.canvas.draw()
