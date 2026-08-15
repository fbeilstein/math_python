import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import implementation_tasks


def _calc_ph(pka, ca, cb, v, ct, isa):
    na, nb = ca, cb
    nt = v * ct
    if isa:
        na += nt
        nb -= nt
    else:
        na -= nt
        nb += nt
    if nb <= 0: return -np.log10(-nb/(1+v)) if nb!=0 else 7.0
    if na <= 0: return 14.0 + np.log10(-na/(1+v)) if na!=0 else 7.0
    return pka + np.log10(nb/na)
        
class Level1Titration:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.fig = plt.figure()
        self.fig.patch.set_facecolor('#1e1e1e')
        
        self.ax = self.fig.add_axes([0.1, 0.4, 0.8, 0.5])
        self.ax.set_facecolor('#252526')
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.set_title("pH Titration Curve", color="white")
        
        # Controls
        axcolor = '#3e3e42'
        self.ax_pka = self.fig.add_axes([0.1, 0.25, 0.3, 0.03], facecolor=axcolor)
        self.ax_c_acid = self.fig.add_axes([0.1, 0.2, 0.3, 0.03], facecolor=axcolor)
        self.ax_c_base = self.fig.add_axes([0.1, 0.15, 0.3, 0.03], facecolor=axcolor)
        self.ax_vol = self.fig.add_axes([0.1, 0.1, 0.8, 0.03], facecolor=axcolor)
        self.ax_radio = self.fig.add_axes([0.5, 0.15, 0.15, 0.1], facecolor=axcolor)
        
        self.s_pka = Slider(self.ax_pka, 'pKa', 1.0, 10.0, valinit=4.76)
        self.s_c_acid = Slider(self.ax_c_acid, 'C_acid', 0.0, 1.0, valinit=0.1)
        self.s_c_base = Slider(self.ax_c_base, 'C_base', 0.0, 1.0, valinit=0.1)
        self.s_vol = Slider(self.ax_vol, 'Titrant Vol', 0.0, 2.0, valinit=0.0)
        
        orig_draw = self.ax_radio.draw_artist
        self.ax_radio.draw_artist = lambda *args, **kwargs: None
        self.radio = RadioButtons(self.ax_radio, ('Add Strong Acid', 'Add Strong Base'), active=1)
        self.ax_radio.draw_artist = orig_draw
        
        for w in [self.s_pka, self.s_c_acid, self.s_c_base, self.s_vol]:
            w.label.set_color('white')
            w.valtext.set_color('white')
        for t in self.radio.labels:
            t.set_color('white')
            
        self.s_pka.on_changed(self.update)
        self.s_c_acid.on_changed(self.update)
        self.s_c_base.on_changed(self.update)
        self.s_vol.on_changed(self.update)
        self.radio.on_clicked(self.update)
        
        self.line_theory, = self.ax.plot([], [], 'w--', label='Theoretical Curve')
        self.point_student, = self.ax.plot([], [], 'ro', markersize=10, label='Your calculate_pH()')
        self.ax.set_xlim(0, 2)
        self.ax.set_ylim(0, 14)
        self.ax.legend(facecolor='#252526', edgecolor='white', labelcolor='white')
        
        self.update(None)

    def update(self, _):
        pka = self.s_pka.val
        c_acid = self.s_c_acid.val
        c_base = self.s_c_base.val
        vol = self.s_vol.val
        is_acid = (self.radio.value_selected == 'Add Strong Acid')
        c_titrant = 0.1
        
        vols = np.linspace(0, 2, 200)
        phs = []
        for v in vols:
            phs.append(_calc_ph(pka, c_acid, c_base, v, c_titrant, is_acid))
        
        self.line_theory.set_data(vols, phs)
        
        try:
            student_ph = implementation_tasks.calculate_pH(pka, c_acid, c_base, vol, c_titrant, is_acid)
            if student_ph is None:
                self.point_student.set_data([], [])
            else:
                self.point_student.set_data([vol], [student_ph])
        except Exception as e:
            self.dashboard.log(f"Error in calculate_pH: {e}", color="#f44747")
            self.point_student.set_data([], [])
            
        self.fig.canvas.draw_idle()
