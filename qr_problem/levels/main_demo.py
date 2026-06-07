import tkinter as tk
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import qr_code as qr
from levels.base_level import BaseLevelUI

class LevelUI(BaseLevelUI):
    def setup_inputs(self):
        f1 = tk.Frame(self.top_frame, bg="#1e1e1e")
        f1.pack(fill=tk.X, pady=2)
        
        tk.Label(f1, text="Text to encode:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        self.ent_txt = tk.Entry(f1, width=40)
        self.ent_txt.insert(0, "Hello QR World!")
        self.ent_txt.pack(side=tk.LEFT, padx=5)
        
        tk.Button(f1, text="Generate QR", command=self.update_canvas).pack(side=tk.LEFT, padx=10)
        self.update_canvas()
        
    def draw_math(self):
        try:
            text = self.ent_txt.get()
            
            exp_table, log_table = qr.generate_gf256_tables()
            
            version, specs = qr.determine_version(text)
            raw_data_bytes = qr.encode_data(text, specs[0])
            
            interleaved_data, interleaved_ec = qr.interleave_blocks(raw_data_bytes, specs, log_table, exp_table)
            
            data_bits = [int(b) for byte in interleaved_data for b in f"{byte:08b}"]
            ec_bits = [int(b) for byte in interleaved_ec for b in f"{byte:08b}"]
            
            matrix = qr.build_qr_matrix(version, data_bits, ec_bits)
            
            self.ax.imshow(matrix, cmap="gray", vmin=0, vmax=1)
            self.ax.set_title(f"QR Matrix (Version {version})", color='white', fontsize=18)
        except Exception as e:
            import traceback
            err = traceback.format_exc()
            self.ax.text(0.5, 0.5, f"Error: {e}\n{err}", color="red", fontsize=8, ha='center', va='center')

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Main QR Demo")
    root.geometry("800x600")
    app = LevelUI(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
