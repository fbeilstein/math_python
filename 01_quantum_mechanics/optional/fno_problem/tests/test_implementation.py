import pytest
import torch
import sys
import os

# Add parent directory to path to import implementation_tasks
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import implementation_tasks as tasks

def test_spectral_conv1d():
    batch = 4
    in_channels = 3
    out_channels = 5
    N_x = 256
    modes = 16

    conv = tasks.SpectralConv1d(in_channels, out_channels, modes)
    x = torch.randn(batch, in_channels, N_x, requires_grad=True)
    
    out = conv(x)
    assert out.shape == (batch, out_channels, N_x), f"Expected shape {(batch, out_channels, N_x)}, got {out.shape}"
    
    # Test differentiability
    loss = out.sum()
    loss.backward()
    assert x.grad is not None, "Input gradient is None (not differentiable)"
    assert conv.weights.grad is not None, "Weights gradient is None (parameters not updating)"

def test_generate_temporal_features():
    batch = 8
    N_x = 128
    t = torch.rand(batch, 1)
    
    out = tasks.generate_temporal_features(t, N_x)
    assert out.shape == (batch, N_x, 10), f"Expected shape {(batch, N_x, 10)}, got {out.shape}"

def test_fno1d():
    batch = 2
    N_x = 256
    
    model = tasks.FNO1d(modes=16, width=32)
    # The forward pass of FNO1d expects: V, x_coord, t, psi0_re, psi0_im
    V = torch.randn(batch, N_x, 1)
    x_coord = torch.randn(batch, N_x, 1)
    t = torch.rand(batch, 1)
    psi0_re = torch.randn(batch, N_x, 1)
    psi0_im = torch.randn(batch, N_x, 1)
    
    out = model(V, x_coord, t, psi0_re, psi0_im)
    assert out.shape == (batch, N_x, 3), f"Expected output shape {(batch, N_x, 3)}, got {out.shape}"
