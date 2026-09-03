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
        self.ent_msg.bind("<Return>", lambda e: self.encode_message())
        
        tk.Label(self.control_frame, text="EC Bytes:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_ec = tk.Entry(self.control_frame, width=5)
        self.ent_ec.insert(0, "4")
        self.ent_ec.pack(side=tk.LEFT, padx=5)
        self.ent_ec.bind("<Return>", lambda e: self.encode_message())
        
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
            
            poly_obj = utils.make_poly([1, 0, 0, 0, 1, 1, 1, 0, 1][::-1], 2)
            gf = tasks.ExtensionField(poly_obj)
            
            msg_vals = [ord(c) for c in msg]
            
            # Reverse message for Low-to-High math, then encode
            msg_poly = tasks.Polynomial([utils.int_to_ext(c, gf) for c in reversed(msg_vals)])
            codeword_poly = tasks.rs_encode(msg_poly, ec, gf)
            
            # Extract Low-to-High up to exact expected degree
            deg = len(msg_vals) + ec - 1
            coeffs_lth = [utils.ext_to_int(codeword_poly[i]) for i in range(deg + 1)]
            
            # Reverse for High-to-Low UI
            self.encoded_vals = coeffs_lth[::-1]
            
            for widget in self.boxes_frame.winfo_children():
                widget.destroy()
            self.byte_entries = []
            self.true_err_labels = []
            self.arrow_labels = []
            self.dec_mag_labels = []
            
            msg_len = len(msg_vals)
            
            # Label row
            label_frame = tk.Frame(self.boxes_frame, bg="#1e1e1e")
            label_frame.pack(fill=tk.X)
            tk.Label(label_frame, text="Codeword Bytes (tamper below to inject errors):", fg="#ffcc00", bg="#1e1e1e").pack(side=tk.LEFT, padx=5)
            
            # Byte boxes row
            boxes_row = tk.Frame(self.boxes_frame, bg="#1e1e1e")
            boxes_row.pack(fill=tk.X, pady=2)
            
            lbl_v_frame = tk.Frame(boxes_row, bg="#1e1e1e")
            lbl_v_frame.pack(side=tk.LEFT, padx=(5, 0))
            tk.Label(lbl_v_frame, text="MSG", fg="#28a745", bg="#1e1e1e", font=("Courier", 8), pady=10).pack(side=tk.TOP)
            
            for i, val in enumerate(self.encoded_vals):
                # First msg_len bytes are message, rest are parity (in HTL order)
                is_msg = i < msg_len
                border_color = "#28a745" if is_msg else "#ff8c00"
                poly_idx = len(self.encoded_vals) - 1 - i
                
                v_frame = tk.Frame(boxes_row, bg="#1e1e1e")
                v_frame.pack(side=tk.LEFT, padx=1)
                
                # Top: Entry box
                frame1 = tk.Frame(v_frame, bg=border_color, padx=1, pady=1)
                frame1.pack(side=tk.TOP)
                ent = tk.Entry(frame1, width=4, justify='center', font=("Courier", 14, "bold"))
                ent.insert(0, str(val))
                ent.pack()
                ent.bind("<KeyRelease>", lambda e: self.update_canvas())
                self.byte_entries.append(ent)
                
                # Index under Entry
                tk.Label(v_frame, text=str(poly_idx), fg="#888", bg="#1e1e1e", font=("Courier", 8)).pack(side=tk.TOP)
                
                tk.Label(v_frame, text="", bg="#1e1e1e", font=("Courier", 2)).pack(side=tk.TOP)
                
                # True error (no border, blends with background when 0)
                err_lbl = tk.Label(v_frame, text="0", width=4, font=("Courier", 14, "bold"), bg="#1e1e1e", fg="#555")
                err_lbl.pack(side=tk.TOP)
                self.true_err_labels.append(err_lbl)
                
                # Arrows and Decoded Magnitude
                arr_lbl = tk.Label(v_frame, text=" ", font=("Courier", 14, "bold"), fg="red", bg="#1e1e1e")
                arr_lbl.pack(side=tk.TOP)
                self.arrow_labels.append(arr_lbl)
                
                dec_mag_lbl = tk.Label(v_frame, text=" ", font=("Courier", 14, "bold"), fg="red", bg="#1e1e1e")
                dec_mag_lbl.pack(side=tk.TOP)
                self.dec_mag_labels.append(dec_mag_lbl)
                
                # Add separators
                if i == msg_len - 1:
                    sep_v_frame = tk.Frame(boxes_row, bg="#1e1e1e")
                    sep_v_frame.pack(side=tk.LEFT, padx=2)
                    tk.Label(sep_v_frame, text="|", fg="#555", bg="#1e1e1e", font=("Courier", 16)).pack(side=tk.TOP)
                    
                    ec_v_frame = tk.Frame(boxes_row, bg="#1e1e1e")
                    ec_v_frame.pack(side=tk.LEFT, padx=(0, 2))
                    tk.Label(ec_v_frame, text="EC", fg="#ff8c00", bg="#1e1e1e", font=("Courier", 8), pady=10).pack(side=tk.TOP)
                
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
            # Reset UI labels
            for arr_lbl, dec_lbl in zip(self.arrow_labels, self.dec_mag_labels):
                arr_lbl.config(text=" ")
                dec_lbl.config(text=" ")
                
            # User modifies High-to-Low array in UI
            corrupted_htl = []
            for idx in range(len(self.encoded_vals)):
                ent = self.byte_entries[idx]
                err_lbl = self.true_err_labels[idx]
                try:
                    c_val = int(ent.get()) & 0xFF
                    corrupted_htl.append(c_val)
                    true_err = c_val ^ self.encoded_vals[idx]
                    err_lbl.config(text=str(true_err))
                    
                    if true_err != 0:
                        ent.config(fg="#ff4444")
                        err_lbl.config(bg="black", fg="white")
                    else:
                        ent.config(fg="black")
                        err_lbl.config(bg="#1e1e1e", fg="#555")
                except ValueError:
                    # Fallback for invalid text while typing
                    corrupted_htl.append(self.encoded_vals[idx])
                    err_lbl.config(text="?", bg="#1e1e1e", fg="#555")
                    ent.config(fg="black")
                    
            ec = int(self.ent_ec.get())
            poly_obj = utils.make_poly([1, 0, 0, 0, 1, 1, 1, 0, 1][::-1], 2)
            gf = tasks.ExtensionField(poly_obj)
            
            # Reverse back to Low-to-High for math
            corrupted_lth = corrupted_htl[::-1]
                        
            msg_poly = tasks.Polynomial([utils.int_to_ext(c, gf) for c in corrupted_lth])
            syn = tasks.calculate_syndromes(msg_poly, ec, gf)
            if not syn: raise NotImplementedError("calculate_syndromes not implemented")
            syn_vals = [utils.ext_to_int(s) for s in syn]
            
            # Show original vs received with corruption markers
            orig_str = str(self.encoded_vals)
            recv_str = str(corrupted_htl)
            text += f"Original:  {orig_str}\n"
            text += f"Received:  {recv_str}\n"
            text += f"\nSyndromes: {syn_vals}\n\n"
            
            if all(not bool(s) for s in syn):
                text += "No errors detected!"
                
                # In Low-to-High array, message bytes are at the end [ec:]
                # E.g. [p0, p1, p2, p3, o, l, l, e, H]. Reverse to get "Hello"
                decoded_chars = [chr(c) for c in corrupted_lth[ec:]]
                text += f"\n\nDecoded Message: \"{''.join(decoded_chars[::-1])}\""
            else:
                err_loc = tasks.pgz_error_locator(syn, gf)
                if not err_loc: raise NotImplementedError("pgz_error_locator not implemented")
                text += f"Error Locator $\\Lambda(x) = {poly_to_latex([utils.ext_to_int(err_loc[i]) for i in range(err_loc.degree() + 1)][::-1]).strip('$')}$\n\n"
                
                err_pos = tasks.chien_search(err_loc, len(corrupted_lth), gf)
                if err_pos is None: raise NotImplementedError("chien_search not implemented")
                text += f"Found roots at positions: {err_pos}\n\n"
                
                Y_mags = tasks.linear_error_magnitudes(syn, err_pos, gf)
                
                # Draw arrows for discovered error positions
                for i, pos in enumerate(err_pos):
                    idx_htl = len(self.encoded_vals) - 1 - pos
                    if 0 <= idx_htl < len(self.arrow_labels):
                        self.arrow_labels[idx_htl].config(text="↑")
                        if Y_mags is not None and i < len(Y_mags):
                            self.dec_mag_labels[idx_htl].config(text=str(utils.ext_to_int(Y_mags[i])))
                            
                if Y_mags is None: raise NotImplementedError("linear_error_magnitudes not implemented")
                
                mags_str = {err_pos[i]: utils.ext_to_int(Y_mags[i]) for i in range(len(err_pos))}
                text += f"Error Magnitudes: {mags_str}\n\n"
                
                for i, pos in enumerate(err_pos):
                    corrupted_lth[pos] = corrupted_lth[pos] ^ utils.ext_to_int(Y_mags[i])
                
                corrected_htl = corrupted_lth[::-1]
                text += f"Corrected: {corrected_htl}"
                
                decoded_chars = [chr(c) for c in corrupted_lth[ec:]]
                text += f"\n\nRecovered Message: \"{''.join(decoded_chars[::-1])}\""
            
            self.ax.text(0.5, 0.5, text, fontsize=14, ha='center', va='center', color='white', wrap=True)
            
        except NotImplementedError as e:
            text += f"\n\n[Pending Task] {e}"
            self.ax.text(0.5, 0.5, text, color="#ffcc00", fontsize=14, ha='center', va='center', wrap=True)
        except Exception as e:
            text += f"\n\n[Error] {type(e).__name__}: {e}"
            self.ax.text(0.5, 0.5, text, color="#ff6666", fontsize=14, ha='center', va='center', wrap=True)
        
        self.canvas.draw()
