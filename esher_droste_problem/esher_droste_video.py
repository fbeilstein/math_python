import cv2
import numpy as np
import time

# -----------------------
# ROI (editable rectangle)
# -----------------------
rect = [200, 150, 300, 250]
drag = False
resize = False
offset = (0, 0)

def mouse(event, x, y, flags, param):
    global rect, drag, resize, offset

    rx, ry, rw, rh = rect
    
    # 30x30 area in the bottom right corner for resizing
    is_resize_area = (rx + rw - 30 <= x <= rx + rw + 30) and (ry + rh - 30 <= y <= ry + rh + 30)
    inside = rx <= x <= rx+rw and ry <= y <= ry+rh

    if event == cv2.EVENT_LBUTTONDOWN:
        if is_resize_area:
            resize = True
        elif inside:
            drag = True
            offset = (x - rx, y - ry)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drag:
            rect[0] = x - offset[0]
            rect[1] = y - offset[1]
        elif resize:
            rect[2] = max(30, x - rect[0])
            rect[3] = max(30, y - rect[1])

    elif event == cv2.EVENT_LBUTTONUP:
        drag = False
        resize = False


# -----------------------
# DROSTE FIELD (Escher Conformal Crop)
# -----------------------
def droste_field(frame, rect):
    H, W = frame.shape[:2]
    x0, y0, w, h = rect
    
    cx = x0 + w / 2.0
    cy = y0 + h / 2.0
    
    # 1. Calculate the largest symmetric boundary that perfectly matches the phone's aspect ratio
    # AND never exceeds the physical boundaries of the camera feed.
    max_w_half = min(cx, W - cx)
    max_h_half = min(cy, H - cy)
    
    # 'c' is the scale factor from the phone size to the maximum cropped size
    c_x = max_w_half / (w / 2.0) if w > 0 else 1
    c_y = max_h_half / (h / 2.0) if h > 0 else 1
    c = min(c_x, c_y)
    
    # The outer boundary is now exactly proportional to the phone AND strictly inside the camera
    bound_x = c * (w / 2.0)
    bound_y = c * (h / 2.0)
    
    S = max(bound_x, bound_y)
    Bx = bound_x / S
    By = bound_y / S
    
    # Because Bx and By are exactly proportional to the phone, m_x and m_y are identical!
    # This guarantees the nested spiral perfectly fills the phone with no gaps.
    m = c
    if m <= 1.01:
        m = 2.0 # Fallback safety
        
    y_grid, x_grid = np.meshgrid(np.arange(H), np.arange(W), indexing='ij')
    
    nx = (x_grid - cx) / S
    ny = (y_grid - cy) / S
    
    Z = nx + 1j * ny
    Z = np.where(Z == 0, 1e-8 + 1j*1e-8, Z)
    
    # 2. Pure Smooth Escher Conformal Transformation
    alpha = np.log(m) / (2 * np.pi)
    C = 1.0 + 1j * alpha
    
    Z_map = np.exp(C * np.log(Z))
    
    # Exact rotation to keep the inner phone upright
    r_0 = (h / 2.0) / S 
    exact_rotation = -alpha * np.log(r_0)
    Z_map = Z_map * np.exp(1j * exact_rotation)
    
    # 3. ReplicateRegion Fold
    X_map = np.real(Z_map)
    Y_map = np.imag(Z_map)
    
    R_rect = np.maximum(np.abs(X_map) / Bx, np.abs(Y_map) / By)
    R_rect = np.where(R_rect == 0, 1e-8, R_rect)
    
    k = np.ceil(np.log(R_rect) / np.log(m))
    
    Z_folded = Z_map * (m ** -k)
    
    src_x = (np.real(Z_folded) * S + cx).astype(np.float32)
    src_y = (np.imag(Z_folded) * S + cy).astype(np.float32)
    
    # Since we perfectly clamped the boundaries, src_x and src_y will NEVER go out of bounds.
    # BORDER_CONSTANT with black will prove that no out-of-bounds lookups ever happen.
    return cv2.remap(frame, src_x, src_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))


# -----------------------
# MAIN LOOP (split view)
# -----------------------
cap = cv2.VideoCapture(0)
cv2.namedWindow("Droste", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Droste", mouse)

capture_start_time = None
saved_time = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    h, w = frame.shape[:2]

    x, y, rw, rh = rect
    
    # STRICT UI CLAMP
    # Required so that scaling the window doesn't mathematically break the bounds
    x = max(0, min(x, w - 30))
    y = max(0, min(y, h - 30))
    rw = max(30, min(rw, w - x - 1))
    rh = max(30, min(rh, h - y - 1))
    rect = [x, y, rw, rh]

    # LEFT: raw + ROI
    left = frame.copy()
    
    # Calculate crop boundary to show the user what part of the image is used
    cx = x + rw / 2.0
    cy = y + rh / 2.0
    max_w_half = min(cx, w - cx)
    max_h_half = min(cy, h - cy)
    
    c_x = max_w_half / (rw / 2.0) if rw > 0 else 1
    c_y = max_h_half / (rh / 2.0) if rh > 0 else 1
    c = min(c_x, c_y)
    
    crop_x1 = int(cx - c * (rw / 2.0))
    crop_y1 = int(cy - c * (rh / 2.0))
    crop_x2 = int(cx + c * (rw / 2.0))
    crop_y2 = int(cy + c * (rh / 2.0))
    
    # Draw the crop boundary (blue)
    cv2.rectangle(left, (crop_x1, crop_y1), (crop_x2, crop_y2), (255, 0, 0), 1)
    
    # Draw the inner ROI (green)
    cv2.rectangle(left, (x, y), (x+rw, y+rh), (0,255,0), 2)
    
    # Visual indicator for the resize handle
    cv2.circle(left, (x+rw, y+rh), 8, (0,0,255), -1)

    # RIGHT: DROSTE FIELD
    right = droste_field(frame, rect)

    view = np.hstack([left, right])
    
    # Check timer and display countdown or save images
    if capture_start_time is not None:
        elapsed = time.time() - capture_start_time
        remaining = 5 - int(elapsed)
        
        if remaining > 0:
            cv2.putText(view, f"Taking photo in: {remaining}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        else:
            # Save raw frame and the escher rendering
            cv2.imwrite("raw_photo.jpg", frame)
            cv2.imwrite("esher_photo.jpg", right)
            print("Photos saved successfully: raw_photo.jpg, esher_photo.jpg")
            
            # Reset timer and trigger confirmation
            capture_start_time = None
            saved_time = time.time()
            
    if saved_time is not None and (time.time() - saved_time) < 2.0:
        cv2.putText(view, "Saved!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow("Droste", view)

    key = cv2.waitKey(1)
    if key == 27:  # ESC to quit
        break
    elif key == ord('s') or key == 32:  # 's' or spacebar to start timer
        if capture_start_time is None:
            capture_start_time = time.time()

cap.release()
cv2.destroyAllWindows()