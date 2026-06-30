import tkinter as tk
from tkinter import ttk
import numpy as np
from implementation_tasks import calculate_slab_displacement, calculate_focal_length

class Inspector:
    def __init__(self, parent, on_update_callback):
        self.parent = parent
        self.on_update = on_update_callback # Redraw callback for the bench
        self.current_lens = None
        
        # UI Elements
        self.frame = tk.LabelFrame(parent, text="Physics Inspector", width=250)
        self.frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        self.frame.pack_propagate(False)
        
        self.lbl_phys = tk.Label(self.frame, text="Select a lens.", justify=tk.LEFT, 
                                 fg="blue", font=("Consolas", 10))
        self.lbl_phys.pack(pady=20, padx=10)
        
        # Refractive Index Control owned by Inspector
        self.n_var = tk.DoubleVar(value=1.52)
        self.setup_controls()

    def setup_controls(self):
        ctrl_frame = tk.Frame(self.frame)
        ctrl_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        #tk.Label(ctrl_frame, text="Index (n):").pack(side=tk.LEFT, padx=5)
        #self.spin_n = ttk.Spinbox(ctrl_frame, from_=1.0, to=4.0, increment=0.01, 
        #                          textvariable=self.n_var, width=6, command=self.sync_to_lens)
        #self.spin_n.pack(side=tk.LEFT)
        #self.n_var.trace_add("write", lambda *args: self.sync_to_lens())

    def sync_with_selected(self, lens):
        """Called by the Bench when a lens is clicked or loaded."""
        self.current_lens = lens
        if lens:
            self.n_var.set(lens.n) # Pull n from lens to UI
            self.refresh_text()
        else:
            self.lbl_phys.config(text="Select a lens.")

    def sync_to_lens(self):
        """Pushes UI changes back to the lens object."""
        if self.current_lens:
            try:
                self.current_lens.n = self.n_var.get()
                self.refresh_text()
                self.on_update() # Trigger bench redraw
            except tk.TclError: pass

    def refresh_text(self):
        """Updates the descriptive text panel based on lens type."""
        if not self.current_lens: 
            return
        
        p = self.current_lens.phys 
        n = self.current_lens.n
        theta = self.current_lens.angle
        
        if p.get('is_slab', False):
            try:
                # Pass the actual rotation (converted to radians) to the student function
                #h_val = tasks.calculate_slab_displacement(p['d'], n, np.radians(theta))
                h_val = calculate_slab_displacement(p['d'], n, np.arcsin(np.sin(np.radians(int(theta)))))
                h_str = f"{h_val:.2f} mm" if h_val is not None else "Not Implemented"
            except: 
                h_str = "Error in Task"
            text = (f"Type: SLAB\nn: {n:.3f}\nd: {p['d']:.1f}mm\n"
                    f"Angle: {theta:+.1f}°\n-------------------\n"
                    f"Displacement: {h_str}")
        else:
            R1 = p['R1_abs'] if p['is_convex_front'] else -p['R1_abs']
            R2 = -p['R2_abs'] if p['is_convex_back'] else p['R2_abs']
            try:
                # Student only sees the standard 4-parameter call
                f_val = calculate_focal_length(R1, R2, p['d'], n)
                f_str = f"{f_val:.2f} mm" if f_val is not None else "Not Implemented"
            except:
                f_str = "Error"
            text = (f"Type: LENS\nn: {n:.3f}\nR1: {R1:+.1f}\nR2: {R2:+.1f}\n"
                    f"d: {p['d']:.1f}\n-------------------\n"
                    f"Theor. f: {f_str}")
        
        self.lbl_phys.config(text=text)
