import tkinter as tk
from tkinter import messagebox
import importlib
import sys
import subprocess
import os
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import RectangleSelector

# Ensure directories are in path for robust importing
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import source_manager
import implementation_tasks

class DrosteLabDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Escher Droste Lab")
        self.geometry("1400x800")
        self.configure(bg="#1e1e1e")
        self.demo_process = None

        self.current_lvl_num = 1
        self.source_mgr = source_manager.SourceManager()
        self.rect = [150, 100, 200, 200] # x, y, w, h
        self.im_left = None
        self.im_right = None
        
        self.setup_sidebar()
        self.setup_main_area()
        self.setup_matplotlib()

        # Start the video loop
        self.after(50, self.update_frame)

    def setup_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#252526", highlightbackground="#333333", highlightthickness=1)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        
        tk.Label(self.sidebar, text="Transformations", font=("Arial", 12, "bold"), 
                 bg="#252526", fg="white").pack(pady=15, padx=20)
        
        self.tasks = {
            1: "Normalization",
            2: "Log-Polar",
            3: "Conformal Twist",
            4: "Exponentiation",
            5: "Droste Fold"
        }
        
        self.level_buttons = {}
        for num, name in self.tasks.items():
            btn = tk.Button(self.sidebar, text=f"L{num} {name}", width=20, font=("Arial", 9),
                            bg="#3e3e42", fg="white",
                            command=lambda n=num: self.switch_level(n))
            btn.pack(pady=4, padx=10)
            self.level_buttons[num] = btn

        # Highlight first level
        self.level_buttons[1].configure(bg="#007acc")

        tk.Button(self.sidebar, text="🔄 Reload Code", bg="#007acc", fg="white",
                  command=self.reload_code).pack(pady=(30, 10), padx=20, fill="x")

        tk.Button(self.sidebar, text="🚀 Run Main Demo", bg="#007acc", fg="white", 
                  font=("Arial", 10, "bold"), command=self.run_main_simulation).pack(pady=(0, 20), padx=20, fill="x")

        # Source Selection
        tk.Label(self.sidebar, text="Video Source", font=("Arial", 10, "bold"), 
                 bg="#252526", fg="white").pack(pady=(20, 5), padx=20)

        self.source_var = tk.StringVar(value="grid")
        for mode, text in [("grid", "Grid"), ("image", "Image (Disk)"), ("camera", "Webcam")]:
            rb = tk.Radiobutton(self.sidebar, text=text, variable=self.source_var, value=mode,
                                bg="#252526", fg="white", selectcolor="#3e3e42",
                                command=self.change_source)
            rb.pack(anchor="w", padx=20)

    def setup_main_area(self):
        self.main_container = tk.Frame(self, bg="#1e1e1e")
        self.main_container.pack(side="right", fill="both", expand=True)

    def setup_matplotlib(self):
        self.fig = Figure(figsize=(12, 6), facecolor="#1e1e1e")
        # Maximize the subplots area
        self.fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.08, wspace=0.15)
        
        self.ax_left = self.fig.add_subplot(121)
        self.ax_right = self.fig.add_subplot(122)
        
        for ax in [self.ax_left, self.ax_right]:
            ax.set_facecolor("#1e1e1e")
            ax.tick_params(colors='white', labelsize=10)
            for spine in ax.spines.values():
                spine.set_color('white')
            # Add a clean, highly visible mathematical grid
            ax.grid(True, color='black', linestyle='--', alpha=0.4)

        self.ax_left.set_title("Source Image + ROI", color="white", fontsize=14)
        self.ax_right.set_title("Transformation Result", color="white", fontsize=14)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        
        self.drag_active = False
        self.resize_active = False
        self.offset = (0, 0)

    def on_mouse_press(self, event):
        if event.inaxes != self.ax_left: return
        x, y = event.xdata, event.ydata
        if x is None or y is None: return
        
        rx, ry, rw, rh = self.rect
        is_resize_area = (rx + rw - 30 <= x <= rx + rw + 30) and (ry + rh - 30 <= y <= ry + rh + 30)
        inside = rx <= x <= rx+rw and ry <= y <= ry+rh

        if is_resize_area:
            self.resize_active = True
        elif inside:
            self.drag_active = True
            self.offset = (x - rx, y - ry)

    def on_mouse_move(self, event):
        if event.inaxes != self.ax_left: return
        x, y = event.xdata, event.ydata
        if x is None or y is None: return
        
        if self.drag_active:
            self.rect[0] = int(x - self.offset[0])
            self.rect[1] = int(y - self.offset[1])
        elif self.resize_active:
            self.rect[2] = int(max(30, x - self.rect[0]))
            self.rect[3] = int(max(30, y - self.rect[1]))

    def on_mouse_release(self, event):
        self.drag_active = False
        self.resize_active = False

    def change_source(self):
        mode = self.source_var.get()
        self.source_mgr.set_mode(mode)

    def reload_code(self):
        try:
            importlib.reload(implementation_tasks)
        except Exception as e:
            messagebox.showerror("Compilation Error", f"Error in implementation_tasks.py:\n\n{e}")

    def switch_level(self, level_num):
        self.current_lvl_num = level_num
        for num, btn in self.level_buttons.items():
            btn.configure(bg="#3e3e42")
        self.level_buttons[level_num].configure(bg="#007acc")

    def update_frame(self):
        frame = self.source_mgr.get_frame()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        H, W = frame_rgb.shape[:2]
        
        # Clamp bounds strictly so it never goes off-screen
        x, y, rw, rh = self.rect
        x = max(0, min(x, W - 30))
        y = max(0, min(y, H - 30))
        rw = max(30, min(rw, W - x - 1))
        rh = max(30, min(rh, H - y - 1))
        self.rect = [int(x), int(y), int(rw), int(rh)]

        # We draw UI elements on left_view so they don't get warped
        left_view = frame_rgb.copy()
        
        # Draw ROI overlay on the left view and the source frame
        if self.rect is not None:
            x, y, w, h = self.rect
            cx = x + w / 2.0
            cy = y + h / 2.0
            
            c, bound_x, bound_y, S_true, Bx, By = implementation_tasks.calculate_mathematical_bounds(H, W, cx, cy, w, h)
            
            gx = int(cx - bound_x)
            gy = int(cy - bound_y)
            gw = int(bound_x * 2)
            gh = int(bound_y * 2)
            
            # Draw on left_view (UI only)
            cv2.rectangle(left_view, (int(x), int(y)), (int(x + w), int(y + h)), (0, 0, 255), 2)  # Red inner
            cv2.rectangle(left_view, (gx, gy), (gx + gw, gy + gh), (0, 255, 0), 2)                # Green outer
            
            # Burn into frame_rgb so cv2.remap perfectly warps them through every math level
            cv2.rectangle(frame_rgb, (int(x), int(y)), (int(x + w), int(y + h)), (0, 0, 255), 3)  # Red inner
            cv2.rectangle(frame_rgb, (gx, gy), (gx + gw, gy + gh), (0, 255, 0), 3)                # Green outer
        
        # Draw the mathematical origin axes for the source frame (yellow) ONLY on left_view
        cx = int(x + rw / 2.0)
        cy = int(y + rh / 2.0)
        cv2.line(left_view, (cx, 0), (cx, H), (255, 255, 0), 1)
        cv2.line(left_view, (0, cy), (W, cy), (255, 255, 0), 1)
        
        # Visual indicator for the resize handle (Red dot)
        cv2.circle(left_view, (x+rw, y+rh), 8, (255, 0, 0), -1)
        
        if self.im_left is None:
            self.im_left = self.ax_left.imshow(left_view)
        else:
            self.im_left.set_data(left_view)

        # Apply transformations using inverse mapping for image warping
        result_rgb, extent = self.run_transformation_pipeline(frame_rgb)
        
        # Draw destination mathematical crosshairs perfectly centered
        cx_out = int(W / 2.0)
        cy_out = int(H / 2.0)
        cv2.line(result_rgb, (cx_out, 0), (cx_out, H), (255, 255, 0), 2)
        cv2.line(result_rgb, (0, cy_out), (W, cy_out), (255, 255, 0), 2)

        if self.im_right is None:
            self.im_right = self.ax_right.imshow(result_rgb, extent=extent)
            self.ax_right.set_aspect('equal', adjustable='box')
        else:
            self.im_right.set_extent(extent)
            self.im_right.set_data(result_rgb)
            self.ax_right.set_xlim(extent[0], extent[1])
            self.ax_right.set_ylim(extent[2], extent[3])
            self.ax_right.set_aspect('equal', adjustable='box')

        self.canvas.draw_idle()
        self.canvas.flush_events()
        
        # Schedule next update (aim for ~20 FPS)
        self.after(50, self.update_frame)

    def run_transformation_pipeline(self, frame_rgb):
        try:
            H, W = frame_rgb.shape[:2]
            x0, y0, w, h = self.rect
            cx = x0 + w / 2.0
            cy = y0 + h / 2.0
            
            c, bound_x, bound_y, S_true, Bx, By = implementation_tasks.calculate_mathematical_bounds(H, W, cx, cy, w, h)
            
            m = c if c > 1.01 else 2.0
            alpha = np.log(m) / (2 * np.pi)
            r_0 = (h / 2.0) / S_true
            exact_rotation = -alpha * np.log(r_0)
            C = 1.0 + 1j * alpha
            
            # S_disp is the display scalar for the right screen grid.
            # We scale it so the mathematical Y-axis shows exactly [-1.2, 1.2]
            S_disp = (H / 2.0) / 1.2
            
            # L1: Generate the mathematical grid for the right screen
            # This grid is centered at W/2, H/2, so the singularity is perfectly in the middle of the screen.
            Z_out = implementation_tasks.backward_step_1_normalize(H, W, S_disp)
            y_grid, x_grid = np.meshgrid(np.arange(H), np.arange(W), indexing='ij')

            # Initial variables
            Z = Z_out
            extent = [-W/2.0/S_disp, W/2.0/S_disp, H/2.0/S_disp, -H/2.0/S_disp]

            # Specialized grid for L2/L3 intermediate visualizer
            if self.current_lvl_num in [2, 3]:
                log_m = max(np.log(m), 1.0)
                X_min, X_max = -log_m * 2.0, log_m * 2.0
                Y_min, Y_max = -np.pi, np.pi
                X_w = (x_grid / W) * (X_max - X_min) + X_min
                Y_w = (y_grid / H) * (Y_max - Y_min) + Y_min
                Z = X_w + 1j * Y_w
                extent = [X_min, X_max, Y_max, Y_min]

            # --- THE CASCADE PIPELINE ---
            
            if self.current_lvl_num >= 4:
                try:
                    Z_new = implementation_tasks.backward_step_4_exponentiation(Z)
                    Z = Z_new if Z_new is not None else Z
                except Exception:
                    pass
                
            if self.current_lvl_num >= 3:
                try:
                    Z_new = implementation_tasks.backward_step_3_conformal_twist(Z, C)
                    Z = Z_new if Z_new is not None else Z
                except Exception:
                    pass
                
            if self.current_lvl_num >= 2:
                try:
                    Z_new = implementation_tasks.backward_step_2_log_polar(Z)
                    Z = Z_new if Z_new is not None else Z
                except Exception:
                    pass
                
            if self.current_lvl_num == 5:
                try:
                    Z_new = implementation_tasks.backward_step_5_droste_fold(Z, m, exact_rotation, Bx, By)
                    Z = Z_new if Z_new is not None else Z
                except Exception:
                    pass

            Z_src = Z
            src_x, src_y = implementation_tasks.denormalize(Z_src, cx, cy, S_true)

            result_rgb = cv2.remap(frame_rgb, src_x, src_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            return result_rgb, extent

        except Exception as e:
            err_frame = frame_rgb.copy()
            err_frame[:, :, 0] = 255 # Red channel maxed out
            return err_frame, [-1, 1, 1, -1]

    def run_main_simulation(self):
        """Launches the main esher_droste_video.py script as an independent process."""
        try:
            # Turn off the camera if it's currently on so the main demo can access it
            if self.source_var.get() == "camera":
                self.source_var.set("grid")
                self.change_source()
            if self.demo_process is not None and self.demo_process.poll() is None:
                self.demo_process.terminate()
            self.demo_process = subprocess.Popen([sys.executable, "esher_droste_video.py"])
        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to launch esher_droste_video.py:\n{e}")

    def on_closing(self):
        if self.demo_process is not None and self.demo_process.poll() is None:
            self.demo_process.terminate()
        self.source_mgr.release()
        self.destroy()

if __name__ == "__main__":
    app = DrosteLabDashboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
