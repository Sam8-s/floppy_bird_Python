import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_RADIUS = 15
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_SPEED = 2
GRAVITY = 0.5
JUMP_STRENGTH = -7
FPS = 60

# Colors
SKY_BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

# Setup Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Python")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# Bird
bird_y = HEIGHT // 2
bird_velocity = 0

# Game State
pipes = []
score = 0
game_running = False
showing_start_menu = True
game_over = False

def reset_game():
    global bird_y, bird_velocity, pipes, score, game_running, game_over
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_running = True
    game_over = False

def show_start_menu():
    screen.fill(SKY_BLUE)
    title = big_font.render("Flappy Bird", True, BLACK)
    start_msg = font.render("Press SPACE to Start", True, BLACK)
    control_msg = font.render("Press ESC to Quit", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(start_msg, (WIDTH // 2 - start_msg.get_width() // 2, HEIGHT // 2))
    screen.blit(control_msg, (WIDTH // 2 - control_msg.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.update()

def show_game_over():
    global game_running, game_over
    game_running = False
    game_over = True
    screen.fill(SKY_BLUE)
    over_text = big_font.render("Game Over", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    retry_text = font.render("Press SPACE to Retry or ESC to Quit", True, BLACK)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 10))
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 30))
    pygame.display.update()

def add_pipe():
    center_y = random.randint(150, 350)
    top = center_y - PIPE_GAP // 2
    bottom = center_y + PIPE_GAP // 2
    pipes.append({'x': WIDTH, 'top': top, 'bottom': bottom, 'passed': False})

def draw_game():
    screen.fill(SKY_BLUE)

    # Draw Bird
    pygame.draw.circle(screen, BLACK, (100, int(bird_y)), BIRD_RADIUS)

    # Draw Pipes
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, PIPE_WIDTH, pipe['top']))
        pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['bottom'], PIPE_WIDTH, HEIGHT - pipe['bottom']))

    # Draw Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

# Main Loop
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if showing_start_menu:
                    showing_start_menu = False
                    reset_game()
                elif not game_running and game_over:
                    reset_game()
                else:
                    bird_velocity = JUMP_STRENGTH

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if showing_start_menu:
        show_start_menu()
        continue

    if not game_running and game_over:
        show_game_over()
        continue

    # Game logic
    bird_velocity += GRAVITY
    bird_y += bird_velocity

    if len(pipes) == 0 or pipes[-1]['x'] < WIDTH - 200:
        add_pipe()

    for pipe in pipes:
        pipe['x'] -= PIPE_SPEED

        if not pipe['passed'] and pipe['x'] + PIPE_WIDTH < 100:
            score += 1
            pipe['passed'] = True

        # Collision
        if 100 + BIRD_RADIUS > pipe['x'] and 100 - BIRD_RADIUS < pipe['x'] + PIPE_WIDTH:
            if bird_y - BIRD_RADIUS < pipe['top'] or bird_y + BIRD_RADIUS > pipe['bottom']:
                show_game_over()

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe['x'] + PIPE_WIDTH > 0]

    # Check boundaries
    if bird_y - BIRD_RADIUS < 0 or bird_y + BIRD_RADIUS > HEIGHT:
        show_game_over()

    draw_game()
