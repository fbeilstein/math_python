import json
import numpy as np
from tkinter import filedialog, messagebox

class IOManager:
    @staticmethod
    def _clean_types(obj):
        if isinstance(obj, (np.bool_, bool)): 
            return bool(obj)
        
        # Catch NumPy numbers
        if isinstance(obj, (np.float32, np.float64)): 
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)): 
            return int(obj)
            
        # Recursive cleaning for nested structures like 'geo'
        if isinstance(obj, np.ndarray): 
            return obj.tolist()
        if isinstance(obj, dict): 
            return {k: IOManager._clean_types(v) for k, v in obj.items()}
        if isinstance(obj, list): 
            return [IOManager._clean_types(i) for i in obj]
            
        return obj

    @staticmethod
    def save_lab(source_type, source_pos, lenses):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path: return
        
        # Bench only handles bench-level data
        raw_data = {
            "source_type": source_type,
            "source_pos": IOManager._clean_types(source_pos),
            "lenses": [lens.to_dict() for lens in lenses] # Lenses handle themselves!
        }
        data = IOManager._clean_types(raw_data)
        
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed: {e}")

    @staticmethod
    def load_lab():
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file_path: return None
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed: {e}")
            return None
