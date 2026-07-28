"""
Level 4 — Eigenfunctions of the Infinite Square Well
=======================================================
Student implements: well_eigenfunction(x, n, L)

Visual debugger: slider for quantum number n (continuous!).
Watch what happens when n is not a positive integer — the boundary condition
psi(L) ≠ 0 is violated, proving quantization is necessary.
Run:
    python levels/level_4_eigenfunctions.py
    python levels/level_4_eigenfunctions.py --no-graphics
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks


# ============================================================
# GRAPHICS & INTERACTION
# ============================================================
class Level4Eigenfunctions:

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.fig.patch.set_facecolor('#1a1a2e')
        self.fig.suptitle('Level 4 — Eigenfunctions of the Infinite Square Well',
                          color='white', fontsize=12, fontweight='bold')
        self.fig.subplots_adjust(bottom=0.28)

        ax_n = plt.axes([0.15, 0.10, 0.70, 0.04])
        self.sl_n = widgets.Slider(ax_n, 'Quantum number $n$', 0.5, 7.0,
                                   valinit=1.0, valstep=0.05, color='#4fc3f7')
        self.sl_n.label.set_color('white')
        self.sl_n.valtext.set_color('white')
        self.sl_n.on_changed(self._redraw)

        self.ax.set_facecolor('#16213e')
        self.ax.tick_params(colors='#cccccc')
        for sp in self.ax.spines.values():
            sp.set_edgecolor('#444466')

        self.draw()

    def disconnect_events(self):
        self.sl_n.disconnect_events()

    def _redraw(self, val):
        self.ax.clear(); self.ax.set_facecolor('#16213e')
        for sp in self.ax.spines.values(): sp.set_edgecolor('#444466')
        self.draw()
        self.fig.canvas.draw_idle()

    def draw(self):
        L = 10.0
        x = np.linspace(0, L, 1024, endpoint=False)
        n = self.sl_n.val

        self.ax.tick_params(colors='#cccccc')
        self.ax.set_xlabel('x', color='#cccccc')
        self.ax.set_ylabel('ψₙ(x)', color='#cccccc')
        self.ax.grid(True, color='#2a2a4a', ls='--', alpha=0.6)

        # Draw infinite walls
        self.ax.axvline(0,  color='white', lw=4, zorder=5)
        self.ax.axvline(L,  color='white', lw=4, zorder=5)
        self.ax.axvspan(-0.5, 0, color='#37474f', alpha=0.5)
        self.ax.axvspan(L, L+0.5, color='#37474f', alpha=0.5)
        self.ax.text(-0.25, 0.8, 'V=∞', transform=self.ax.get_xaxis_transform(),
                     ha='center', color='white', fontsize=12, fontweight='bold')
        self.ax.text(L+0.25, 0.8, 'V=∞', transform=self.ax.get_xaxis_transform(),
                     ha='center', color='white', fontsize=12, fontweight='bold')

        try:
            psi = tasks.well_eigenfunction(x, n, L)
            if psi is None: psi = np.zeros_like(x, dtype=complex)
        except Exception as e:
            self.ax.text(0.5, 0.5, f'Error:\n{e}', transform=self.ax.transAxes,
                         ha='center', va='center', color='#ff6e6e', fontsize=10)
            return

        # Is n close to an integer?
        is_integer_n = abs(n - round(n)) < 0.05 and round(n) >= 1
        color = '#4fc3f7' if is_integer_n else '#ff7043'
        self.ax.plot(x, psi, color=color, lw=2.5, label=f'ψ_n(x),  n = {n:.2f}')
        self.ax.axhline(0, color='#555577', lw=0.8)
        self.ax.set_xlim(-0.5, L + 0.5)

        # Boundary condition readout
        bc_left  = psi[0]
        bc_right = psi[-1]
        bc_ok    = abs(bc_left) < 0.05 and abs(bc_right) < 0.05
        bc_color = '#81c784' if bc_ok else '#ff6e6e'
        self.ax.scatter([0, L], [bc_left, bc_right], color=bc_color, s=80, zorder=10)
        bc_label = '✓ Boundary cond. satisfied' if bc_ok else '✗ Boundary cond. VIOLATED'
        self.ax.text(0.98, 0.95, bc_label,
                     transform=self.ax.transAxes, ha='right', va='top',
                     color=bc_color, fontsize=11, fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))

        if is_integer_n:
            dx = x[1] - x[0]
            norm = np.sum(psi**2) * dx
            self.ax.text(0.02, 0.95, f'∫ψ² dx = {norm:.4f}',
                         transform=self.ax.transAxes, ha='left', va='top',
                         color='#ffcc80', fontsize=9,
                         bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8))

        self.ax.legend(loc='lower right', fontsize=10, facecolor='#1a1a2e', labelcolor='white')



if __name__ == '__main__':
    if '--no-graphics' in sys.argv:
        sys.argv.remove('--no-graphics')
        unittest.main()
    else:
        lvl = Level4Eigenfunctions()
        plt.show()
