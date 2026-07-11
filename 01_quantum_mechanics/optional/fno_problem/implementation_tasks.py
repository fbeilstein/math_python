import torch
import torch.nn as nn
import numpy as np
from numpy.fft import fft, ifft, fftfreq

# --- Natural units: hbar = m = 1 ---
hbar = 1.0
m    = 1.0

# =============================================================================
#  HELPERS (provided)
# =============================================================================

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


# =============================================================================
#  STUDENT IMPLEMENTATION
# =============================================================================

class SpectralConv1d(nn.Module):
    """
    Spectral convolution layer operating in Fourier space.

    Operations:
        1. FFT the input along the spatial dimension
        2. Multiply the first k_max modes by learnable complex weights R
        3. Zero-pad the remaining modes
        4. IFFT back to physical space

    Args:
        in_channels:  number of input channels
        out_channels: number of output channels
        modes:        number of Fourier modes to keep (k_max)
    """
    def __init__(self, in_channels, out_channels, modes):
        super().__init__()
        self.modes = modes
        # Hint: create nn.Parameter of shape (in_ch, out_ch, modes)
        # with dtype=torch.cfloat. Scale by 1/(in_ch * out_ch).
        pass

    def forward(self, x):
        """
        Args:
            x: (batch, channels, N_x)
        Returns:
            (batch, out_channels, N_x)
        """
        # Hint: torch.fft.rfft, torch.einsum("bix,iox->box", ...), torch.fft.irfft
        pass


class MiniFNO(nn.Module):
    """
    Minimal Fourier Neural Operator for 1D quantum dynamics.

    Architecture:
        Lifting:    Linear(3, width)  — input: [V(x), Re(ψ₀), Im(ψ₀)]
        2× layers:  SpectralConv1d(width, width, modes) + Conv1d(width, width, 1) + GeLU
        Projection: Linear(width, 2)  — output: [Re(ψ), Im(ψ)]

    Forward args:
        V:    (batch, N_x) — potential
        psi0: (batch, N_x) — initial wavefunction (complex)
        t:    (batch, 1)   — target time
    """
    def __init__(self, modes=32, width=32):
        super().__init__()
        pass

    def forward(self, V, psi0, t):
        """
        Returns: (batch, N_x, 2) — [Re(ψ), Im(ψ)] at time t
        """
        pass


# =============================================================================
#  DATA GENERATION (provided)
# =============================================================================

def generate_training_sample(x, dx, dt, n_steps):
    """
    Generate one (V, psi0, t, psi_t) sample using the NumPy solver.

    Returns:
        V_np:    (N,) potential array
        psi0_np: (N,) initial wavefunction (complex)
        t:       float — propagation time
        psi_t:   (N,) wavefunction at time t (complex)
    """
    N = len(x)
    k = 2 * np.pi * fftfreq(N, d=dx)

    # Random Gaussian bump potential
    height = np.random.uniform(-15, 15)
    width = np.random.uniform(0.3, 1.0)
    center = np.random.uniform(-1.0, 1.0)
    V = height * np.exp(-(x - center)**2 / (2 * width**2))

    # Random initial wavepacket
    x0 = np.random.uniform(-5.5, -4.5)
    k0 = np.random.uniform(2.5, 3.5)
    sigma = np.random.uniform(0.4, 0.6)
    psi0 = gaussian_packet(x, x0, sigma, k0)

    # Propagate to random time
    target_step = np.random.randint(10, 60) * 10
    psi = psi0.copy()
    for _ in range(target_step):
        psi = np_split_operator_step(psi, k, V, dt)

    return V, psi0, target_step * dt, psi


# =============================================================================
#  SELF-TESTING
# =============================================================================
if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
