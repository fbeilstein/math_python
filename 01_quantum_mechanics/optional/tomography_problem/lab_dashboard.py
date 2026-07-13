"""
Quantum Mechanics Lab: Inverse Tomography
===========================================
Visual debugger: watch the learned potential converge to the hidden one.

Student implements functions in: implementation_tasks.py
This file only provides the visualization / test harness.

Run:  python lab_dashboard.py
"""
import sys
import os
import time

try:
    import torch
except ImportError:
    print("=" * 60)
    print("This problem requires PyTorch: pip install torch")
    print("=" * 60)
    sys.exit(1)

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import interp1d

import implementation_tasks as tasks
import data_generation as data_gen

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# ═══════════════════════════════════════════════
#  Physics Setup
# ═══════════════════════════════════════════════
L, N = 40.0, 512
x_np = np.linspace(-L / 2, L / 2, N, endpoint=False)
dx = x_np[1] - x_np[0]
dt = 0.005
STEPS, N_SNAP = 400, 40
SAVE_EVERY = STEPS // N_SNAP

k_np = 2 * np.pi * np.fft.fftfreq(N, d=dx)
k_sq = torch.tensor(k_np**2, dtype=torch.float32, device=DEVICE)
psi0_np = data_gen.gaussian_packet(x_np, -18.0, 0.5, 10.0)
psi0 = torch.tensor(psi0_np, dtype=torch.complex64, device=DEVICE)


