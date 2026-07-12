import sys
import os
import time
import numpy as np

try:
    import torch
except ImportError:
    print("=" * 60)
    print("This problem requires PyTorch. Please run: python install_pytorch.py")
    print("=" * 60)
    sys.exit(1)

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RadioButtons
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import interp1d

import implementation_tasks as tasks
import data_generation as data_gen

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# ═══════════════════════════════════════════════
#  Physics Setup
# ═══════════════════════════════════════════════
N_X = 256
X_MIN, X_MAX = -10.0, 10.0
DT = 0.005
x_np = np.linspace(X_MIN, X_MAX, N_X, endpoint=False)
dx = x_np[1] - x_np[0]
k_np = 2 * np.pi * np.fft.fftfreq(N_X, d=dx)

WEIGHTS_DIR = 'weights'
os.makedirs(WEIGHTS_DIR, exist_ok=True)
WEIGHTS_PATH = os.path.join(WEIGHTS_DIR, 'fno_model.pth')

def calculate_transmission_np(dens, x_grid, barrier_end=2.0):
    dx = x_grid[1] - x_grid[0]
    mask = x_grid > barrier_end
    return np.sum(dens[mask]) * dx

class Dashboard:
    def __init__(self):
        self.mode = "Train"
        self.V_drawn = np.zeros(N_X)
        self.psi_history = None
        self.drawing = False
        self.draw_xs = []
        self.draw_ys = []
        self.t_show = 0.0
        
        # Initial Wavepacket params
        self.x0 = -5.0
        self.k0 = 3.0
        self.sigma = 0.5

        self.is_training = False

        # Initialize FNO
        self.model = tasks.FNO1d(modes=128, width=128).to(DEVICE)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-4, weight_decay=1e-4)
        self.scheduler = torch.optim.lr_scheduler.OneCycleLR(self.optimizer, max_lr=2e-3, steps_per_epoch=1, epochs=50000)
        
        if os.path.exists(WEIGHTS_PATH):
            try:
                state_dict = torch.load(WEIGHTS_PATH, map_location=DEVICE)
                has_nans = any(torch.isnan(v).any().item() for v in state_dict.values())
                if has_nans:
                    print(f"Warning: {WEIGHTS_PATH} contains NaNs (corrupted). Starting fresh in Train mode.")
                else:
                    self.model.load_state_dict(state_dict)
                    self.mode = "Inference"
                    print(f"Loaded existing weights from {WEIGHTS_PATH}. Starting in Inference mode.")
            except Exception as e:
                print(f"Error loading {WEIGHTS_PATH}: {e}. Starting fresh.")
        else:
            print("No weights found. Starting in Train mode. Weights will auto-save every 10 epochs.")

        # Initialize GPU-accelerated Batched SSFM for live training
        print("Initializing GPU Batched SSFM for data generation...")
        self.BATCH = 32 if DEVICE != 'cpu' else 16
        self.ssfm = data_gen.BatchedSSFM(N_x=N_X, x_min=X_MIN, x_max=X_MAX, dt=DT, T_final=3.0, device=DEVICE)
        self.loss_hist = []
        self.ep = 0

        self.setup_ui()
        self._show_initial()

    def setup_ui(self):
        self.fig = plt.figure(figsize=(15, 10))
        self.fig.patch.set_facecolor('#0d1117')
        self.fig.canvas.mpl_connect('close_event', lambda e: sys.exit(0))
        self.fig.suptitle('FNO — Universal Quantum Propagator', color='white', fontsize=14, fontweight='bold')

        # Control Panel Background
        self.ax_ctrl_bg = self.fig.add_axes([0.02, 0.05, 0.22, 0.9])
        self.ax_ctrl_bg.set_facecolor('#161b22')
        self.ax_ctrl_bg.set_xticks([]); self.ax_ctrl_bg.set_yticks([])
        for spine in self.ax_ctrl_bg.spines.values(): spine.set_color('#30363d')
        self.ax_ctrl_bg.text(0.5, 0.98, 'DASHBOARD CONTROLS', color='white', ha='center', va='top', fontweight='bold', transform=self.ax_ctrl_bg.transAxes)

        # Mode Radio
        ax_radio = self.fig.add_axes([0.04, 0.81, 0.18, 0.08], facecolor='#161b22')
        self.radio_mode = RadioButtons(ax_radio, ('Train', 'Inference'), active=0 if self.mode=="Train" else 1)
        for label in self.radio_mode.labels: label.set_color('white')
        self.radio_mode.on_clicked(self.on_mode_change)

        # Initial State Sliders
        ax_x0 = self.fig.add_axes([0.08, 0.75, 0.12, 0.02], facecolor='#161b22')
        self.sl_x0 = Slider(ax_x0, 'x₀', -8.0, 8.0, valinit=self.x0, color='#58a6ff')
        
        ax_k0 = self.fig.add_axes([0.08, 0.70, 0.12, 0.02], facecolor='#161b22')
        self.sl_k0 = Slider(ax_k0, 'k₀', -8.0, 8.0, valinit=self.k0, color='#58a6ff')
        
        ax_sig = self.fig.add_axes([0.08, 0.65, 0.12, 0.02], facecolor='#161b22')
        self.sl_sig = Slider(ax_sig, 'σ', 0.2, 2.0, valinit=self.sigma, color='#58a6ff')
        
        for sl in [self.sl_x0, self.sl_k0, self.sl_sig]:
            sl.label.set_color('white'); sl.valtext.set_color('white')
            sl.on_changed(self.on_param_change)

        # Potential Presets
        btn_c = '#21262d'; btn_hc = '#30363d'
        
        ax_b1 = self.fig.add_axes([0.04, 0.55, 0.08, 0.035])
        self.btn_clear = Button(ax_b1, 'Free Space', color=btn_c, hovercolor=btn_hc)
        self.btn_clear.label.set_color('white'); self.btn_clear.on_clicked(self.on_clear)
        
        ax_b2 = self.fig.add_axes([0.14, 0.55, 0.08, 0.035])
        self.btn_barr = Button(ax_b2, 'Barrier', color=btn_c, hovercolor=btn_hc)
        self.btn_barr.label.set_color('white'); self.btn_barr.on_clicked(self.on_barrier)

        ax_b3 = self.fig.add_axes([0.04, 0.50, 0.08, 0.035])
        self.btn_well = Button(ax_b3, 'Well', color=btn_c, hovercolor=btn_hc)
        self.btn_well.label.set_color('white'); self.btn_well.on_clicked(self.on_well)
        
        ax_b4 = self.fig.add_axes([0.14, 0.50, 0.08, 0.035])
        self.btn_dbl = Button(ax_b4, 'Double Well', color=btn_c, hovercolor=btn_hc)
        self.btn_dbl.label.set_color('white'); self.btn_dbl.on_clicked(self.on_double)

        ax_time = self.fig.add_axes([0.08, 0.28, 0.12, 0.02], facecolor='#161b22')
        self.sl_time = Slider(ax_time, 'Time', 0.0, 3.0, valinit=0.0, color='#00b4d8')
        self.sl_time.label.set_color('white'); self.sl_time.valtext.set_color('white')
        self.sl_time.on_changed(self.on_time_change)

        # Training controls
        ax_btrain = self.fig.add_axes([0.04, 0.75, 0.18, 0.05])
        self.btn_train_toggle = Button(ax_btrain, 'Start Training', color='#238636', hovercolor='#2ea043')
        self.btn_train_toggle.label.set_color('white'); self.btn_train_toggle.label.set_fontweight('bold')
        self.btn_train_toggle.on_clicked(self.on_train_toggle)

        ax_bload = self.fig.add_axes([0.04, 0.69, 0.08, 0.035])
        self.btn_load = Button(ax_bload, 'Load Saved', color=btn_c, hovercolor=btn_hc)
        self.btn_load.label.set_color('white'); self.btn_load.on_clicked(self.on_load_saved)

        ax_breinit = self.fig.add_axes([0.14, 0.69, 0.08, 0.035])
        self.btn_reinit = Button(ax_breinit, 'Re-init', color=btn_c, hovercolor=btn_hc)
        self.btn_reinit.label.set_color('white'); self.btn_reinit.on_clicked(self.on_reinit_model)

        self.status_text = self.fig.text(0.13, 0.20, 'Status: Idle', color='#ff7b72', ha='center', va='center', fontweight='bold')

        # --- Plots ---
        self.ax_loss = self.fig.add_axes([0.28, 0.70, 0.68, 0.22], facecolor='#161b22')
        self.ax_V = self.fig.add_axes([0.28, 0.40, 0.68, 0.22], facecolor='#161b22')
        self.ax_psi = self.fig.add_axes([0.28, 0.08, 0.68, 0.25], facecolor='#161b22')
        
        for ax in (self.ax_loss, self.ax_V, self.ax_psi):
            ax.tick_params(colors='#8b949e')
            for sp in ax.spines.values(): sp.set_color('#30363d')
            ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

        self.ax_loss.set_title('Training Loss', color='white')
        self.ax_loss.set_yscale('log')
        self.ax_loss.tick_params(axis='y', colors='#8b949e', which='both')
        self.line_loss, = self.ax_loss.plot([], [], color='#58a6ff', lw=2)
        self.ax_loss.yaxis.get_offset_text().set_color('white')

        self.ax_V.set_title('Potential V(x) — Draw manually or use presets!', color='white')
        self.ax_V.set_xlim(X_MIN, X_MAX); self.ax_V.set_ylim(-15, 15)
        self.line_V_true, = self.ax_V.plot([], [], 'w-', lw=2, label='V(x)')
        self.ink_trail, = self.ax_V.plot([], [], color='#ffa657', lw=2, alpha=0.7, ls='--')
        self.V_fill_pos = None; self.V_fill_neg = None

        self.ax_psi.set_title('Wavefunction', color='white')
        self.ax_psi.set_xlim(X_MIN, X_MAX); self.ax_psi.set_ylim(-0.4, 0.8)
        
        self.psi_bg_img = self.ax_psi.imshow(
            np.zeros((1, len(x_np))),
            extent=[X_MIN, X_MAX, 0, 1], aspect='auto', cmap='coolwarm_r',
            alpha=0.3, transform=self.ax_psi.get_xaxis_transform(),
            vmin=-10, vmax=10, zorder=0)

        self.line_psi_true, = self.ax_psi.plot([], [], 'w-', lw=2, label='True |ψ|²')
        self.line_psi_fno, = self.ax_psi.plot([], [], '#ff4757', lw=2, ls='--', label='FNO |ψ|²')
        self.line_re_true, = self.ax_psi.plot([], [], '#00d0ff', lw=1, alpha=0.5, label='True Re(ψ)')
        self.line_re_fno, = self.ax_psi.plot([], [], '#ffa502', lw=1, ls=':', label='FNO Re(ψ)')
        self.ax_psi.legend(facecolor='#161b22', labelcolor='white')

        # Mouse events for drawing
        self.fig.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.fig.canvas.mpl_connect('button_release_event', self.on_mouse_release)

        self.update_mode_ui()

    def update_mode_ui(self):
        is_train = (self.mode == "Train")
        self.ax_loss.set_visible(is_train)
        if is_train:
            self.ax_V.set_position([0.28, 0.40, 0.68, 0.22])
            self.ax_psi.set_position([0.28, 0.08, 0.68, 0.25])
        else:
            self.ax_V.set_position([0.28, 0.55, 0.68, 0.37])
            self.ax_psi.set_position([0.28, 0.08, 0.68, 0.40])
            
        self.btn_train_toggle.ax.set_visible(is_train)
        self.btn_train_toggle.set_active(is_train)
        self.btn_load.ax.set_visible(is_train)
        self.btn_load.set_active(is_train)
        self.btn_reinit.ax.set_visible(is_train)
        self.btn_reinit.set_active(is_train)
        
        # Hide/Show inference controls
        for widget in [self.sl_x0, self.sl_k0, self.sl_sig, self.sl_time,
                       self.btn_clear, self.btn_barr, self.btn_well, self.btn_dbl]:
            widget.ax.set_visible(not is_train)
            widget.set_active(not is_train)
            
        if is_train:
            self.status_text.set_text('Status: Training Paused' if not self.is_training else 'Status: Training (Auto-saving)')
            current_bumps = min(15, 1 + (self.ep // 1000))
            self.ax_V.set_title(f"Random Landscape ({current_bumps} bumps)", color='white')
        else:
            self.status_text.set_text('Status: Inference Mode')
            self.is_training = False
            self.btn_train_toggle.label.set_text('Start Training')
            self.btn_train_toggle.color = '#238636'
            self.btn_train_toggle.ax.set_facecolor('#238636')
            self.ax_V.set_title('Potential V(x) — Draw manually or use presets!', color='white')
            
        self.fig.canvas.draw_idle()

    def on_train_toggle(self, event):
        if self.mode != "Train": return
        self.is_training = not self.is_training
        if self.is_training:
            self.btn_train_toggle.label.set_text('Stop Training')
            self.btn_train_toggle.color = '#da3633'
            self.btn_train_toggle.hovercolor = '#f85149'
            self.status_text.set_text('Status: Training (Auto-saving)')
        else:
            self.btn_train_toggle.label.set_text('Start Training')
            self.btn_train_toggle.color = '#238636'
            self.btn_train_toggle.hovercolor = '#2ea043'
            self.status_text.set_text('Status: Training Paused (Saved to disk)')
            torch.save(self.model.state_dict(), WEIGHTS_PATH)
        
        self.btn_train_toggle.ax.set_facecolor(self.btn_train_toggle.color)
        self.fig.canvas.draw_idle()

    def on_mode_change(self, label):
        self.mode = label
        self.update_mode_ui()

    def on_param_change(self, val):
        self.x0 = self.sl_x0.val
        self.k0 = self.sl_k0.val
        self.sigma = self.sl_sig.val
        self.psi_history = None
        self._show_initial()

    def _show_initial(self):
        psi0 = data_gen.gaussian_packet(x_np, self.x0, self.sigma, self.k0)
        self.line_psi_true.set_data(x_np, np.abs(psi0)**2)
        self.line_psi_fno.set_data([], [])
        self.line_re_true.set_data(x_np, np.real(psi0))
        self.line_re_fno.set_data([], [])
        self._update_V_plot()
        self.fig.canvas.draw_idle()

    # ---- Presets & Train Controls ----
    def on_load_saved(self, event):
        if os.path.exists(WEIGHTS_PATH):
            self.model.load_state_dict(torch.load(WEIGHTS_PATH, map_location=DEVICE))
            self.status_text.set_text('Status: Loaded Saved Weights!')
            self.fig.canvas.draw_idle()

    def on_reinit_model(self, event):
        self.model = implementation_tasks.FNO1d().to(DEVICE)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-4, weight_decay=1e-4)
        self.scheduler = torch.optim.lr_scheduler.OneCycleLR(self.optimizer, max_lr=2e-3, steps_per_epoch=1, epochs=50000)
        self.ep = 0
        self.loss_hist = []
        self.ax_loss.clear()
        self.ax_loss.set_title('Training Loss', color='white')
        self.ax_loss.set_yscale('log')
        self.ax_loss.tick_params(axis='y', colors='#8b949e', which='both')
        for sp in self.ax_loss.spines.values(): sp.set_color('#30363d')
        self.ax_loss.grid(True, color='#2a2a4a', ls='--', alpha=0.6)
        self.line_loss, = self.ax_loss.plot([], [], color='#58a6ff', lw=2)
        self.ax_loss.yaxis.get_offset_text().set_color('white')
        self.status_text.set_text('Status: Model Re-initialized!')
        self.fig.canvas.draw_idle()

    def on_clear(self, event):
        self.V_drawn = np.zeros(N_X); self._reset_sim()
    def on_barrier(self, event):
        self.V_drawn = np.where(np.abs(x_np) < 0.5, 8.0, 0.0); self._reset_sim()
    def on_well(self, event):
        self.V_drawn = np.where(np.abs(x_np) < 1.0, -8.0, 0.0); self._reset_sim()
    def on_double(self, event):
        self.V_drawn = np.where((np.abs(x_np) < 1.5) & (np.abs(x_np) > 0.3), 10.0, 0.0); self._reset_sim()

    def _reset_sim(self):
        self.psi_history = None
        self.V_drawn = gaussian_filter1d(self.V_drawn, sigma=2)
        self._update_V_plot()
        self.fig.canvas.draw_idle()

    # ---- Drawing ----
    def on_mouse_press(self, event):
        if self.mode == "Train" or event.inaxes != self.ax_V: return
        self.drawing = True
        self.draw_xs.clear(); self.draw_ys.clear()

    def on_mouse_move(self, event):
        if not self.drawing or event.inaxes != self.ax_V: return
        self.draw_xs.append(event.xdata)
        self.draw_ys.append(event.ydata)
        self.ink_trail.set_data(self.draw_xs, self.draw_ys)
        self.fig.canvas.draw_idle()

    def on_mouse_release(self, event):
        if not self.drawing: return
        self.drawing = False
        self.ink_trail.set_data([], [])
        if len(self.draw_xs) < 2: return

        order = np.argsort(self.draw_xs)
        dx_a, dy_a = np.array(self.draw_xs)[order], np.array(self.draw_ys)[order]
        _, ui = np.unique(dx_a, return_index=True)
        dx_a, dy_a = dx_a[ui], dy_a[ui]

        if len(dx_a) > 1:
            f = interp1d(dx_a, dy_a, kind='linear', bounds_error=False, fill_value=np.nan)
            V_new = f(x_np)
            mask = ~np.isnan(V_new)
            self.V_drawn[mask] = V_new[mask]
            self.V_drawn = gaussian_filter1d(self.V_drawn, sigma=2)
            self.psi_history = None
            self._update_V_plot()
            self.fig.canvas.draw_idle()

    def _update_V_plot(self):
        self.line_V_true.set_data(x_np, self.V_drawn)
        if self.V_fill_pos: self.V_fill_pos.remove()
        if self.V_fill_neg: self.V_fill_neg.remove()
        self.V_fill_pos = self.ax_V.fill_between(x_np, 0, self.V_drawn, where=(self.V_drawn >= 0), color='#00b4d8', alpha=0.3)
        self.V_fill_neg = self.ax_V.fill_between(x_np, 0, self.V_drawn, where=(self.V_drawn < 0), color='#f77f00', alpha=0.3)
        self.psi_bg_img.set_data(self.V_drawn[None, :])

    # ---- SSFM & Inference ----
    def on_simulate(self, event=None):
        if self.mode == "Train": return
        self.status_text.set_text('Status: Simulating Exact Physics...')
        self.fig.canvas.draw_idle(); self.fig.canvas.flush_events()

        psi_init = data_gen.gaussian_packet(x_np, self.x0, self.sigma, self.k0)
        self.psi_history = []
        psi = psi_init.copy()
        
        steps = int(3.0 / DT)
        for i in range(steps + 1):
            if i % 10 == 0:
                self.psi_history.append((i * DT, psi.copy()))
            psi = data_gen.np_split_operator_step(psi, k_np, self.V_drawn, DT)
            
        self.status_text.set_text('Status: Ready. Scrub time.')
        if event is not None:
            self.on_time_change(self.sl_time.val)

    def on_time_change(self, val):
        if self.mode == "Train": return
        
        if self.psi_history is None:
            self.on_simulate(None)
            
        t_target = val
        
        if self.psi_history is not None:
            idx = min(int((t_target / 3.0) * len(self.psi_history)), len(self.psi_history)-1)
            psi_true = self.psi_history[idx][1]
            self.line_psi_true.set_data(x_np, np.abs(psi_true)**2)
            self.line_re_true.set_data(x_np, np.real(psi_true))
            self.ax_psi.set_title(f"Wavepacket (t = {t_target:.2f})", color='white')
        
        with torch.no_grad():
            V_t = torch.tensor(self.V_drawn, dtype=torch.float32, device=DEVICE).unsqueeze(0)
            x_t = torch.tensor(x_np, dtype=torch.float32, device=DEVICE).unsqueeze(0).unsqueeze(-1)
            t_t = torch.tensor([[t_target]], dtype=torch.float32, device=DEVICE)
            psi0_val = data_gen.gaussian_packet(x_np, self.x0, self.sigma, self.k0)
            psi0_t = torch.tensor(psi0_val, dtype=torch.complex64, device=DEVICE).unsqueeze(0)
            
            V_in = V_t.unsqueeze(-1) / 10.0
            psi0_re = psi0_t.real.unsqueeze(-1)
            psi0_im = psi0_t.imag.unsqueeze(-1)
            
            out = self.model(V_in, x_t, t_t, psi0_re, psi0_im)
            pred_re, pred_im = out[0, ..., 0], out[0, ..., 1]
            pred_dens = (pred_re**2 + pred_im**2).cpu().numpy()
            
            self.line_psi_fno.set_data(x_np, pred_dens)
            self.line_re_fno.set_data(x_np, pred_re.cpu().numpy())
            
        self.fig.canvas.draw_idle()

    # ---- Training Loop ----
    def train_step(self):
        self.ep += 1
        
        # 1. Generate live batch on GPU
        current_bumps = min(15, 1 + (self.ep // 1000))
        V_b, psi_history, psi0_b = self.ssfm.generate_batch(batch_size=self.BATCH, num_bumps=current_bumps)
        
        # Select random target time index (0 to 59 frames)
        t_indices = torch.randint(0, 60, (self.BATCH,), device=DEVICE)
        psi_true = psi_history[torch.arange(self.BATCH), t_indices]
        t_b = ((t_indices + 1) * 0.05).unsqueeze(1).float()
        
        # Format inputs for FNO
        batch, N_x = V_b.shape[0], V_b.shape[1]
        x_coord = torch.tensor(x_np, dtype=torch.float32, device=DEVICE).unsqueeze(0).unsqueeze(-1).expand(batch, N_x, 1)
        V_in = V_b.unsqueeze(-1) / 10.0
        psi0_re = psi0_b.real.unsqueeze(-1)
        psi0_im = psi0_b.imag.unsqueeze(-1)

        self.optimizer.zero_grad()
        out = self.model(V_in, x_coord, t_b, psi0_re, psi0_im)
        
        pred_re = out[..., 0]
        pred_im = out[..., 1]
        pred_env = out[..., 2]
        
        true_re = psi_true.real
        true_im = psi_true.imag
        true_dens = true_re**2 + true_im**2

        # Physics-Informed Loss Components
        mse_loss = (torch.mean((pred_re - true_re)**2) +
                    torch.mean((pred_im - true_im)**2) +
                    torch.mean((pred_env - true_dens)**2))

        norm_pred = torch.sum(pred_env * dx, dim=1)
        norm_loss = torch.mean((norm_pred - 1.0)**2)

        fft_loss = (torch.mean(torch.abs(torch.fft.rfft(pred_re) - torch.fft.rfft(true_re))) +
                    torch.mean(torch.abs(torch.fft.rfft(pred_im) - torch.fft.rfft(true_im))))

        loss = mse_loss + 0.1 * norm_loss + 0.05 * fft_loss
        
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()
        self.scheduler.step()
        self.loss_hist.append(loss.item())

        update_freq = 10 if DEVICE != 'cpu' else 2
        if self.ep == 1 or self.ep % update_freq == 0:
            torch.save(self.model.state_dict(), WEIGHTS_PATH)
            self.line_loss.set_data(range(len(self.loss_hist)), self.loss_hist)
            
            # Safely calculate limits
            valid_loss = [l for l in self.loss_hist if not np.isnan(l) and not np.isinf(l)]
            if valid_loss:
                self.ax_loss.set_xlim(0, max(10, len(valid_loss)))
                self.ax_loss.set_ylim(min(valid_loss)*0.9, max(valid_loss)*1.1)
            
            with torch.no_grad():
                true_dens_disp = true_dens[0].cpu().numpy()
                pred_dens_disp = pred_env[0].cpu().numpy()
                true_re_disp = true_re[0].cpu().numpy()
                pred_re_disp = pred_re[0].cpu().numpy()
                
                self.V_drawn = V_b[0].cpu().numpy()
                self._update_V_plot()
                self.line_psi_true.set_data(x_np, true_dens_disp)
                self.line_psi_fno.set_data(x_np, pred_dens_disp)
                self.line_re_true.set_data(x_np, true_re_disp)
                self.line_re_fno.set_data(x_np, pred_re_disp)
                
                T_true = calculate_transmission_np(true_dens_disp, x_np)
                T_pred = calculate_transmission_np(pred_dens_disp, x_np)
                self.line_psi_true.set_label(f'True |ψ|² (T={T_true:.3f})')
                self.line_psi_fno.set_label(f'FNO |ψ|² (T={T_pred:.3f})')
                self.ax_psi.legend(facecolor='#161b22', labelcolor='white')
                
                self.ax_psi.set_title(f"Wavepacket (t={t_b[0].item():.2f})", color='white')
                self.ax_V.set_title(f"Random Landscape ({current_bumps} bumps)", color='white')
            self.fig.canvas.draw_idle()

    def run(self):
        plt.ion(); plt.show()
        while plt.fignum_exists(self.fig.number):
            if self.mode == "Train" and self.is_training:
                self.train_step()
                plt.pause(0.01)
            else:
                plt.pause(0.1)

if __name__ == '__main__':
    Dashboard().run()
