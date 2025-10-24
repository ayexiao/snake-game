import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (40, 40, 40)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN])
        self.score = 0
        self.grow_pending = 2  # Start with length 3
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (
            (point == pygame.K_LEFT and self.direction == pygame.K_RIGHT) or
            (point == pygame.K_RIGHT and self.direction == pygame.K_LEFT) or
            (point == pygame.K_UP and self.direction == pygame.K_DOWN) or
            (point == pygame.K_DOWN and self.direction == pygame.K_UP)
        ):
            return
        self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = head
        
        if self.direction == pygame.K_UP:
            y -= 1
        elif self.direction == pygame.K_DOWN:
            y += 1
        elif self.direction == pygame.K_LEFT:
            x -= 1
        elif self.direction == pygame.K_RIGHT:
            x += 1
        
        # Wrap around screen edges
        x = x % GRID_WIDTH
        y = y % GRID_HEIGHT
        
        new_head = (x, y)
        
        # Check for collision with self
        if new_head in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_head)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
        
        return True
    
    def grow(self):
        self.grow_pending += 1
        self.length += 1
        self.score += 10
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # Draw snake body
            color = GREEN if i == 0 else BLUE  # Head is green, body is blue
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRAY, rect, 1)

def draw_score(surface, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(text, (10, 10))

def draw_game_over(surface, score):
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    
    game_over_text = font_large.render("GAME OVER", True, RED)
    score_text = font_small.render(f"Final Score: {score}", True, WHITE)
    restart_text = font_small.render("Press SPACE to restart", True, WHITE)
    
    surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
    surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
    surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 70))

def main():
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize_position()
                        game_over = False
                else:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        snake.turn(event.key)
        
        if not game_over:
            # Move snake
            if not snake.move():
                game_over = True
            
            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.grow()
                food.randomize_position()
                # Ensure food doesn't spawn on snake
                while food.position in snake.positions:
                    food.randomize_position()
        
        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, snake.score)
        
        if game_over:
            draw_game_over(screen, snake.score)
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()