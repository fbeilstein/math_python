import torch
import torch.nn as nn

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
    """
    def __init__(self, in_channels, out_channels, modes):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.modes = modes
        
        # Original FNO initialization (vital for learning high-frequency phase oscillations)
        self.scale = (1 / (in_channels * out_channels))
        self.weights = nn.Parameter(
            self.scale * torch.rand(in_channels, out_channels, self.modes, dtype=torch.cfloat)
        )

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
        out_ft = torch.zeros(batch_size, self.out_channels, x_ft.shape[-1], 
                             dtype=torch.cfloat, device=x.device)
                             
        out_ft[:, :, :self.modes] = torch.einsum(
            "bix,iox->box", 
            x_ft[:, :, :self.modes], 
            self.weights
        )
        
        # 3. IFFT back to physical space
        x_out = torch.fft.irfft(out_ft, n=N_x)
        return x_out


def generate_temporal_features(t, N_x): #contains solution
    """
    Generate 10 temporal Fourier features (PINNs trick).
    
    Args:
        t:   (batch, 1) float tensor — target time
        N_x: int — spatial grid size
        
    Returns:
        (batch, N_x, 10) float tensor — temporal features expanded across the grid
    """
    batch = t.shape[0]
    t_features = []
    freqs = [1.0, 2.0, 4.0, 8.0, 16.0]
    for f in freqs:
        t_features.append(torch.sin(f * t))
        t_features.append(torch.cos(f * t))

    t_feats = torch.cat(t_features, dim=-1)  # (batch, 10)
    t_in = t_feats.unsqueeze(1).expand(batch, N_x, 10)
    return t_in


class FNO1d(nn.Module):
    """
    Full Fourier Neural Operator for 1D quantum dynamics.

    Architecture:
        Lifting:    Linear(14, width)  — input: [V(x), x, t_feats (10), Re(ψ₀), Im(ψ₀)]
        5× layers:  SpectralConv1d(width, width, modes) + Conv1d(width, width, 1) + GeLU
        Projection: Linear(width, 256) -> Linear(256, 3) — output: [Re(ψ), Im(ψ), |ψ|²]
    """
    def __init__(self, modes=128, width=128):
        super().__init__()
        self.modes = modes
        self.width = width
        
        # Input channels: V(x) (1), x (1), t_feats (10), psi0_re (1), psi0_im (1)
        self.fc0 = nn.Linear(14, self.width)

        self.conv0 = SpectralConv1d(self.width, self.width, self.modes)
        self.conv1 = SpectralConv1d(self.width, self.width, self.modes)
        self.conv2 = SpectralConv1d(self.width, self.width, self.modes)
        self.conv3 = SpectralConv1d(self.width, self.width, self.modes)
        self.conv4 = SpectralConv1d(self.width, self.width, self.modes)

        self.w0 = nn.Conv1d(self.width, self.width, 1)
        self.w1 = nn.Conv1d(self.width, self.width, 1)
        self.w2 = nn.Conv1d(self.width, self.width, 1)
        self.w3 = nn.Conv1d(self.width, self.width, 1)
        self.w4 = nn.Conv1d(self.width, self.width, 1)

        self.fc1 = nn.Linear(self.width, 256)
        # Output 3 channels: Re, Im, Envelope
        self.fc2 = nn.Linear(256, 3)

    def forward(self, V_in, x_coord, t, psi0_re, psi0_im): #contains solution
        """
        Args:
            V_in:    (batch, N_x, 1) — normalized potential
            x_coord: (batch, N_x, 1) — spatial coordinates
            t:       (batch, 1)      — target time
            psi0_re: (batch, N_x, 1) — real part of initial wavefunction
            psi0_im: (batch, N_x, 1) — imaginary part of initial wavefunction

        Returns:
            (batch, N_x, 3) — [Re(ψ), Im(ψ), |ψ|²] at time t
        """
        N_x = V_in.shape[1]
        
        # 1. Consciously generate the temporal features (PINNs trick)
        t_in = generate_temporal_features(t, N_x)
        
        # 2. Consciously assemble the 14-channel input grid
        grid = torch.cat([V_in, x_coord, t_in, psi0_re, psi0_im], dim=-1)
        
        # 3. Lift and apply Fourier layers
        x = self.fc0(grid)
        x = x.permute(0, 2, 1)

        x1 = self.conv0(x) + self.w0(x)
        x = torch.nn.functional.gelu(x1)
        x1 = self.conv1(x) + self.w1(x)
        x = torch.nn.functional.gelu(x1)
        x1 = self.conv2(x) + self.w2(x)
        x = torch.nn.functional.gelu(x1)
        x1 = self.conv3(x) + self.w3(x)
        x = torch.nn.functional.gelu(x1)
        x1 = self.conv4(x) + self.w4(x)
        x = torch.nn.functional.gelu(x1)

        x = x.permute(0, 2, 1)
        x = self.fc1(x)
        x = torch.nn.functional.gelu(x)
        x = self.fc2(x)

        return x




# =============================================================================
#  SELF-TESTING
# =============================================================================
if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
