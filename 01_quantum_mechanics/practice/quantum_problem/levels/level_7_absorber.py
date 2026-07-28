"""
Level 7 — Absorbing Boundary Conditions
==========================================
Student implements: absorbing_mask(N, gobble_frac)

Visual debugger: side-by-side comparison of the mask profile,
and how applying it to the wave packet eliminates wrap-around artifacts.
Run:
    python levels/level_7_absorber.py
    python levels/level_7_absorber.py --no-graphics
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks


# ============================================================
# GRAPHICS
# ============================================================
class Level7Absorber:

    def __init__(self):
        self.fig, (self.ax_mask, self.ax_wave) = plt.subplots(1, 2, figsize=(13, 5))
        self.fig.patch.set_facecolor('#1a1a2e')
        self.fig.suptitle('Level 7 — Absorbing Boundary Mask (Gobbler)',
                          color='white', fontsize=12, fontweight='bold')
        self.fig.subplots_adjust(bottom=0.22)

        ax_frac = plt.axes([0.15, 0.07, 0.70, 0.04])
        self.sl_frac = widgets.Slider(ax_frac, 'Absorber fraction', 0.02, 0.3,
                                      valinit=0.10, color='#ce93d8')
        self.sl_frac.label.set_color('white')
        self.sl_frac.valtext.set_color('white')
        self.sl_frac.on_changed(self._redraw)

        for ax, title in zip((self.ax_mask, self.ax_wave),
                              ('Mask profile  mask(x)', 'Wave packet after 200 steps')):
            ax.set_facecolor('#16213e')
            ax.tick_params(colors='#cccccc')
            ax.set_title(title, color='white', fontsize=10)
            for sp in ax.spines.values(): sp.set_edgecolor('#444466')
            ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

        self.draw()

    def _redraw(self, val):
        self.ax_mask.clear(); self.ax_wave.clear()
        for ax, title in zip((self.ax_mask, self.ax_wave),
                              ('Mask profile  mask(x)', 'Wave packet after 200 steps')):
            ax.set_facecolor('#16213e')
            ax.tick_params(colors='#cccccc')
            ax.set_title(title, color='white', fontsize=10)
            for sp in ax.spines.values(): sp.set_edgecolor('#444466')
            ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)
        self.draw()
        self.fig.canvas.draw_idle()

    def draw(self):
        from numpy.fft import fftfreq
        N  = 512
        L  = 40.0
        x  = np.linspace(-L/2, L/2, N, endpoint=False)
        dx = x[1] - x[0]
        k  = 2 * np.pi * fftfreq(N, d=dx)
        V  = np.zeros(N)
        dt = 0.002
        gf = self.sl_frac.val

        # -- left panel: mask --
        try:
            mask = tasks.absorbing_mask(N, gf)
            if mask is None: raise NotImplementedError()
        except Exception as e:
            self.ax_mask.text(0.5, 0.5, f'Error:\n{e}', transform=self.ax_mask.transAxes,
                              ha='center', va='center', color='#ff6e6e', fontsize=9)
            return
        self.ax_mask.plot(x, mask, color='#ce93d8', lw=2)
        gw = int(gf * N)
        self.ax_mask.axvspan(x[0], x[gw],  color='#ff7043', alpha=0.15, label='Absorbing zone')
        self.ax_mask.axvspan(x[-gw], x[-1], color='#ff7043', alpha=0.15)
        self.ax_mask.set_ylim(-0.05, 1.15)
        self.ax_mask.axhline(1.0, color='gray', ls='--', alpha=0.5)
        self.ax_mask.set_xlabel('x', color='#cccccc')
        self.ax_mask.set_ylabel('mask value', color='#cccccc')
        self.ax_mask.legend(fontsize=9, facecolor='#1a1a2e', labelcolor='white')

        # -- right panel: apply mask during evolution --
        psi = tasks.gaussian_packet(x, -L * 0.25, 1.0, 10.0)
        try:
            for _ in range(200):
                psi = tasks.split_operator_step(psi, k, V, dt)
                if psi is None: psi = np.zeros_like(x, dtype=complex)
                psi *= mask
        except Exception:
            pass
        prob = np.abs(psi)**2
        norm = np.sum(prob) * dx
        self.ax_wave.plot(x, prob, color='#4fc3f7', lw=2, label=f'|ψ|²  (norm={norm:.4f})')
        self.ax_wave.axhline(0, color='#555577', lw=0.8)
        self.ax_wave.set_xlabel('x', color='#cccccc')
        norm_color = '#81c784' if norm < 0.5 else '#ff6e6e'  # absorbed a lot
        self.ax_wave.legend(fontsize=9, facecolor='#1a1a2e', labelcolor=norm_color)



if __name__ == '__main__':
    if '--no-graphics' in sys.argv:
        sys.argv.remove('--no-graphics')
        unittest.main()
    else:
        lvl = Level7Absorber()
        plt.show()
