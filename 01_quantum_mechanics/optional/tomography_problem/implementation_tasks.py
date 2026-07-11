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

def pt_split_operator_step(psi, k_sq, V, dt):
    """
    One Trotter split-operator step in PyTorch (differentiable).

    Same physics as np_split_operator_step, but using torch operations
    so that autograd can backpropagate through it.

    Args:
        psi:   (N,) complex tensor — wavefunction
        k_sq:  (N,) float tensor  — k^2 values (squared momentum grid)
        V:     (N,) float tensor  — potential
        dt:    float              — time step

    Returns:
        (N,) complex tensor — evolved wavefunction
    """
    pass


class GridPotential(nn.Module):
    """
    Learnable potential V(x) represented as a smoothed grid.

    The raw parameter V_raw is convolved with a small Gaussian kernel
    to prevent unphysical high-frequency ringing.

    Args:
        n_points: int — number of spatial grid points
    """
    def __init__(self, n_points):
        super().__init__()
        # Hint: create nn.Parameter for V_raw, build a fixed Gaussian
        # smoothing kernel and register it as a buffer.
        pass

    def forward(self):
        """Return the smoothed potential as a 1D tensor of shape (n_points,)."""
        pass


def run_teacher_forcing(V_pred, psi_observations, psi0, k_sq, dt):
    """
    Compute the teacher-forcing loss over sparse observations.

    For each pair of consecutive snapshots (psi_i, psi_{i+1}):
      1. Start from the TRUE state psi_i (teacher forcing)
      2. Propagate forward using pt_split_operator_step with V_pred
      3. Accumulate MSE loss against psi_{i+1}

    Args:
        V_pred:            (N,) tensor — current potential estimate
        psi_observations:  list of (step_idx, psi_tensor) tuples
        psi0:              (N,) complex tensor — initial wavefunction
        k_sq:              (N,) float tensor — k^2 grid
        dt:                float — time step

    Returns:
        scalar tensor — total loss
    """
    pass


# =============================================================================
#  SELF-TESTING
# =============================================================================
if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
