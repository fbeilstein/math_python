import numpy as np
from numpy.fft import fft, ifft, fftfreq

# --- Natural units: hbar = m = 1 ---
hbar = 1.0
m    = 1.0

def gaussian_packet(x, x0, sigma, k0):
    """Normalized Gaussian wave packet (NumPy)."""
    psi = (1 / (2 * np.pi * sigma**2))**0.25 * \
          np.exp(-(x - x0)**2 / (4 * sigma**2)) * \
          np.exp(1j * k0 * x)
    dx = x[1] - x[0]
    psi /= np.sqrt(np.sum(np.abs(psi)**2) * dx)
    return psi


def np_split_operator_step(psi, k, V, dt):
    """NumPy split-operator step (reference — from QM Problem 5)."""
    psi = psi * np.exp(-1j * V * dt / (2 * hbar))
    psi_k = fft(psi)
    psi_k = psi_k * np.exp(-1j * hbar * k**2 * dt / (2 * m))
    psi = ifft(psi_k)
    psi = psi * np.exp(-1j * V * dt / (2 * hbar))
    return psi