class Dashboard:
    def __init__(self):
        self.is_training = False
        self.drawing = False
        self.draw_xs = []
        self.draw_ys = []
        
        self.V_drawn = gaussian_filter1d(np.where(np.abs(x_np) < 1.0, 25.0, 0.0), sigma=2)
        self.last_V_trained = None
        self.observations = []
        
        self.model = None
        self.optimizer = None
        self.ep = 0
        self.t0 = time.time()
        
        self.setup_ui()
        
    def setup_ui(self):
        self.fig = plt.figure(figsize=(12, 7))
        self.fig.patch.set_facecolor('#0d1117')
        self.fig.canvas.manager.set_window_title('Inverse Quantum Tomography')
        self.fig.suptitle('Inverse Quantum Tomography — Discovering V(x)', color='white', fontsize=14, fontweight='bold')
        self.fig.canvas.mpl_connect('close_event', lambda e: sys.exit(0))
        
        # Left Panel (Controls)
        self.ax_ctrl_bg = self.fig.add_axes([0.02, 0.05, 0.22, 0.9])
        self.ax_ctrl_bg.set_facecolor('#161b22')
        self.ax_ctrl_bg.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        for sp in self.ax_ctrl_bg.spines.values(): sp.set_color('#30363d')
        
        self.fig.text(0.13, 0.92, 'Control Panel', color='white', fontsize=12, fontweight='bold', ha='center')
        
        # Train Toggle Button
        ax_btrain = self.fig.add_axes([0.04, 0.85, 0.18, 0.05])
        self.btn_train_toggle = Button(ax_btrain, 'Start Training', color='#238636', hovercolor='#2ea043')
        self.btn_train_toggle.label.set_color('white'); self.btn_train_toggle.label.set_fontweight('bold')
        self.btn_train_toggle.on_clicked(self.on_train_toggle)
        
        self.status_text = self.fig.text(0.13, 0.82, 'Status: Ready (Draw mode)', color='#8b949e', fontsize=9, ha='center')
        
        # Presets
        self.fig.text(0.13, 0.75, 'Target Potentials', color='white', fontsize=11, fontweight='bold', ha='center')
        
        btn_c = '#21262d'; btn_hc = '#30363d'
        ax_b1 = self.fig.add_axes([0.04, 0.69, 0.08, 0.04])
        self.btn_clear = Button(ax_b1, 'Free Space', color=btn_c, hovercolor=btn_hc)
        self.btn_clear.label.set_color('white'); self.btn_clear.on_clicked(self.on_clear)
        
        ax_b2 = self.fig.add_axes([0.14, 0.69, 0.08, 0.04])
        self.btn_barr = Button(ax_b2, 'Barrier', color=btn_c, hovercolor=btn_hc)
        self.btn_barr.label.set_color('white'); self.btn_barr.on_clicked(self.on_barrier)

        ax_b3 = self.fig.add_axes([0.04, 0.63, 0.08, 0.04])
        self.btn_well = Button(ax_b3, 'Well', color=btn_c, hovercolor=btn_hc)
        self.btn_well.label.set_color('white'); self.btn_well.on_clicked(self.on_f_well)
        
        ax_b4 = self.fig.add_axes([0.14, 0.63, 0.08, 0.04])
        self.btn_dbl = Button(ax_b4, 'Double Slit', color=btn_c, hovercolor=btn_hc)
        self.btn_dbl.label.set_color('white'); self.btn_dbl.on_clicked(self.on_double)
        
        self.preset_widgets = [self.btn_clear, self.btn_barr, self.btn_well, self.btn_dbl]

        # Main Plots
        self.ax_V = self.fig.add_axes([0.28, 0.55, 0.68, 0.37])
        self.ax_psi = self.fig.add_axes([0.28, 0.08, 0.68, 0.40])
        
        for ax in (self.ax_V, self.ax_psi):
            ax.set_facecolor('#161b22')
            ax.tick_params(colors='#8b949e')
            for sp in ax.spines.values(): sp.set_color('#30363d')
            ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)
            
        self.ax_V.set_title("Draw Potential V(x)", color='white')
        self.ax_V.axhline(y=0, color='#444466', linewidth=1)
        self.ax_psi.set_title("Wave at final time", color='white')

        self.line_vt, = self.ax_V.plot(x_np, self.V_drawn, color='#ff7b72', lw=3, label='Hidden V_true (Target)')
        self.line_vp, = self.ax_V.plot(x_np, np.zeros(N), color='#79c0ff', lw=2, label='V_pred (Learned)')
        self.ink_trail, = self.ax_V.plot([], [], color='#ffcc80', lw=2, alpha=0.7, ls='--')
        self.ax_V.set_ylim(-10, 40)
        self.ax_V.set_xlim(x_np[0], x_np[-1])
        self.ax_V.legend(facecolor='#161b22', labelcolor='white')
        
        self.line_pt, = self.ax_psi.plot(x_np, np.zeros(N), color='#ff7b72', lw=2, label='True Re[ψ]', alpha=0.5)
        self.line_pp, = self.ax_psi.plot(x_np, np.zeros(N), color='#79c0ff', lw=2, label='Pred Re[ψ]')
        self.ax_psi.set_ylim(-0.8, 0.8)
        self.ax_psi.set_xlim(x_np[0], x_np[-1])
        self.ax_psi.legend(facecolor='#161b22', labelcolor='white')
        
        self.info_text = self.ax_V.text(0.02, 0.85, '', transform=self.ax_V.transAxes, color='white', fontfamily='monospace')
        
        # Scrubber
        ax_slider = self.fig.add_axes([0.04, 0.55, 0.18, 0.03], facecolor='#161b22')
        self.sl_time = Slider(ax_slider, 'Snap', 0, N_SNAP, valinit=N_SNAP, valstep=1, color='#79c0ff')
        self.sl_time.label.set_color('white')
        self.sl_time.valtext.set_color('white')
        self.sl_time.on_changed(self.update_slider)
        
        # Events
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        
        self._update_plot()
        
    def _update_plot(self):
        self.line_vt.set_ydata(self.V_drawn)
        self.ink_trail.set_data([], [])
        self.fig.canvas.draw_idle()
        
    def on_clear(self, event):
        if self.is_training: return
        self.V_drawn = np.zeros(N)
        self._update_plot()
    def on_barrier(self, event):
        if self.is_training: return
        V_raw = np.where(np.abs(x_np) < 0.5, 25.0, 0.0)
        self.V_drawn = gaussian_filter1d(V_raw, sigma=2)
        self._update_plot()
    def on_f_well(self, event):
        if self.is_training: return
        V_raw = np.where(np.abs(x_np) < 1.0, -10.0, 0.0)
        self.V_drawn = gaussian_filter1d(V_raw, sigma=2)
        self._update_plot()
    def on_double(self, event):
        if self.is_training: return
        V_raw = np.where((np.abs(x_np) < 1.5) & (np.abs(x_np) > 0.2), 30.0, 0.0)
        self.V_drawn = gaussian_filter1d(V_raw, sigma=2)
        self._update_plot()
        
    def on_train_toggle(self, event):
        self.is_training = not self.is_training
        
        if self.is_training:
            self.btn_train_toggle.label.set_text('Stop Training')
            self.btn_train_toggle.color = '#da3633'
            self.btn_train_toggle.hovercolor = '#f85149'
            self.status_text.set_text('Status: Training...')
            self.ax_V.set_title("Training - Discovering V(x)", color='white')
            
            # Disable presets
            for w in self.preset_widgets:
                w.set_active(False)
                
            # If the potential was changed since last train, regenerate truth
            if self.last_V_trained is None or not np.allclose(self.V_drawn, self.last_V_trained):
                print("\nNew potential detected. Generating ground truth observations...")
                self.last_V_trained = self.V_drawn.copy()
                self.observations = []
                psi_np = psi0_np.copy()
                for step in range(STEPS + 1):
                    if step % SAVE_EVERY == 0:
                        self.observations.append((step, torch.tensor(psi_np, dtype=torch.complex64, device=DEVICE)))
                    if step < STEPS:
                        psi_np = data_gen.np_split_operator_step(psi_np, k_np, self.V_drawn, dt)
                        
                final_true = self.observations[-1][1]
                self.line_pt.set_ydata(torch.real(final_true).cpu().numpy())
                
                print("Re-initializing neural network...")
                self.model = tasks.GridPotential(N).to(DEVICE)
                self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1.0)
                self.ep = 0
                self.line_vp.set_ydata(np.zeros(N))
                self.line_pp.set_ydata(np.zeros(N))
                
            self.t0 = time.time()
                
        else:
            self.btn_train_toggle.label.set_text('Start Training')
            self.btn_train_toggle.color = '#238636'
            self.btn_train_toggle.hovercolor = '#2ea043'
            self.status_text.set_text('Status: Ready (Draw mode)')
            self.ax_V.set_title("Draw Potential V(x)", color='white')
            
            for w in self.preset_widgets:
                w.set_active(True)
                
        self.btn_train_toggle.ax.set_facecolor(self.btn_train_toggle.color)
        self.fig.canvas.draw_idle()

    # --- Drawing Logic ---
    def on_press(self, event):
        if self.is_training or event.inaxes != self.ax_V: return
        self.drawing = True
        self.draw_xs.clear(); self.draw_ys.clear()

    def on_motion(self, event):
        if not self.drawing or event.inaxes != self.ax_V: return
        self.draw_xs.append(event.xdata); self.draw_ys.append(event.ydata)
        self.ink_trail.set_data(self.draw_xs, self.draw_ys)
        self.fig.canvas.draw_idle()

    def on_release(self, event):
        if not self.drawing: return
        self.drawing = False
        self.ink_trail.set_data([], [])
        
        if len(self.draw_xs) < 2: 
            self.fig.canvas.draw_idle()
            return
            
        order = np.argsort(self.draw_xs)
        dx_arr = np.array(self.draw_xs)[order]
        dy_arr = np.array(self.draw_ys)[order]
        _, unique_idx = np.unique(dx_arr, return_index=True)
        dx_arr = dx_arr[unique_idx]; dy_arr = dy_arr[unique_idx]
        
        if len(dx_arr) < 2: return
        
        interp_func = interp1d(dx_arr, dy_arr, kind='linear', bounds_error=False, fill_value=np.nan)
        V_new = interp_func(x_np)
        drawn_mask = ~np.isnan(V_new)
        self.V_drawn[drawn_mask] = V_new[drawn_mask]
        self.V_drawn = gaussian_filter1d(self.V_drawn, sigma=3)
        self._update_plot()
        
    def update_slider(self, val):
        idx = int(self.sl_time.val)
        if hasattr(self, 'observations') and len(self.observations) > idx:
            true_psi = self.observations[idx][1]
            t_val = self.observations[idx][0] * dt
            self.line_pt.set_ydata(torch.real(true_psi).cpu().numpy())
            self.ax_psi.set_title(f"Wave at t={t_val:.2f}", color='white')
        if hasattr(self, 'current_pred_history') and len(self.current_pred_history) > idx:
            self.line_pp.set_ydata(np.real(self.current_pred_history[idx]))
        self.fig.canvas.draw_idle()
        
    def train_step(self):
        self.ep += 1
        self.optimizer.zero_grad()
        V_pred = self.model()
        loss = tasks.run_teacher_forcing(V_pred, self.observations, psi0, k_sq, dt)
        loss.backward()
        self.optimizer.step()
        
        if self.ep % 5 == 0:
            with torch.no_grad():
                self.line_vp.set_ydata(V_pred.cpu().numpy())
                self.current_pred_history = [psi0.clone().cpu().numpy()]
                psi_fwd = psi0.clone()
                for step in range(1, STEPS + 1):
                    psi_fwd = tasks.pt_split_operator_step(psi_fwd, k_sq, V_pred, dt)
                    if step % SAVE_EVERY == 0:
                        self.current_pred_history.append(psi_fwd.cpu().numpy())
                self.update_slider(None)
                
                fps = self.ep / max(1e-5, (time.time() - self.t0))
                self.info_text.set_text(f"Epoch {self.ep} | Loss: {loss.item():.4e} | {fps:.1f} it/s")
                
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
            
    def run(self):
        plt.ion(); plt.show()
        while plt.fignum_exists(self.fig.number):
            if self.is_training:
                self.train_step()
                plt.pause(0.001)
            else:
                plt.pause(0.1)

if __name__ == '__main__':
    app = Dashboard()
    app.run()
