import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import implementation_tasks

class Level2Inhibition:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.fig = plt.figure()
        self.fig.patch.set_facecolor('#1e1e1e')
        
        self.ax1 = self.fig.add_axes([0.1, 0.5, 0.35, 0.4])
        self.ax2 = self.fig.add_axes([0.55, 0.5, 0.35, 0.4])
        
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#252526')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
        
        self.ax1.set_title("Michaelis-Menten Plot")
        self.ax2.set_title("Lineweaver-Burk Plot")
        
        axcolor = '#3e3e42'
        self.ax_i = self.fig.add_axes([0.1, 0.25, 0.8, 0.03], facecolor=axcolor)
        self.ax_radio = self.fig.add_axes([0.1, 0.05, 0.3, 0.15], facecolor=axcolor)
        
        self.s_i = Slider(self.ax_i, 'True [I]', 0.0, 10.0, valinit=5.0)
        self.s_i.label.set_color('white')
        self.s_i.valtext.set_color('white')
        
        orig_draw = self.ax_radio.draw_artist
        self.ax_radio.draw_artist = lambda *args, **kwargs: None
        self.radio = RadioButtons(self.ax_radio, ('competitive', 'uncompetitive', 'noncompetitive'), active=0)
        self.ax_radio.draw_artist = orig_draw
        for t in self.radio.labels:
            t.set_color('white')
            
        self.s_i.on_changed(self.update)
        self.radio.on_clicked(self.update)
        
        self.result_text = self.fig.text(0.5, 0.4, "", color='#00ff00', fontsize=14, ha='center')
        
        self.update(None)

    def update(self, _):
        true_I = self.s_i.val
        inh_type = self.radio.value_selected
        
        true_Km = 2.0
        true_Vmax = 10.0
        Ki = 3.0
        
        # Generate data
        S_array = np.linspace(0.5, 20, 15)
        V_no_inh = (true_Vmax * S_array) / (true_Km + S_array)
        
        if inh_type == 'competitive':
            app_Km = true_Km * (1 + true_I / Ki)
            app_Vmax = true_Vmax
        elif inh_type == 'uncompetitive':
            app_Km = true_Km / (1 + true_I / Ki)
            app_Vmax = true_Vmax / (1 + true_I / Ki)
        else: # noncompetitive
            app_Km = true_Km
            app_Vmax = true_Vmax / (1 + true_I / Ki)
            
        V_with_inh = (app_Vmax * S_array) / (app_Km + S_array)
        
        # Use clean data because Lineweaver-Burk is extremely sensitive to noise
        # and student's strict tolerance (1e-3) will fail otherwise.
        V_no_inh_noisy = V_no_inh
        V_with_inh_noisy = V_with_inh
        
        self.ax1.clear()
        self.ax2.clear()
        
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#252526')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
        self.ax1.set_title("Michaelis-Menten Plot")
        self.ax2.set_title("Lineweaver-Burk Plot")
        
        # Plot raw data
        self.ax1.plot(S_array, V_no_inh_noisy, 'wo', label='No Inh Data')
        self.ax1.plot(S_array, V_with_inh_noisy, 'ro', label='+ Inh Data')
        self.ax2.plot(1/S_array, 1/V_no_inh_noisy, 'wo', label='No Inh Data')
        self.ax2.plot(1/S_array, 1/V_with_inh_noisy, 'ro', label='+ Inh Data')
        
        try:
            res = implementation_tasks.analyze_inhibition(S_array, V_no_inh_noisy, V_with_inh_noisy, true_I)
            if res is not None:
                calc_Km, calc_Vmax, calc_type, calc_Ki = res
                
                # Reconstruct fits
                S_smooth = np.linspace(0, 25, 100)
                v_no_fit = (calc_Vmax * S_smooth) / (calc_Km + S_smooth)
                
                if calc_type == 'competitive':
                    cKm = calc_Km * (1 + true_I/calc_Ki)
                    cVmax = calc_Vmax
                elif calc_type == 'uncompetitive':
                    cKm = calc_Km / (1 + true_I/calc_Ki)
                    cVmax = calc_Vmax / (1 + true_I/calc_Ki)
                else:
                    cKm = calc_Km
                    cVmax = calc_Vmax / (1 + true_I/calc_Ki)
                    
                v_with_fit = (cVmax * S_smooth) / (cKm + S_smooth)
                
                self.ax1.plot(S_smooth, v_no_fit, 'w--')
                self.ax1.plot(S_smooth, v_with_fit, 'r--')
                
                # Lineweaver-Burk exact lines (including negative intercept)
                X_plot = np.linspace(-0.6, 2.5, 100)
                self.ax2.plot(X_plot, (calc_Km/calc_Vmax)*X_plot + 1.0/calc_Vmax, 'w--')
                self.ax2.plot(X_plot, (cKm/cVmax)*X_plot + 1.0/cVmax, 'r--')
                self.ax2.set_xlim(-0.6, 2.5)
                
                self.dashboard.log(f"Student predicted type: {calc_type}, Ki = {calc_Ki:.2f}")
                self.result_text.set_text(f"Your Ki = {calc_Ki:.2f}  (true Ki = {Ki:.2f})")
        except Exception as e:
            self.dashboard.log(f"Error in analyze_inhibition: {e}", color="#f44747")
            self.result_text.set_text("")
            
        self.ax1.legend(facecolor='#252526', edgecolor='white', labelcolor='white')
        self.fig.canvas.draw_idle()
