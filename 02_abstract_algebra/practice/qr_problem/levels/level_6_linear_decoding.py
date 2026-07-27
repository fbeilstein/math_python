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
        
        tk.Label(f1, text="Encoded Msg (Hex):", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_msg = tk.Entry(f1, width=40)
        self.ent_msg.insert(0, "48 65 6c 6c 6f 1a 45 7b 23")
        self.ent_msg.pack(side=tk.LEFT, padx=5)
        
        tk.Label(f1, text="EC Bytes:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_ec = tk.Entry(f1, width=5)
        self.ent_ec.insert(0, "4")
        self.ent_ec.pack(side=tk.LEFT, padx=5)
        
        f2 = tk.Frame(self.top_frame, bg="#1e1e1e")
        f2.pack(fill=tk.X, pady=2)
        
        tk.Label(f2, text="Inject Error (Pos, ValHex):", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_err = tk.Entry(f2, width=15)
        self.ent_err.insert(0, "1, ff")
        self.ent_err.pack(side=tk.LEFT, padx=5)
        
        tk.Button(f2, text="Decode", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        self.update_canvas()
        
    def update_canvas(self):
        self.ax.clear()
        self.ax.axis('off')
        
        try:
            msg_hex = self.ent_msg.get().replace(",", " ").split()
            encoded = [int(x, 16) for x in msg_hex]
            ec = int(self.ent_ec.get())
            
            poly_obj = utils.make_poly([1, 0, 0, 0, 1, 1, 1, 0, 1], 2)
            gf = tasks.ExtensionField(poly_obj)
            
            corrupted = list(encoded)
            err_str = self.ent_err.get().strip()
            if err_str:
                parts = err_str.split(',')
                if len(parts) == 2:
                    pos = int(parts[0].strip())
                    val = int(parts[1].strip(), 16)
                    if 0 <= pos < len(corrupted):
                        corrupted[pos] ^= val
                        
            msg_poly = tasks.Polynomial([utils.int_to_ext(c, gf) for c in corrupted])
            syn = tasks.calculate_syndromes(msg_poly, ec, gf)
            syn_vals = [utils.ext_to_int(s) for s in syn]
            
            text = f"Received: {corrupted}\n\n"
            text += f"Syndromes: {syn_vals}\n\n"
            
            if all(s.val == 0 for s in syn):
                text += "No errors detected!"
            else:
                err_loc = tasks.pgz_error_locator(syn, gf)
                text += f"Error Locator $\Lambda(x) = {poly_to_latex([utils.ext_to_int(c) for c in err_loc.coeffs]).strip('$')}$\n\n"
                
                err_pos = tasks.chien_search(err_loc, len(corrupted), gf)
                text += f"Found roots at positions: {err_pos}\n\n"
                
                mags = tasks.linear_error_magnitudes(syn, err_pos, len(corrupted), gf)
                text += f"Error Magnitudes: {{{k}: {utils.ext_to_int(v)} for k, v in mags.items()}}\n\n"
                
                for p_idx, mag in mags.items():
                    corrupted[p_idx] = corrupted[p_idx] ^ utils.ext_to_int(mag)
                    
                text += f"Corrected: {corrupted}"
            
            self.ax.text(0.5, 0.5, text, fontsize=12, ha='center', va='center', color='white', wrap=True)
            
        except Exception as e:
            self.ax.text(0.5, 0.5, f"Error: {e}", color="red", fontsize=14, ha='center', va='center')
        
        self.canvas.draw()
