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
        self.control_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.control_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(self.control_frame, text="Message:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_msg = tk.Entry(self.control_frame, width=20)
        self.ent_msg.insert(0, "Hello")
        self.ent_msg.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.control_frame, text="EC Bytes:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_ec = tk.Entry(self.control_frame, width=5)
        self.ent_ec.insert(0, "4")
        self.ent_ec.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.control_frame, text="Encode Message", command=self.encode_message).pack(side=tk.LEFT, padx=10)
        
        tk.Button(self.control_frame, text="Run Decoder", command=self.update_canvas, bg="#007acc", fg="white").pack(side=tk.LEFT, padx=10)

        # Frame for the dynamic boxes
        self.boxes_frame = tk.Frame(self.top_frame, bg="#1e1e1e")
        self.boxes_frame.pack(fill=tk.X, pady=10)
        
        self.byte_entries = []
        
        # Initial setup
        self.encode_message()
        
    def encode_message(self):
        try:
            msg = self.ent_msg.get()
            ec = int(self.ent_ec.get())
            
            poly_obj = utils.make_poly([1, 0, 0, 0, 1, 1, 1, 0, 1], 2)
            gf = tasks.ExtensionField(poly_obj)
            
            msg_vals = [ord(c) for c in msg]
            msg_poly = tasks.Polynomial([utils.int_to_ext(c, gf) for c in msg_vals])
            
            gen = tasks.get_generator_poly(ec, gf)
            if not gen: raise NotImplementedError("get_generator_poly not implemented (L5)")
            
            shift = tasks.Polynomial([gf.zero] * ec + [gf.one])
            shifted = msg_poly * shift
            q, r = divmod(shifted, gen)
            
            codeword_poly = shifted - r
            self.encoded_vals = [utils.ext_to_int(codeword_poly[i]) for i in range(codeword_poly.degree() + 1)]
            
            for widget in self.boxes_frame.winfo_children():
                widget.destroy()
            self.byte_entries = []
            
            tk.Label(self.boxes_frame, text="Codeword Bytes (tamper below to inject errors):", fg="#ffcc00", bg="#1e1e1e").pack(side=tk.LEFT, padx=5)
            
            for i, val in enumerate(self.encoded_vals):
                ent = tk.Entry(self.boxes_frame, width=4, justify='center', font=("Courier", 14, "bold"))
                ent.insert(0, str(val))
                ent.pack(side=tk.LEFT, padx=2)
                self.byte_entries.append(ent)
                
            self.ax.clear()
            self.ax.axis('off')
            self.ax.text(0.5, 0.5, "Message encoded successfully!\nChange any number in the boxes above, then click 'Run Decoder'.", fontsize=16, ha='center', va='center', color='#28a745')
            self.canvas.draw()
            
        except Exception as e:
            self.ax.clear()
            self.ax.axis('off')
            self.ax.text(0.5, 0.5, f"Encoding Error: {e}", color="red", fontsize=14, ha='center', va='center')
            self.canvas.draw()
        
    def update_canvas(self):
        self.ax.clear()
        self.ax.axis('off')
        
        text = ""
        try:
            corrupted = []
            for ent in self.byte_entries:
                corrupted.append(int(ent.get()))
                
            ec = int(self.ent_ec.get())
            
            poly_obj = utils.make_poly([1, 0, 0, 0, 1, 1, 1, 0, 1], 2)
            gf = tasks.ExtensionField(poly_obj)
                        
            msg_poly = tasks.Polynomial([utils.int_to_ext(c, gf) for c in corrupted])
            syn = tasks.calculate_syndromes(msg_poly, ec, gf)
            if not syn: raise NotImplementedError("calculate_syndromes not implemented")
            syn_vals = [utils.ext_to_int(s) for s in syn]
            
            text += f"Received: {corrupted}\n\n"
            text += f"Syndromes: {syn_vals}\n\n"
            
            if all(s.val == 0 for s in syn):
                text += "No errors detected!"
                
                msg_len = len(corrupted) - ec
                decoded_chars = [chr(c) for c in corrupted[ec:]]
                text += f"\n\nDecoded Message: \"{''.join(decoded_chars)}\""
            else:
                err_loc = tasks.pgz_error_locator(syn, gf)
                if not err_loc: raise NotImplementedError("pgz_error_locator not implemented")
                text += f"Error Locator $\Lambda(x) = {poly_to_latex([utils.ext_to_int(err_loc[i]) for i in range(err_loc.degree() + 1)][::-1]).strip('$')}$\n\n"
                
                err_pos = tasks.chien_search(err_loc, len(corrupted), gf)
                if err_pos is None: raise NotImplementedError("chien_search not implemented")
                text += f"Found roots at positions: {err_pos}\n\n"
                
                mags = tasks.linear_error_magnitudes(syn, err_pos, len(corrupted), gf)
                if mags is None: raise NotImplementedError("linear_error_magnitudes not implemented")
                mags_str = {k: utils.ext_to_int(v) for k, v in mags.items()}
                text += f"Error Magnitudes: {mags_str}\n\n"
                
                for p_idx, mag in mags.items():
                    corrupted[p_idx] = corrupted[p_idx] ^ utils.ext_to_int(mag)
                    
                text += f"Corrected: {corrupted}"
                
                msg_len = len(corrupted) - ec
                decoded_chars = [chr(c) for c in corrupted[ec:]]
                text += f"\n\nRecovered Message: \"{''.join(decoded_chars)}\""
            
            self.ax.text(0.5, 0.5, text, fontsize=14, ha='center', va='center', color='white', wrap=True)
            
        except Exception as e:
            text += f"\n\n[Stopped] Error: {e}"
            self.ax.text(0.5, 0.5, text, color="red", fontsize=14, ha='center', va='center', wrap=True)
        
        self.canvas.draw()
