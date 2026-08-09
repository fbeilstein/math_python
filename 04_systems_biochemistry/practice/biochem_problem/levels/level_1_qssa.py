import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import odeint
import implementation_tasks as tasks
from base_level import BaseLevel


class Level1QSSA(BaseLevel):
    """A live comparison of the fast full model and its slow QSSA reduction."""

    def __init__(self, fig=None):
        super().__init__(fig)

    def draw(self):
        self.fig.clear()
        self.fig.patch.set_facecolor('#0f172a')
        grid = self.fig.add_gridspec(2, 2, width_ratios=[1.55, 1], hspace=.45, wspace=.38)
        self.ax_time = self.fig.add_subplot(grid[0, 0])
        self.ax_phase = self.fig.add_subplot(grid[1, 0])
        self.ax_error = self.fig.add_subplot(grid[0, 1])
        self.ax_complex = self.fig.add_subplot(grid[1, 1])
        self.axes = [self.ax_time, self.ax_phase, self.ax_error, self.ax_complex]
        self._style_ax(self.ax_time, 'Full model versus QSSA', 'time', 'substrate $S(t)$')
        self._style_ax(self.ax_phase, 'Phase portrait  (click to launch)', '$S$', 'complex $C$')
        self._style_ax(self.ax_error, 'Reduction error', r'$\varepsilon$', 'relative $L_2$ error')
        self._style_ax(self.ax_complex, 'Fast boundary layer', 'time', 'complex $C(t)$')
        self.fig.subplots_adjust(bottom=.18, top=.92, left=.08, right=.96)

        self.t = np.linspace(0, 15, 420)
        self.eps_grid = np.logspace(-3, -1, 7)
        self.epsilon = .04
        self.S0, self.C0 = 1.0, 0.0
        self.time_index = 0

        # Time series
        (self.full_line,) = self.ax_time.plot([], [], color='#55d6ff', lw=2.4, label='full $S(t)$')
        (self.qssa_line,) = self.ax_time.plot([], [], color='#ffcc66', lw=2, ls='--', label='QSSA $S(t)$')
        self.time_dot = self.ax_time.scatter([], [], s=55, color='#ff5f87', zorder=6)
        self.ax_time.legend(facecolor='#16213e', labelcolor='white', fontsize=8)

        # Phase portrait
        (self.phase_traj,) = self.ax_phase.plot([], [], color='#55d6ff', lw=1.5, alpha=0.4)
        (self.manifold_line,) = self.ax_phase.plot([], [], '--', color='#ffcc66', lw=2,
                                                    label=r'QSSA manifold $C_{eq}(S)$')
        self.phase_dot = self.ax_phase.scatter([], [], s=65, color='#ff5f87',
                                                edgecolors='white', zorder=8)
        self.ax_phase.legend(facecolor='#16213e', labelcolor='white', fontsize=7)

        # Boundary layer shading stored as a patch reference
        self._bl_patch = None

        # Complex panel
        (self.complex_line,) = self.ax_complex.plot([], [], color='#a3ffb0', lw=2)
        self.complex_dot = self.ax_complex.scatter([], [], s=45, color='#ff5f87', zorder=6)

        # Error panel
        self.error_line, = self.ax_error.loglog([], [], 'o-', color='#c792ea', lw=2)
        self.error_dot = self.ax_error.scatter([], [], s=55, color='#ffcc66', zorder=6)

        self.status = self.ax_time.text(.02, .96, '', transform=self.ax_time.transAxes, va='top',
                                         color='white', fontsize=8,
                                         bbox=dict(boxstyle='round,pad=.4', facecolor='#26354f',
                                                   edgecolor='none'))

        # Slider & buttons
        slider_ax = self.fig.add_axes([.13, .065, .50, .028], facecolor='#26354f')
        self.eps_slider = Slider(slider_ax, r'$\varepsilon=E_{tot}/S_0$', .001, .1,
                                  valinit=self.epsilon, color='#55d6ff')
        self.register_widget(self.eps_slider)
        self.eps_slider.on_changed(self._set_epsilon)
        self.add_button([.70, .045, .12, .07], 'Play / Pause', self.toggle_animation)
        self.add_button([.84, .045, .10, .07], 'Reset', self._reset, '#6c5ce7')

        # Click-to-launch in phase portrait
        self.cids.append(self.fig.canvas.mpl_connect('button_press_event', self._launch))

        self._recompute()

    def _launch(self, event):
        if event.inaxes == self.ax_phase and event.xdata is not None:
            self.S0 = np.clip(event.xdata, 0.01, 1.5)
            self.C0 = np.clip(event.ydata, 0.0, 0.15)
            self._recompute()

    def _set_epsilon(self, value):
        self.epsilon = float(value)
        self._recompute()

    def _recompute(self):
        Etot = self.epsilon
        full = odeint(tasks.full_enzyme_system_rhs, [self.S0, self.C0], self.t,
                      args=(1., 1., 1., Etot))
        reduced = odeint(tasks.qssa_reduced_rhs, [self.S0], self.t,
                         args=(1., 1., 1., Etot))[:, 0]
        self.full_S, self.complex_C, self.reduced = full[:, 0], full[:, 1], reduced

        # Error grid
        self.errors = tasks.compute_boundary_layer_error(self.eps_grid)

        # Time series
        self.full_line.set_data(self.t, self.full_S)
        self.qssa_line.set_data(self.t, self.reduced)
        self.complex_line.set_data(self.t, self.complex_C)
        self.error_line.set_data(self.eps_grid, self.errors)

        # Phase portrait: vector field + QSSA manifold + trajectory
        for c in list(self.ax_phase.collections): c.remove()
        for p in list(self.ax_phase.patches): p.remove()
        s_lim = (0, max(1.1, self.S0 * 1.15))
        c_lim = (0, max(0.035, 1.15 * np.max(self.complex_C), self.C0 * 1.15))
        self.draw_vector_field(self.ax_phase, tasks.full_enzyme_system_rhs,
                               s_lim, c_lim, nx=14, ny=12, Etot=Etot)
        S_man = np.linspace(0.01, s_lim[1], 200)
        Km = 2.0  # (k_minus1 + kcat) / k1
        C_man = Etot * S_man / (Km + S_man)
        self.manifold_line.set_data(S_man, C_man)
        self.phase_traj.set_data(full[:, 0], full[:, 1])

        # Axes limits
        self.ax_time.set_xlim(0, self.t[-1])
        self.ax_time.set_ylim(0, max(1.08, self.S0 * 1.1))
        self.ax_complex.set_xlim(0, self.t[-1])
        self.ax_complex.set_ylim(0, max(.03, 1.15 * np.max(self.complex_C)))
        self.ax_error.set_xlim(self.eps_grid[0] * .8, self.eps_grid[-1] * 1.25)
        self.ax_error.set_ylim(max(1e-5, np.min(self.errors) * .5),
                               max(.2, np.max(self.errors) * 2))
        self.ax_phase.set_xlim(*s_lim)
        self.ax_phase.set_ylim(*c_lim)

        # Boundary layer shading
        if self._bl_patch is not None:
            self._bl_patch.remove()
        bl_width = self.epsilon * 3
        self._bl_patch = self.ax_time.axvspan(0, bl_width, alpha=0.12, color='#ff5f87',
                                               zorder=0)

        self.time_index = 0
        self._update_frame(0)
        self.fig.canvas.draw_idle()

    def _update_frame(self, frame):
        self.time_index = int(frame) % len(self.t)
        i = self.time_index
        self.time_dot.set_offsets([[self.t[i], self.full_S[i]]])
        self.complex_dot.set_offsets([[self.t[i], self.complex_C[i]]])
        self.phase_dot.set_offsets([[self.full_S[i], self.complex_C[i]]])

        # Ghost trail in phase portrait
        traj = np.column_stack([self.full_S, self.complex_C])
        # Re-draw trail on each frame (clear old trail collections)
        while len(self.ax_phase.collections) > 1:
            # keep quiver (index 0), remove others
            if len(self.ax_phase.collections) > 2:
                self.ax_phase.collections[-1].remove()
            else:
                break
        self.draw_trail(self.ax_phase, traj, i, trail_length=50, cmap='cool')

        current_error = np.linalg.norm(self.full_S[:i + 1] - self.reduced[:i + 1]) / \
                        (np.linalg.norm(self.full_S[:i + 1]) + 1e-12)
        self.error_dot.set_offsets([[self.epsilon, current_error]])
        self.status.set_text(f't = {self.t[i]:.2f}   ε = {self.epsilon:.3f}\n'
                             f'relative error = {current_error:.3g}\n'
                             f'IC: S₀={self.S0:.2f}, C₀={self.C0:.2f}')
        return self.full_line, self.qssa_line, self.time_dot

    def _reset(self, _event=None):
        self.S0, self.C0 = 1.0, 0.0
        self.pause_animation()
        self._recompute()


if __name__ == '__main__':
    level = Level1QSSA(); plt.show()
