
import pygame
import random
import sys

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
PADDLE_SPEED = 7
AI_SPEED = 6
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- Game Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping-Pong by Gemini")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)

# --- Game Objects ---
player_paddle = pygame.Rect(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# --- Game Variables ---
ball_speed_x_current = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y_current = BALL_SPEED_Y * random.choice((1, -1))
player_score = 0
opponent_score = 0
player_speed_current = 0

def reset_ball():
    """Resets the ball to the center with a random direction."""
    global ball_speed_x_current, ball_speed_y_current
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed_x_current = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y_current = BALL_SPEED_Y * random.choice((1, -1))

def draw_elements():
    """Draws all game elements to the screen."""
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    player_text = font.render(str(player_score), True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH // 4, 10))

    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(opponent_text, (SCREEN_WIDTH * 3 // 4 - opponent_text.get_width(), 10))

# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # --- Player Input ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player_speed_current += PADDLE_SPEED
            if event.key == pygame.K_w:
                player_speed_current -= PADDLE_SPEED
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player_speed_current -= PADDLE_SPEED
            if event.key == pygame.K_w:
                player_speed_current += PADDLE_SPEED

    # --- Game Logic ---
    
    # Move player paddle
    player_paddle.y += player_speed_current

    # AI Opponent Logic
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += AI_SPEED
    if opponent_paddle.centery > ball.centery:
        opponent_paddle.y -= AI_SPEED

    # Paddle boundary checking
    if player_paddle.top < 0:
        player_paddle.top = 0
    if player_paddle.bottom > SCREEN_HEIGHT:
        player_paddle.bottom = SCREEN_HEIGHT
    if opponent_paddle.top < 0:
        opponent_paddle.top = 0
    if opponent_paddle.bottom > SCREEN_HEIGHT:
        opponent_paddle.bottom = SCREEN_HEIGHT
        
    # Move ball
    ball.x += ball_speed_x_current
    ball.y += ball_speed_y_current

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y_current *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x_current *= -1.1 # Speed up ball slightly on each hit

    # Scoring
    if ball.left <= 0:
        opponent_score += 1
        reset_ball()
    
    if ball.right >= SCREEN_WIDTH:
        player_score += 1
        reset_ball()

    # --- Drawing ---
    draw_elements()
    pygame.display.flip()
    clock.tick(60)

