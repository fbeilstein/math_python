import numpy as np
import matplotlib.pyplot as plt

class BaseLevel:
    """
    Shared base for all wave-packet level visual debuggers.

    Subclasses must implement:
        draw(self) -> None
            Clears and redraws the axes from scratch.
    """

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(9, 4))
        self.fig.patch.set_facecolor('#1a1a2e')
        self.ax.set_facecolor('#16213e')
        self.sliders = {}    # populated by subclass
        self.cids    = []

    # ------------------------------------------------------------------
    # Axis styling helpers
    # ------------------------------------------------------------------
    def style_axes(self, xlabel='x', ylabel=''):
        self.ax.set_facecolor('#16213e')
        self.ax.tick_params(colors='#cccccc')
        self.ax.xaxis.label.set_color('#cccccc')
        self.ax.yaxis.label.set_color('#cccccc')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#444466')
        self.ax.set_xlabel(xlabel, fontsize=10)
        if ylabel:
            self.ax.set_ylabel(ylabel, fontsize=10)
        self.ax.grid(True, color='#2a2a4a', linestyle='--', alpha=0.6)

    # ------------------------------------------------------------------
    # Redraw helper called by slider callbacks
    # ------------------------------------------------------------------
    def _on_slider_change(self, val):
        self.ax.clear()
        self.draw()
        self.fig.canvas.draw_idle()

    # ------------------------------------------------------------------
    # Standard redraw loop
    # ------------------------------------------------------------------
    def draw(self):
        raise NotImplementedError("Subclasses must implement draw()")
