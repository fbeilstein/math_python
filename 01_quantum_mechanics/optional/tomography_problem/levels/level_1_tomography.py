"""
Level 1 — Inverse Quantum Tomography
=======================================
Visual debugger: watch the learned potential converge to the hidden one.

Student implements functions in: implementation_tasks.py
This file only provides the visualization / test harness.

Run:  python levels/level_1_tomography.py
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
from scipy.ndimage import gaussian_filter1d
import implementation_tasks as tasks

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
psi0_np = tasks.gaussian_packet(x_np, -18.0, 0.5, 10.0)
psi0 = torch.tensor(psi0_np, dtype=torch.complex64, device=DEVICE)

# Hidden potential
V_true_np = gaussian_filter1d(np.where(np.abs(x_np) < 1.0, 25.0, 0.0), sigma=2)
V_true = torch.tensor(V_true_np, dtype=torch.float32, device=DEVICE)

# Generate observations with NumPy solver
observations = []
psi_np = psi0_np.copy()
for step in range(STEPS + 1):
    if step % SAVE_EVERY == 0:
        observations.append((step, torch.tensor(psi_np, dtype=torch.complex64, device=DEVICE)))
    if step < STEPS:
        psi_np = tasks.np_split_operator_step(psi_np, k_np, V_true_np, dt)

print(f"Device: {DEVICE} | {len(observations)} snapshots")

# ═══════════════════════════════════════════════
#  Training + Visualization
# ═══════════════════════════════════════════════
model = tasks.GridPotential(N).to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=1.0)

fig, (ax_v, ax_psi) = plt.subplots(2, 1, figsize=(10, 7))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Inverse Quantum Tomography — Discovering V(x)',
             color='white', fontsize=13, fontweight='bold')
for ax in (ax_v, ax_psi):
    ax.set_facecolor('#161b22')
    ax.tick_params(colors='#8b949e')
    for sp in ax.spines.values(): sp.set_color('#30363d')

line_vt, = ax_v.plot(x_np, V_true_np, color='#ff7b72', lw=2, label='Hidden V_true', alpha=0.5)
line_vp, = ax_v.plot(x_np, np.zeros(N), color='#79c0ff', lw=2, label='V_pred')
ax_v.set_ylim(-10, 40)
ax_v.legend(facecolor='#161b22', labelcolor='white')
ax_v.set_title("Potential", color='white')

final_true = observations[-1][1]
line_pt, = ax_psi.plot(x_np, torch.real(final_true).cpu().numpy(),
                       color='#ff7b72', lw=2, label='True Re[ψ]', alpha=0.5)
line_pp, = ax_psi.plot(x_np, np.zeros(N), color='#79c0ff', lw=2, label='Pred Re[ψ]')
ax_psi.set_ylim(-0.8, 0.8)
ax_psi.legend(facecolor='#161b22', labelcolor='white')
ax_psi.set_title("Wave at final time", color='white')

info = ax_v.text(0.02, 0.85, '', transform=ax_v.transAxes, color='white', fontfamily='monospace')

plt.ion(); plt.show()
EPOCHS = 300
t0 = time.time()

try:
    for ep in range(1, EPOCHS + 1):
        if not plt.fignum_exists(fig.number): break
        optimizer.zero_grad()
        V_pred = model()
        loss = tasks.run_teacher_forcing(V_pred, observations, psi0, k_sq, dt)
        loss.backward()
        optimizer.step()

        if ep % 5 == 0:
            with torch.no_grad():
                line_vp.set_ydata(V_pred.cpu().numpy())
                psi_fwd = psi0.clone()
                for s in range(STEPS):
                    psi_fwd = tasks.pt_split_operator_step(psi_fwd, k_sq, V_pred, dt)
                line_pp.set_ydata(torch.real(psi_fwd).cpu().numpy())
            info.set_text(f"Epoch {ep}/{EPOCHS} | Loss: {loss.item():.4e} | {ep/(time.time()-t0):.1f} it/s")
            fig.canvas.draw(); fig.canvas.flush_events()
except KeyboardInterrupt:
    pass

plt.ioff(); plt.show()
