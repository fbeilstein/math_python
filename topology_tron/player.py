import pygame

class Player:
    def __init__(self, color, start_x, start_y, default_dx, default_dy, cell_size):
        self.color = color
        self.x = start_x
        self.y = start_y
        
        # Next direction to move (updated by input)
        self.next_dx = default_dx
        self.next_dy = default_dy
        
        # Current direction (used for moving)
        self.dx = default_dx
        self.dy = default_dy
        
        self.cell_size = cell_size
        self.trace = set()
        self.trace.add((self.x, self.y))
        
        self.alive = True
        self.boost = False

    def update_direction(self, new_dx, new_dy):
        # Prevent 180-degree turns
        if (self.dx != -new_dx or new_dx == 0) and (self.dy != -new_dy or new_dy == 0):
            self.next_dx = new_dx
            self.next_dy = new_dy

    def move(self, new_x, new_y, new_dx, new_dy):
        self.x = new_x
        self.y = new_y
        self.dx = new_dx
        self.dy = new_dy
        self.trace.add((self.x, self.y))

    def draw(self, surface):
        for tx, ty in self.trace:
            rect = pygame.Rect(tx * self.cell_size, ty * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(surface, self.color, rect)
        
        # Draw head slightly brighter
        head_rect = pygame.Rect(self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size)
        bright_color = (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50))
        pygame.draw.rect(surface, bright_color, head_rect)
