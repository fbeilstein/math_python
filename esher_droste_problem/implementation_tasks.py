import numpy as np

def calculate_mathematical_bounds(H, W, cx, cy, w, h): #contains solution
    """L0: Calculates the outer fundamental domain boundaries (Green Rectangle) and scaling factors."""
    max_w_half = min(cx, W - cx)
    max_h_half = min(cy, H - cy)
    c_x = max_w_half / (w / 2.0) if w > 0 else 1
    c_y = max_h_half / (h / 2.0) if h > 0 else 1
    c = min(c_x, c_y)
    
    bound_x = c * (w / 2.0)
    bound_y = c * (h / 2.0)
    S_true = max(bound_x, bound_y)
    Bx = bound_x / S_true
    By = bound_y / S_true
    
    return c, bound_x, bound_y, S_true, Bx, By


def denormalize(Z_src, cx, cy, S_true): #contains solution
    src_x = (np.real(Z_src) * S_true + cx).astype(np.float32)
    src_y = (np.imag(Z_src) * S_true + cy).astype(np.float32)
    return src_x, src_y

def backward_step_1_normalize(H, W, S_disp): #contains solution
    y_grid, x_grid = np.meshgrid(np.arange(H), np.arange(W), indexing='ij')
    X = (x_grid - W/2.0) / S_disp
    Y = (y_grid - H/2.0) / S_disp
    Z_out = X + 1j * Y
    Z_out = np.where(Z_out == 0, 1e-8 + 1j*1e-8, Z_out)
    return Z_out

def backward_step_2_log_polar(W_out): #contains solution
    return np.exp(W_out)

def backward_step_3_conformal_twist(W_straight, C): #contains solution
    return W_straight * C

def backward_step_4_exponentiation(Z_out): #contains solution
    return np.log(Z_out)

def backward_step_5_droste_fold(Z_spiral, m, exact_rotation, Bx, By): #contains solution
    Z = Z_spiral * np.exp(1j * exact_rotation)
    X_map = np.real(Z)
    Y_map = np.imag(Z)
    R_rect = np.maximum(np.abs(X_map) / Bx, np.abs(Y_map) / By)
    R_rect = np.where(R_rect == 0, 1e-8, R_rect)
    k = np.ceil(np.log(R_rect) / np.log(m))
    return Z * (m ** -k)
