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
    Level 1: Spectral convolution layer operating in Fourier space.

    Operations:
        1. FFT the input along the spatial dimension
        2. Multiply the first k_max modes by learnable complex weights R
        3. Zero-pad the remaining modes
        4. IFFT back to physical space
    """
    def __init__(self, in_channels, out_channels, modes): #contains solution
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.modes = modes
        
        # Learnable complex weights for the Fourier modes
        self.weights = nn.Parameter(
            torch.empty(in_channels, out_channels, modes, dtype=torch.cfloat)
        )
        # Proper initialization for complex parameters
        nn.init.xavier_normal_(self.weights.real, gain=1/(in_channels*out_channels))
        nn.init.xavier_normal_(self.weights.imag, gain=1/(in_channels*out_channels))

    def forward(self, x): #contains solution
        """
        Args:
            x: (batch, channels, N_x)
        Returns:
            (batch, out_channels, N_x)
        """
        batch_size = x.shape[0]
        N_x = x.shape[-1]
        
        # 1. FFT
        x_ft = torch.fft.rfft(x)
        
        # 2. Multiply modes
        # Output tensor in Fourier space, initialized to zero
        out_ft = torch.zeros(batch_size, self.out_channels, x_ft.shape[-1], 
                             dtype=torch.cfloat, device=x.device)
                             
        # Einsum: b=batch, i=in_channels, o=out_channels, x=spatial
        out_ft[:, :, :self.modes] = torch.einsum(
            "bix,iox->box", 
            x_ft[:, :, :self.modes], 
            self.weights
        )
        
        # 3. IFFT back to physical space
        x_out = torch.fft.irfft(out_ft, n=N_x)
        return x_out


class MiniFNO(nn.Module):
    """
    Level 2: Minimal Fourier Neural Operator for 1D quantum dynamics.

    Architecture:
        Lifting:    Linear(3, width)  — input: [V(x), Re(ψ₀), Im(ψ₀)]
        2× layers:  SpectralConv1d(width, width, modes) + Conv1d(width, width, 1) + GeLU
        Projection: Linear(width, 2)  — output: [Re(ψ), Im(ψ)]
    """
    def __init__(self, modes=32, width=32): #contains solution
        super().__init__()
        
        self.modes = modes
        self.width = width
        
        # Lifting layer (applied point-wise)
        self.fc0 = nn.Linear(3, self.width)
        
        # First spectral block
        self.conv0 = SpectralConv1d(self.width, self.width, self.modes)
        self.w0 = nn.Conv1d(self.width, self.width, 1)
        
        # Second spectral block
        self.conv1 = SpectralConv1d(self.width, self.width, self.modes)
        self.w1 = nn.Conv1d(self.width, self.width, 1)
        
        # Projection layer
        self.fc1 = nn.Linear(self.width, 128)
        self.fc2 = nn.Linear(128, 2)

    def forward(self, V, psi0, t): #contains solution
        """
        Returns: (batch, N_x, 2) — [Re(ψ), Im(ψ)] at time t
        """
        # Note: t is currently ignored in this mini version for simplicity,
        # it just learns the mapping for the specific dataset timestep distribution.
        
        # Stack inputs into (batch, N_x, 3)
        x = torch.stack([V, psi0.real, psi0.imag], dim=-1)
        
        # Lifting: (batch, N_x, width)
        x = self.fc0(x)
        
        # Permute to (batch, channels, N_x) for convolutions
        x = x.permute(0, 2, 1)
        
        # Layer 1
        x1 = self.conv0(x)
        x2 = self.w0(x)
        x = torch.nn.functional.gelu(x1 + x2)
        
        # Layer 2
        x1 = self.conv1(x)
        x2 = self.w1(x)
        x = torch.nn.functional.gelu(x1 + x2)
        
        # Permute back to (batch, N_x, channels)
        x = x.permute(0, 2, 1)
        
        # Projection
        x = self.fc1(x)
        x = torch.nn.functional.gelu(x)
        x = self.fc2(x)
        
        return x


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
