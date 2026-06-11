import cv2
import numpy as np

class SourceManager:
    def __init__(self):
        self.mode = "grid" # "grid", "image", "camera"
        self.cap = None
        self.image = None
        self.grid = self._generate_grid()
        self.image_path = None

    def _generate_grid(self, width=640, height=480, cell_size=40):
        """Generates a mathematical checkerboard with a polar radial overlay for testing."""
        grid = np.zeros((height, width, 3), dtype=np.uint8)
        grid.fill(255) # White background

        # Checkerboard
        for y in range(0, height, cell_size):
            for x in range(0, width, cell_size):
                if (x // cell_size + y // cell_size) % 2 == 0:
                    cv2.rectangle(grid, (x, y), (x + cell_size, y + cell_size), (200, 200, 200), -1)

        return grid

    def set_mode(self, mode, image_path=None):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        self.mode = mode
        if mode == "camera":
            self.cap = cv2.VideoCapture(0)
        elif mode == "image":
            if image_path:
                self.image_path = image_path
                self.image = cv2.imread(self.image_path)
                if self.image is not None:
                    # Resize to standard width 640 while maintaining aspect ratio
                    h, w = self.image.shape[:2]
                    scale = 640 / w
                    self.image = cv2.resize(self.image, (640, int(h * scale)))

    def get_frame(self):
        if self.mode == "grid":
            return self.grid.copy()
        elif self.mode == "image":
            if self.image is not None:
                return self.image.copy()
            return self.grid.copy() # fallback
        elif self.mode == "camera":
            if self.cap is not None:
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.flip(frame, 1) # Mirror
                    return frame
            return self.grid.copy() # fallback
        return self.grid.copy()

    def release(self):
        if self.cap is not None:
            self.cap.release()
