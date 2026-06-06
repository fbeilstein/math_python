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
    import implementation_tasks
    c, bound_x, bound_y, S_true, Bx, By = implementation_tasks.calculate_mathematical_bounds(H, W, cx, cy, w, h)
    
    m = c if c > 1.01 else 2.0
    alpha = np.log(m) / (2 * np.pi)
    r_0 = (h / 2.0) / S_true
    exact_rotation = -alpha * np.log(r_0)
    C = 1.0 + 1j * alpha
    
    y_grid, x_grid = np.meshgrid(np.arange(H), np.arange(W), indexing='ij')
    Z = (x_grid - cx) / S_true + 1j * (y_grid - cy) / S_true
    Z = np.where(Z == 0, 1e-8 + 1j*1e-8, Z)
    
    try:
        Z_new = implementation_tasks.backward_step_2_log_polar(Z)
        Z = Z_new if Z_new is not None else Z
        
        Z_new = implementation_tasks.backward_step_3_conformal_twist(Z, C)
        Z = Z_new if Z_new is not None else Z
        
        Z_new = implementation_tasks.backward_step_4_exponentiation(Z)
        Z = Z_new if Z_new is not None else Z
        
        Z_new = implementation_tasks.backward_step_5_droste_fold(Z, m, exact_rotation, Bx, By)
        Z = Z_new if Z_new is not None else Z
    except Exception:
        pass
        
    src_x, src_y = implementation_tasks.denormalize(Z, cx, cy, S_true)
    
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
    
    try:
        if cv2.getWindowProperty("Droste", cv2.WND_PROP_VISIBLE) < 1:
            break
    except Exception:
        break
    if key == 27:  # ESC to quit
        break
    elif key == ord('s') or key == 32:  # 's' or spacebar to start timer
        if capture_start_time is None:
            capture_start_time = time.time()

cap.release()
cv2.destroyAllWindows()