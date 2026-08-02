import pygame
import sys
from implementation_tasks import apply_topology
from player import Player

# Constants
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 10
GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE
WINDOW_SCALE = 2  # Scale up for modern screens

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (50, 50, 50)

TOPOLOGIES = [
    "Square",
    "Cylinder",
    "Möbius",
    "Torus",
    "Klein Bottle",
    "Real Projective Plane"
]

class Game:
    def __init__(self):
        pygame.init()
        # Create a window scaled up by WINDOW_SCALE
        self.display_surface = pygame.display.set_mode((WIDTH * WINDOW_SCALE, HEIGHT * WINDOW_SCALE))
        # Internal rendering surface at the exact 640x480 resolution
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        pygame.display.set_caption("Topology Tron")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        
        self.state = "MENU"
        self.selected_top_idx = 0
        
        self.p1 = None
        self.p2 = None
        self.topology = None
        
        # Accumulators for movement timing
        self.p1_acc = 0
        self.p2_acc = 0
        self.tick_threshold = 3 # 60fps / 3 = 20 moves per second base speed

    def init_game(self):
        self.topology = TOPOLOGIES[self.selected_top_idx]
        self.p1 = Player(GREEN, GRID_W // 3, GRID_H // 2, 1, 0, CELL_SIZE)
        self.p2 = Player(RED, 2 * GRID_W // 3, GRID_H // 2, -1, 0, CELL_SIZE)
        self.p1_acc = 0
        self.p2_acc = 0
        self.state = "WAIT_START"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_UP:
                        self.selected_top_idx = (self.selected_top_idx - 1) % len(TOPOLOGIES)
                    elif event.key == pygame.K_DOWN:
                        self.selected_top_idx = (self.selected_top_idx + 1) % len(TOPOLOGIES)
                    elif event.key == pygame.K_RETURN:
                        self.init_game()
                        
                elif self.state == "WAIT_START":
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, 
                                     pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        # Apply the first keypress to direction
                        self.handle_game_keys(event.key)
                        self.state = "PLAYING"
                        
                elif self.state == "PLAYING":
                    self.handle_game_keys(event.key)
                    
                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_RETURN:
                        self.state = "MENU"

    def handle_game_keys(self, key):
        if key == pygame.K_w: self.p1.update_direction(0, -1)
        if key == pygame.K_s: self.p1.update_direction(0, 1)
        if key == pygame.K_a: self.p1.update_direction(-1, 0)
        if key == pygame.K_d: self.p1.update_direction(1, 0)
        
        if key == pygame.K_UP: self.p2.update_direction(0, -1)
        if key == pygame.K_DOWN: self.p2.update_direction(0, 1)
        if key == pygame.K_LEFT: self.p2.update_direction(-1, 0)
        if key == pygame.K_RIGHT: self.p2.update_direction(1, 0)

    def check_boost(self):
        keys = pygame.key.get_pressed()
        self.p1.boost = keys[pygame.K_LSHIFT]
        self.p2.boost = keys[pygame.K_RSHIFT]

    def update(self):
        if self.state != "PLAYING":
            return
            
        self.check_boost()
        
        self.p1_acc += 2 if self.p1.boost else 1
        self.p2_acc += 2 if self.p2.boost else 1
        
        p1_moved = self.p1_acc >= self.tick_threshold
        p2_moved = self.p2_acc >= self.tick_threshold
        
        if not p1_moved and not p2_moved:
            return

        # Calculate intended next positions
        res1 = self.get_next_pos(self.p1) if p1_moved else None
        res2 = self.get_next_pos(self.p2) if p2_moved else None
        
        p1_nx = res1[0] if res1 else self.p1.x
        p1_ny = res1[1] if res1 else self.p1.y
        p2_nx = res2[0] if res2 else self.p2.x
        p2_ny = res2[1] if res2 else self.p2.y

        # Check wall collisions
        if p1_moved and res1 is None:
            self.p1.alive = False
        if p2_moved and res2 is None:
            self.p2.alive = False

        # Did they hit head-to-head or cross over?
        if p1_moved and p2_moved and res1 and res2:
            head_to_head = (p1_nx == p2_nx and p1_ny == p2_ny)
            crossed = ((p1_nx, p1_ny) == (self.p2.x, self.p2.y) and 
                       (p2_nx, p2_ny) == (self.p1.x, self.p1.y))
            if head_to_head or crossed:
                self.p1.alive = False
                self.p2.alive = False

        # Check trace collisions
        if p1_moved and self.p1.alive:
            if (p1_nx, p1_ny) in self.p1.trace or (p1_nx, p1_ny) in self.p2.trace:
                self.p1.alive = False
                
        if p2_moved and self.p2.alive:
            if (p2_nx, p2_ny) in self.p2.trace or (p2_nx, p2_ny) in self.p1.trace:
                self.p2.alive = False

        # Apply movements only if still alive (prevents gigantic overlap)
        if p1_moved:
            self.p1_acc -= self.tick_threshold
            if self.p1.alive and res1:
                self.p1.move(res1[0], res1[1], res1[2], res1[3])
                
        if p2_moved:
            self.p2_acc -= self.tick_threshold
            if self.p2.alive and res2:
                self.p2.move(res2[0], res2[1], res2[2], res2[3])
                
        if not self.p1.alive or not self.p2.alive:
            self.state = "GAME_OVER"

    def get_next_pos(self, p):
        p.dx = p.next_dx
        p.dy = p.next_dy
        return apply_topology(self.topology, p.x, p.y, p.dx, p.dy, GRID_W, GRID_H)

    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == "MENU":
            title = self.font.render("Topology Tron", True, WHITE)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            for i, top in enumerate(TOPOLOGIES):
                color = GREEN if i == self.selected_top_idx else GRAY
                text = self.font.render(top, True, color)
                self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 150 + i * 40))
                
            inst = self.font.render("Press ENTER to start", True, WHITE)
            self.screen.blit(inst, (WIDTH//2 - inst.get_width()//2, 420))
            
        elif self.state in ["WAIT_START", "PLAYING", "GAME_OVER"]:
            self.p1.draw(self.screen)
            self.p2.draw(self.screen)
            
            if self.state == "WAIT_START":
                msg = self.font.render("Press any movement key to START", True, WHITE)
                self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 50))
                top_msg = self.font.render(f"Topology: {self.topology}", True, GRAY)
                self.screen.blit(top_msg, (WIDTH//2 - top_msg.get_width()//2, HEIGHT - 40))
                
            elif self.state == "GAME_OVER":
                if not self.p1.alive and not self.p2.alive:
                    msg = "Draw!"
                elif self.p1.alive:
                    msg = "Green (P1) Wins!"
                else:
                    msg = "Red (P2) Wins!"
                text = self.font.render(msg, True, WHITE)
                self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 20))
                
                inst = self.font.render("Press ENTER for Menu", True, GRAY)
                self.screen.blit(inst, (WIDTH//2 - inst.get_width()//2, HEIGHT//2 + 20))
                
        # Scale the internal rendering surface to the actual window size
        scaled_surface = pygame.transform.scale(self.screen, (WIDTH * WINDOW_SCALE, HEIGHT * WINDOW_SCALE))
        self.display_surface.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
