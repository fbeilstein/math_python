"""
Level 1 — Mini Fourier Neural Operator
=========================================
Visual debugger: watch the FNO learn to predict quantum dynamics.

Student implements functions in: implementation_tasks.py
This file only provides the visualization / training harness.

Run:  python levels/level_1_fno.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
import time

import implementation_tasks as tasks

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# ═══════════════════════════════════════════════
#  Physics Setup
# ═══════════════════════════════════════════════
N_X = 256
X_MIN, X_MAX = -10.0, 10.0
DT = 0.005

x_np = np.linspace(X_MIN, X_MAX, N_X, endpoint=False)
dx = x_np[1] - x_np[0]

# ═══════════════════════════════════════════════
#  Generate Training Data
# ═══════════════════════════════════════════════
print(f"Device: {DEVICE}")
print("Generating training data with NumPy SSFM...")
N_TRAIN, BATCH = 256, 32
train_data = [tasks.generate_training_sample(x_np, dx, DT, 600) for _ in range(N_TRAIN)]
print(f"Done: {N_TRAIN} samples.")

# ═══════════════════════════════════════════════
#  Initialize Student Model
# ═══════════════════════════════════════════════
model = tasks.MiniFNO(modes=32, width=32).to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# ═══════════════════════════════════════════════
#  Training + Visualization
# ═══════════════════════════════════════════════
fig, (ax_loss, ax_wave) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Mini FNO — Learning the Time-Evolution Operator',
             color='white', fontsize=13, fontweight='bold')
for ax in (ax_loss, ax_wave):
    ax.set_facecolor('#161b22')
    ax.tick_params(colors='#8b949e')
    for sp in ax.spines.values(): sp.set_color('#30363d')

loss_hist = []
plt.ion(); plt.show()
EPOCHS = 500
t0 = time.time()

try:
    for ep in range(1, EPOCHS + 1):
        if not plt.fignum_exists(fig.number): break

        idx = np.random.choice(N_TRAIN, BATCH, replace=False)
        V_b = torch.tensor(np.array([train_data[i][0] for i in idx]),
                           dtype=torch.float32, device=DEVICE)
        psi0_b = torch.tensor(np.array([train_data[i][1] for i in idx]),
                              dtype=torch.complex64, device=DEVICE)
        t_b = torch.tensor([[train_data[i][2]] for i in idx],
                           dtype=torch.float32, device=DEVICE)
        psi_true = torch.tensor(np.array([train_data[i][3] for i in idx]),
                                dtype=torch.complex64, device=DEVICE)

        optimizer.zero_grad()
        out = model(V_b, psi0_b, t_b)
        pred_re, pred_im = out[..., 0], out[..., 1]
        loss = torch.mean((pred_re - psi_true.real)**2 + (pred_im - psi_true.imag)**2)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        loss_hist.append(loss.item())

        if ep % 10 == 0:
            ax_loss.clear(); ax_wave.clear()
            for ax in (ax_loss, ax_wave):
                ax.set_facecolor('#161b22'); ax.tick_params(colors='#8b949e')

            ax_loss.semilogy(loss_hist, color='#58a6ff', lw=2)
            ax_loss.set_title(f"Loss (epoch {ep})", color='white')
            ax_loss.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

            with torch.no_grad():
                true_dens = (psi_true[0].real**2 + psi_true[0].imag**2).cpu().numpy()
                pred_dens = (pred_re[0]**2 + pred_im[0]**2).cpu().numpy()
                V_d = V_b[0].cpu().numpy()
                vmax = max(np.abs(V_d).max(), 1)
                ax_wave.fill_between(x_np, 0, V_d/vmax*0.3, color='#ffa657', alpha=0.15)
                ax_wave.plot(x_np, true_dens, color='white', lw=2, label='True |ψ|²')
                ax_wave.plot(x_np, pred_dens, color='#ff4757', lw=2, ls='--', label='FNO |ψ|²')
                ax_wave.set_title(f"t = {t_b[0].item():.2f}", color='white')
                ax_wave.legend(facecolor='#161b22', labelcolor='white')

            plt.tight_layout(); plt.pause(0.01)
except KeyboardInterrupt:
    pass

print(f"Done: {len(loss_hist)} epochs in {time.time()-t0:.1f}s")
plt.ioff(); plt.show()
