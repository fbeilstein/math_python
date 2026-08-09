import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import odeint
import implementation_tasks as tasks
from base_level import BaseLevel


class Level3Slaving(BaseLevel):
    """Synergetics sandbox with vector field, ghost trail, and slaved comparison."""

    def __init__(self, fig=None):
        super().__init__(fig)

    def draw(self):
        self.fig.clear(); self.fig.patch.set_facecolor('#0f172a')
        grid = self.fig.add_gridspec(1, 2, wspace=.35)
        self.ax_phase = self.fig.add_subplot(grid[0, 0])
        self.ax_distance = self.fig.add_subplot(grid[0, 1])
        self.axes = [self.ax_phase, self.ax_distance]
        self._style_ax(self.ax_phase, 'Click to launch a trajectory', '$u$', '$v$')
        self._style_ax(self.ax_distance, 'Approach to the slaved manifold', 'time',
                       r'$|v-u^2/\gamma_v|$')
        self.fig.subplots_adjust(bottom=.18, top=.90, left=.08, right=.96)
        self.gamma_u, self.gamma_v = .12, 2.0
        self.initial = np.array([1.4, 2.8])

        # Phase portrait elements
        u = np.linspace(-2.2, 2.2, 300)
        (self.manifold,) = self.ax_phase.plot(u, u * u / self.gamma_v, '--', color='#ff5f87',
                                               lw=2, label=r'$v=u^2/\gamma_v$')
        (self.traj_line,) = self.ax_phase.plot([], [], color='#55d6ff', lw=1.5, alpha=0.35)
        # Slaved 1D trajectory for comparison
        (self.slaved_line,) = self.ax_phase.plot([], [], color='#ffcc66', lw=2.2, ls=':',
                                                  label='1D slaved model')
        self.point = self.ax_phase.scatter([], [], s=70, color='#ffcc66',
                                            edgecolors='white', zorder=8)

        # Distance panel
        (self.dist_line,) = self.ax_distance.semilogy([], [], color='#a3ffb0', lw=2)
        self.dist_dot = self.ax_distance.scatter([], [], s=45, color='#ffcc66', zorder=5)

        self.ax_phase.legend(facecolor='#16213e', labelcolor='white', fontsize=7)
        self.status = self.ax_phase.text(.03, .96, '', transform=self.ax_phase.transAxes,
                                          va='top', color='white', fontsize=8,
                                          bbox=dict(boxstyle='round,pad=.35', facecolor='#26354f',
                                                    edgecolor='none'))

        # Slider & buttons
        slider_ax = self.fig.add_axes([.18, .065, .42, .028], facecolor='#26354f')
        self.gamma_slider = Slider(slider_ax, r'$\gamma_v$', .4, 5.,
                                    valinit=self.gamma_v, color='#55d6ff')
        self.register_widget(self.gamma_slider)
        self.gamma_slider.on_changed(self._set_gamma)
        self.add_button([.72, .045, .16, .07], 'Play / Pause', self.toggle_animation)
        self.cids.append(self.fig.canvas.mpl_connect('button_press_event', self._launch))
        self._recompute()

    def _set_gamma(self, value):
        self.gamma_v = float(value); self._recompute()

    def _launch(self, event):
        if event.inaxes == self.ax_phase and event.xdata is not None and event.ydata is not None:
            self.initial = np.array([event.xdata, event.ydata]); self._recompute()

    def _recompute(self):
        self.t = np.linspace(0, 18, 450)

        # Full 2D trajectory
        self.sol = odeint(tasks.synergetic_2d_rhs, self.initial, self.t,
                          args=(self.gamma_u, self.gamma_v))
        self.distance = np.abs(self.sol[:, 1] - self.sol[:, 0]**2 / self.gamma_v)

        # 1D slaved model trajectory for comparison
        u0_slaved = self.initial[0]
        sol_1d = odeint(tasks.slaved_order_parameter_rhs, [u0_slaved], self.t,
                        args=(self.gamma_u, self.gamma_v))[:, 0]
        v_slaved = sol_1d**2 / self.gamma_v
        self.slaved_traj = np.column_stack([sol_1d, v_slaved])

        # Update manifold for new gamma_v
        u = np.linspace(-2.2, 2.2, 300)
        self.manifold.set_data(u, u * u / self.gamma_v)

        # Update trajectory lines
        self.traj_line.set_data(self.sol[:, 0], self.sol[:, 1])
        self.slaved_line.set_data(sol_1d, v_slaved)
        self.dist_line.set_data(self.t, np.maximum(self.distance, 1e-8))

        # Vector field
        for c in list(self.ax_phase.collections): c.remove()
        u_lim = (-2.2, 2.2)
        v_max = max(3.6, np.max(self.sol[:, 1]) * 1.15, self.initial[1] * 1.1)
        v_lim = (-.1, v_max)
        self.draw_vector_field(self.ax_phase, tasks.synergetic_2d_rhs,
                               u_lim, v_lim, nx=16, ny=14,
                               gamma_u=self.gamma_u, gamma_v=self.gamma_v)

        self.ax_phase.set(xlim=u_lim, ylim=v_lim)
        self.ax_distance.set(xlim=(0, self.t[-1]),
                             ylim=(1e-6, max(1., np.max(self.distance) * 2)))
        self._update_frame(0)
        self.fig.canvas.draw_idle()

    def _update_frame(self, frame):
        i = int(frame) % len(self.t)
        self.point.set_offsets([self.sol[i]])
        self.dist_dot.set_offsets([[self.t[i], max(self.distance[i], 1e-8)]])

        # Ghost trail in phase space
        traj = self.sol[:, :2]
        self.draw_trail(self.ax_phase, traj, i, trail_length=60, cmap='plasma')

        self.status.set_text(f'initial = ({self.initial[0]:.2f}, {self.initial[1]:.2f})\n'
                             f'γ_v = {self.gamma_v:.2f}\n'
                             f'distance = {self.distance[i]:.3g}')
        return self.point, self.dist_dot


if __name__ == '__main__':
    level = Level3Slaving(); plt.show()
