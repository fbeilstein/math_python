import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import odeint
import implementation_tasks


VIN, K1, KP = 0.36, 0.02, 6.0

def _fp(Km):
    ATP_eq = (2 * VIN * Km) / (KP - 2 * VIN)
    G_eq = VIN / (K1 * ATP_eq)
    return (G_eq, ATP_eq)

def _rhs(state, t, Km):
    G, ATP = state
    dG = VIN - K1 * G * ATP
    dATP = 2 * K1 * G * ATP - KP * ATP / (ATP + Km)
    return [dG, dATP]


class Level4Glycolysis:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.fig = plt.figure(figsize=(14, 5))
        self.fig.patch.set_facecolor('#1e1e1e')

        # ── Left: Bifurcation Diagram ───────────────────────────────────────
        self.ax_bif = self.fig.add_axes([0.04, 0.28, 0.28, 0.62])
        self.ax_bif.set_facecolor('#252526')
        self.ax_bif.tick_params(colors='white')
        self.ax_bif.set_title("Bifurcation (G vs Km)", color='white', fontsize=10)
        self.ax_bif.set_xlabel("Km", color='white')
        self.ax_bif.set_ylabel("[G]", color='white')

        # ── Center: Phase Portrait ──────────────────────────────────────────
        self.ax_phase = self.fig.add_axes([0.37, 0.28, 0.28, 0.62])
        self.ax_phase.set_facecolor('#252526')
        self.ax_phase.tick_params(colors='white')
        self.ax_phase.set_title("Phase Portrait", color='white', fontsize=10)
        self.ax_phase.set_xlabel("[G]", color='white')
        self.ax_phase.set_ylabel("[ATP]", color='white')

        # ── Right: Oscillograph ─────────────────────────────────────────────
        self.ax_osc = self.fig.add_axes([0.70, 0.28, 0.28, 0.62])
        self.ax_osc.set_facecolor('#252526')
        self.ax_osc.tick_params(colors='white')
        self.ax_osc.set_title("Time Series", color='white', fontsize=10)
        self.ax_osc.set_xlabel("t", color='white')
        self.ax_osc.set_ylabel("Concentration", color='white')

        # ── Slider ──────────────────────────────────────────────────────────
        axcolor = '#3e3e42'
        self.ax_km = self.fig.add_axes([0.1, 0.08, 0.8, 0.03], facecolor=axcolor)
        self.s_km = Slider(self.ax_km, 'Km', 10.0, 25.0, valinit=13.0)
        self.s_km.label.set_color('white')
        self.s_km.valtext.set_color('white')

        # ── Bifurcation diagram (static background) ─────────────────────────
        km_vals = np.linspace(10, 25, 100)
        fp_G, max_G, min_G = [], [], []
        for k in km_vals:
            fp = _fp(k)
            fp_G.append(fp[0])
            t = np.linspace(0, 2000, 4000)
            sol = odeint(_rhs, [fp[0]+0.1, fp[1]+0.1], t, args=(k,))
            steady = sol[2000:]
            max_G.append(np.max(steady[:, 0]))
            min_G.append(np.min(steady[:, 0]))

        self.ax_bif.fill_between(km_vals, min_G, max_G, color='#ffff00', label='Oscillations')
        self.ax_bif.plot(km_vals, fp_G, '#00aa00', lw=2, label='[G] fixed')
        self.ax_bif.plot(km_vals, max_G, '#2196F3', lw=1.5, label='[G] max')
        self.ax_bif.plot(km_vals, min_G, '#FF9800', lw=1.5, label='[G] min')
        self.vline = self.ax_bif.axvline(13.0, color='white', lw=1, ls='--')
        self.student_fp, = self.ax_bif.plot([], [], 'co', markersize=8, label='Your fixed point')
        self.ax_bif.legend(facecolor='#252526', edgecolor='white', labelcolor='white', fontsize=7, loc='upper right')

        # ── Phase portrait elements (redrawn on slider change) ──────────────
        self.phase_nullcline_G, = self.ax_phase.plot([], [], 'c-', lw=2, label='dG/dt=0')
        self.phase_nullcline_ATP, = self.ax_phase.plot([], [], 'm-', lw=2, label='dATP/dt=0')
        self.phase_traj, = self.ax_phase.plot([], [], 'w-', lw=1.2, alpha=0.9)
        self.phase_fp, = self.ax_phase.plot([], [], 'yo', markersize=8)
        self.quiver = None
        self.ax_phase.legend(facecolor='#252526', edgecolor='white', labelcolor='white', fontsize=7)

        # ── Oscillograph elements ───────────────────────────────────────────
        self.osc_G, = self.ax_osc.plot([], [], 'c-', lw=1.5, label='[G]')
        self.osc_ATP, = self.ax_osc.plot([], [], 'm-', lw=1.5, label='[ATP]')
        self.ax_osc.legend(facecolor='#252526', edgecolor='white', labelcolor='white', fontsize=7)

        self.s_km.on_changed(self.update)
        self.update(13.0)

    def update(self, val):
        Km = self.s_km.val if val is None else val
        self.vline.set_xdata([Km, Km])

        # ── Student fixed point ─────────────────────────────────────────────
        try:
            res = implementation_tasks.glycolysis_fixed_point(Km)
            if res is not None and len(res) == 2:
                self.student_fp.set_data([Km], [res[0]])
        except Exception as e:
            self.dashboard.log(f"Error in glycolysis_fixed_point: {e}", color="#f44747")
            self.student_fp.set_data([], [])

        # ── Integrate trajectory ────────────────────────────────────────────
        fp = _fp(Km)
        t_span = np.linspace(0, 800, 4000)
        sol = odeint(_rhs, [fp[0]+0.5, fp[1]+0.5], t_span, args=(Km,))

        # ── Phase portrait ──────────────────────────────────────────────────
        G_max = max(np.max(sol[:, 0]) * 1.3, 5)
        ATP_max = max(np.max(sol[:, 1]) * 1.3, 2)

        # G-nullcline: dG/dt=0 → ATP = Vin/(k1*G)
        G_nc = np.linspace(0.1, G_max, 200)
        ATP_nc_G = VIN / (K1 * G_nc)
        self.phase_nullcline_G.set_data(G_nc, ATP_nc_G)

        # ATP-nullcline: dATP/dt=0 → 2*k1*G*ATP = kp*ATP/(ATP+Km) → G = kp/(2*k1*(ATP+Km))
        ATP_nc = np.linspace(0.01, ATP_max, 200)
        G_nc_ATP = KP / (2 * K1 * (ATP_nc + Km))
        self.phase_nullcline_ATP.set_data(G_nc_ATP, ATP_nc)

        # Vector field
        if self.quiver is not None:
            self.quiver.remove()
        Gg, Ag = np.meshgrid(np.linspace(0.1, G_max, 12), np.linspace(0.1, ATP_max, 10))
        dG = VIN - K1 * Gg * Ag
        dA = 2 * K1 * Gg * Ag - KP * Ag / (Ag + Km)
        speed = np.sqrt(dG**2 + dA**2) + 1e-10
        self.quiver = self.ax_phase.quiver(Gg, Ag, dG/speed, dA/speed, color='gray', alpha=0.35, scale=25)

        # Trajectory and fixed point
        self.phase_traj.set_data(sol[:, 0], sol[:, 1])
        self.phase_fp.set_data([fp[0]], [fp[1]])
        self.ax_phase.set_xlim(0, G_max)
        self.ax_phase.set_ylim(0, ATP_max)

        # ── Oscillograph ────────────────────────────────────────────────────
        t_show = t_span[-2000:]
        sol_show = sol[-2000:]
        self.osc_G.set_data(t_show, sol_show[:, 0])
        self.osc_ATP.set_data(t_show, sol_show[:, 1])
        self.ax_osc.set_xlim(t_show[0], t_show[-1])
        self.ax_osc.set_ylim(0, max(np.max(sol_show) * 1.1, 1))

        self.fig.canvas.draw_idle()
