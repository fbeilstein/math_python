import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import odeint
import implementation_tasks as tasks
from base_level import BaseLevel


class Level5Bioswitch(BaseLevel):
    """Bio-switch with nullclines, hysteresis loop, vector field & click-to-launch."""

    def __init__(self, fig=None):
        super().__init__(fig)

    def draw(self):
        self.fig.clear(); self.fig.patch.set_facecolor('#0f172a')
        grid = self.fig.add_gridspec(2, 3, hspace=.48, wspace=.40,
                                      width_ratios=[1, 1, 0.85])
        self.ax_signal = self.fig.add_subplot(grid[0, 0])
        self.ax_response = self.fig.add_subplot(grid[1, 0])
        self.ax_phase = self.fig.add_subplot(grid[:, 1])
        self.ax_hyst = self.fig.add_subplot(grid[:, 2])
        self.axes = [self.ax_signal, self.ax_response, self.ax_phase, self.ax_hyst]
        self._style_ax(self.ax_signal, 'Stimulus', 'time', 'signal $S(t)$')
        self._style_ax(self.ax_response, 'Switch response', 'time', 'state')
        self._style_ax(self.ax_phase, 'Phase portrait  (click to launch)', '$R$', '$E$')
        self._style_ax(self.ax_hyst, 'Hysteresis loop', 'signal $S$', 'response $R$')
        self.fig.subplots_adjust(bottom=.18, top=.92, left=.06, right=.97)
        self.amp, self.high_initial = .08, False

        # Signal panel
        self.sig_line, = self.ax_signal.plot([], [], color='#ff5f87', lw=2.4)

        # Response panel
        self.r_line, = self.ax_response.plot([], [], color='#ffcc66', lw=2, label='$R$')
        self.e_line, = self.ax_response.plot([], [], color='#55d6ff', lw=2, label='$E$')
        self.ax_response.legend(facecolor='#16213e', labelcolor='white', fontsize=8)

        # Phase portrait
        (self.traj,) = self.ax_phase.plot([], [], color='#a3ffb0', lw=1.3, alpha=0.35)
        self.dot = self.ax_phase.scatter([], [], s=65, color='#ff5f87',
                                          edgecolors='white', zorder=8)

        # Hysteresis loop
        self.hyst_high, = self.ax_hyst.plot([], [], color='#ff5f87', lw=2.2, label='high→low')
        self.hyst_low, = self.ax_hyst.plot([], [], color='#55d6ff', lw=2.2, label='low→high')
        self.hyst_marker = self.ax_hyst.scatter([], [], s=70, color='#ffcc66',
                                                 edgecolors='white', zorder=8)
        self.ax_hyst.legend(facecolor='#16213e', labelcolor='white', fontsize=7)

        self.status = self.ax_phase.text(.03, .96, '', transform=self.ax_phase.transAxes,
                                          va='top', color='white', fontsize=8,
                                          bbox=dict(boxstyle='round,pad=.35', facecolor='#26354f',
                                                    edgecolor='none'))

        # Sliders & buttons
        s_ax = self.fig.add_axes([.10, .065, .30, .028], facecolor='#26354f')
        self.slider = Slider(s_ax, 'pulse', 0., .25, valinit=self.amp, color='#ff5f87')
        self.register_widget(self.slider)
        self.slider.on_changed(self._set_amp)
        self.add_button([.47, .045, .13, .07], 'Low state', self._low_state, '#2e86ab')
        self.add_button([.61, .045, .13, .07], 'High state', self._high_state, '#6c5ce7')
        self.add_button([.75, .045, .07, .07], 'Play', self.toggle_animation)

        # Click-to-launch
        self.cids.append(self.fig.canvas.mpl_connect('button_press_event', self._launch_click))
        self.R0, self.E0 = 0., 0.45

        # Pre-compute hysteresis loop
        self._compute_hysteresis()
        self._recompute()

    def _signal(self, t):
        return tasks.gaussian_pulse(t, amp=self.amp, center=1200, width=240)

    def _set_amp(self, value):
        self.amp = float(value); self._recompute()

    def _low_state(self, _event=None):
        self.high_initial = False
        self.R0, self.E0 = 0., 0.45
        self._recompute()

    def _high_state(self, _event=None):
        self.high_initial = True
        self.R0, self.E0 = 180., 0.03
        self._recompute()

    def _launch_click(self, event):
        if event.inaxes == self.ax_phase and event.xdata is not None:
            self.R0 = max(0, event.xdata)
            self.E0 = max(0, event.ydata)
            self.high_initial = self.R0 > 50
            self._recompute()

    def _compute_hysteresis(self):
        """Pre-compute the forward/backward continuation for the hysteresis panel."""
        self.S_range = np.linspace(0.0, 0.15, 35)
        self.R_high, self.R_low, self.S_thr = tasks.hysteresis_continuation(self.S_range)
        self.hyst_high.set_data(self.S_range, self.R_high)
        self.hyst_low.set_data(self.S_range, self.R_low)
        self.ax_hyst.set_xlim(0, self.S_range[-1])
        self.ax_hyst.set_ylim(0, max(10, np.max(self.R_high) * 1.1))

    def _recompute(self):
        self.t = np.linspace(0, 3500, 700)
        initial = [self.R0, self.E0]
        self.sol = odeint(tasks.bioswitch_rhs, initial, self.t, args=(self._signal, None))
        self.signal_data = np.array([self._signal(t) for t in self.t])

        # Signal & response
        self.sig_line.set_data(self.t, self.signal_data)
        self.r_line.set_data(self.t, self.sol[:, 0])
        self.e_line.set_data(self.t, self.sol[:, 1])
        self.traj.set_data(self.sol[:, 0], self.sol[:, 1])

        self.ax_signal.set(xlim=(0, self.t[-1]),
                           ylim=(-.01, max(.03, self.amp * 1.25)))
        self.ax_response.relim(); self.ax_response.autoscale_view()

        # Phase portrait: vector field + nullclines
        for c in list(self.ax_phase.collections): c.remove()
        R_max = max(200, np.max(self.sol[:, 0]) * 1.15, self.R0 * 1.1)
        E_max = max(0.55, np.max(self.sol[:, 1]) * 1.15)
        R_lim = (0, R_max)
        E_lim = (0, E_max)

        self.draw_vector_field(self.ax_phase, tasks.bioswitch_rhs,
                               R_lim, E_lim, nx=14, ny=12,
                               S_func=lambda t: 0.0)
        self.draw_nullclines(self.ax_phase, tasks.bioswitch_rhs,
                             R_lim, E_lim, nx=250, ny=250,
                             S_func=lambda t: 0.0,
                             labels=(r'$\dot{R}=0$', r'$\dot{E}=0$'))

        self.ax_phase.set_xlim(*R_lim)
        self.ax_phase.set_ylim(*E_lim)

        # Hysteresis marker
        self.hyst_marker.set_offsets([[self.amp, self.sol[-1, 0]]])

        self._update_frame(0)
        self.fig.canvas.draw_idle()

    def _update_frame(self, frame):
        i = int(frame) % len(self.t)
        self.dot.set_offsets([self.sol[i]])

        # Ghost trail in phase space
        traj = self.sol[:, :2]
        self.draw_trail(self.ax_phase, traj, i, trail_length=60, cmap='magma')

        state = f'R₀={self.R0:.0f}, E₀={self.E0:.2f}'
        self.status.set_text(f'{state}\npulse = {self.amp:.3f}\n'
                             f'R(t) = {self.sol[i, 0]:.1f}')
        return self.dot,


if __name__ == '__main__':
    level = Level5Bioswitch(); plt.show()
