"""
Level 5 — Split-Operator Method
==================================
Student implements: split_operator_step(psi, k, V, dt)

Visual debugger: wave packet approaching a rectangular barrier.
Note: without an absorbing mask, the packet wraps around periodically.
Run:
    python levels/level_5_split_operator.py
    python levels/level_5_split_operator.py --no-graphics
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import matplotlib.animation as animation
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks


# ============================================================
# GRAPHICS
# ============================================================
class Level5SplitOperator:

    def __init__(self):
        self.fig = plt.figure(figsize=(11, 6))
        gs = self.fig.add_gridspec(3, 1, height_ratios=[8, 1, 3], hspace=0.05)
        self.ax      = self.fig.add_subplot(gs[0])
        self.ax_pot  = self.fig.add_subplot(gs[1])   # potential strip
        self.ax_norm = self.fig.add_subplot(gs[2])
        self.fig.patch.set_facecolor('#1a1a2e')
        self.fig.suptitle('Level 5 — Split-Operator: Barrier Scattering (no absorber)',
                          color='white', fontsize=12, fontweight='bold')
        self.fig.subplots_adjust(bottom=0.22)

        # Grid
        L  = 40.0
        N  = 1024
        self.x  = np.linspace(-L/2, L/2, N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        from numpy.fft import fftfreq
        self.k_grid = 2 * np.pi * fftfreq(N, d=self.dx)
        self.L      = L
        self.dt     = 0.002
        self.V0     = 25.0
        self.a      = 0.5

        # Slider
        ax_v0 = plt.axes([0.15, 0.08, 0.70, 0.03])
        self.sl_v0 = widgets.Slider(ax_v0, 'Barrier height $V_0$', 0, 60, valinit=self.V0, color='#ff7043')
        self.sl_v0.on_changed(self._reset)

        btn_ax = plt.axes([0.82, 0.10, 0.10, 0.06])
        self.btn = widgets.Button(btn_ax, 'Reset', color='#81c784', hovercolor='#66bb6a')
        self.btn.on_clicked(self._reset)

        self._init_state()
        self._setup_plots()

        self.anim = animation.FuncAnimation(
            self.fig, self._animate, interval=30, blit=False, cache_frame_data=False)

    def disconnect_events(self):
        self.sl_v0.disconnect_events()

    def _init_state(self):
        self.V0   = self.sl_v0.val
        self.V    = np.where(np.abs(self.x) < self.a / 2, self.V0, 0.0)
        self.psi  = tasks.gaussian_packet(self.x, -self.L * 0.25, 1.0, 10.0)
        self.norms = []
        self.t     = 0.0

    def _reset(self, event=None):
        self._init_state()
        self.ax.clear(); self.ax_pot.clear(); self.ax_norm.clear()
        self._setup_plots()

    def _setup_plots(self):
        for a in (self.ax, self.ax_pot, self.ax_norm):
            a.set_facecolor('#16213e')
            a.tick_params(colors='#cccccc')
            for sp in a.spines.values(): sp.set_edgecolor('#444466')

        self.ax.set_xlim(self.x[0], self.x[-1])
        y_max = np.max(np.abs(self.psi)**2) * 2.5
        self.ax.set_ylim(-y_max * 0.2, y_max)
        self.ax.set_ylabel('|ψ|²', color='#cccccc')
        self.ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

        self.prob_line, = self.ax.plot(self.x, np.abs(self.psi)**2, color='#4fc3f7', lw=2)
        self.real_line, = self.ax.plot(self.x, self.psi.real, color='#81c784', lw=1, alpha=0.5)
        self.time_text  = self.ax.text(0.02, 0.96, '', transform=self.ax.transAxes,
                                       color='#ffcc80', fontsize=10, va='top',
                                       bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))

        # Potential strip (colorized)
        V_strip = np.tile(self.V, (2, 1))
        self.ax_pot.imshow(V_strip, aspect='auto',
                           extent=[self.x[0], self.x[-1], 0, 1],
                           cmap='hot', vmin=0, vmax=max(1, self.V0),
                           origin='lower')
        self.ax_pot.set_xlim(self.x[0], self.x[-1])
        self.ax_pot.set_yticks([])
        self.ax_pot.set_xticks([])
        self.ax_pot.text(0.01, 0.5, 'V(x)', transform=self.ax_pot.transAxes,
                         va='center', color='#ffcc80', fontsize=9)

        self.norm_line, = self.ax_norm.plot([], [], color='#ce93d8', lw=1.5)
        self.ax_norm.set_xlim(0, 400)
        self.ax_norm.set_ylim(0, 1.2)
        self.ax_norm.axhline(1.0, color='gray', ls='--', alpha=0.5)
        self.ax_norm.set_xlabel('Frame', color='#cccccc')
        self.ax_norm.set_ylabel('∫|ψ|²dx', color='#cccccc')
        self.ax_norm.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

    def _animate(self, frame):
        try:
            for _ in range(12):
                self.psi = tasks.split_operator_step(self.psi, self.k_grid, self.V, self.dt)
            self.t += 12 * self.dt
        except Exception:
            return
        prob = np.abs(self.psi)**2
        self.prob_line.set_ydata(prob)
        self.real_line.set_ydata(self.psi.real)
        norm = np.sum(prob) * self.dx
        self.norms.append(norm)
        if len(self.norms) > self.ax_norm.get_xlim()[1]:
            self.ax_norm.set_xlim(0, len(self.norms) + 50)
        self.norm_line.set_data(range(len(self.norms)), self.norms)
        self.time_text.set_text(f't = {self.t:.2f} | norm = {norm:.4f}')



if __name__ == '__main__':
    if '--no-graphics' in sys.argv:
        sys.argv.remove('--no-graphics')
        unittest.main()
    else:
        lvl = Level5SplitOperator()
        plt.show()
