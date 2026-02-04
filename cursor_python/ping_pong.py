"""
Ping-Pong Game - Python/Pygame
Features: game environment, player input, ball movement & collisions, score keeping.
"""

import pygame
import sys

# Constants
WIDTH, HEIGHT = 800, 500
PADDLE_WIDTH, PADDLE_HEIGHT = 12, 80
PADDLE_SPEED = 8
BALL_SIZE = 12
BALL_SPEED = 6
FPS = 60

# AI
AI_SPEED = 6

# Colors
BG_COLOR = (15, 25, 35)
PADDLE_COLOR = (220, 220, 220)
BALL_COLOR = (255, 255, 255)
TEXT_COLOR = (200, 200, 200)
LINE_COLOR = (60, 70, 80)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping-Pong")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)

    # Mode selection screen
    single_player = None
    while single_player is None:
        screen.fill(BG_COLOR)
        title = font.render("Ping-Pong", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
        msg = font_small.render("Press 1 = Single Player (vs Computer)  |  Press 2 = Two Players", True, TEXT_COLOR)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 220))
        hint = font_small.render("In game: P or Space = Pause", True, (100, 100, 100))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 280))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    single_player = True
                elif event.key == pygame.K_2:
                    single_player = False
        clock.tick(FPS)

    # Game environment: paddles and ball
    paddle1 = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

    ball_dx = BALL_SPEED
    ball_dy = 0
    score1 = 0
    score2 = 0
    paused = False

    def reset_ball(direction=1):
        """Place ball at center and set initial direction."""
        nonlocal ball_dx, ball_dy
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_dx = BALL_SPEED * direction
        ball_dy = 0

    def draw():
        screen.fill(BG_COLOR)
        # Center line (dashed)
        for y in range(0, HEIGHT, 24):
            pygame.draw.rect(screen, LINE_COLOR, (WIDTH // 2 - 2, y, 4, 12))
        pygame.draw.rect(screen, PADDLE_COLOR, paddle1)
        pygame.draw.rect(screen, PADDLE_COLOR, paddle2)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)
        label1 = "You" if single_player else "P1"
        label2 = "CPU" if single_player else "P2"
        s1 = font.render(str(score1), True, TEXT_COLOR)
        s2 = font.render(str(score2), True, TEXT_COLOR)
        l1 = font_small.render(label1, True, TEXT_COLOR)
        l2 = font_small.render(label2, True, TEXT_COLOR)
        screen.blit(l1, (WIDTH // 4 - l1.get_width() // 2, 8))
        screen.blit(l2, (3 * WIDTH // 4 - l2.get_width() // 2, 8))
        screen.blit(s1, (WIDTH // 4 - s1.get_width() // 2, 38))
        screen.blit(s2, (3 * WIDTH // 4 - s2.get_width() // 2, 38))
        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BG_COLOR)
            screen.blit(overlay, (0, 0))
            pause_text = font.render("Paused", True, TEXT_COLOR)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
            hint = font_small.render("Press P or Space to resume", True, TEXT_COLOR)
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.flip()

    def move_computer_paddle():
        target_y = ball.centery - PADDLE_HEIGHT // 2
        diff = target_y - paddle2.y
        move = max(-AI_SPEED, min(AI_SPEED, diff))
        paddle2.y += int(move)
        paddle2.y = max(0, min(HEIGHT - PADDLE_HEIGHT, paddle2.y))

    running = True
    while running:
        # Event / input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_p, pygame.K_SPACE):
                    paused = not paused

        if paused:
            draw()
            clock.tick(FPS)
            continue

        keys = pygame.key.get_pressed()
        # Player 1: W / S — move paddle up and down
        if keys[pygame.K_w] and paddle1.top > 0:
            paddle1.y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
            paddle1.y += PADDLE_SPEED
        # Player 2: human or computer
        if single_player:
            move_computer_paddle()
        else:
            if keys[pygame.K_UP] and paddle2.top > 0:
                paddle2.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
                paddle2.y += PADDLE_SPEED

        # Ball movement
        ball.x += int(ball_dx)
        ball.y += int(ball_dy)

        # Collisions: top and bottom walls — change vertical direction
        if ball.top <= 0:
            ball.top = 0
            ball_dy = abs(ball_dy)
        if ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_dy = -abs(ball_dy)

        # Collisions with paddles — bounce and change horizontal direction
        if ball.colliderect(paddle1):
            ball.left = paddle1.right
            ball_dx = abs(ball_dx)
            # Slight angle based on where ball hits paddle
            hit_pos = (ball.centery - paddle1.centery) / (PADDLE_HEIGHT / 2)
            ball_dy = hit_pos * (BALL_SPEED * 0.8)
        if ball.colliderect(paddle2):
            ball.right = paddle2.left
            ball_dx = -abs(ball_dx)
            hit_pos = (ball.centery - paddle2.centery) / (PADDLE_HEIGHT / 2)
            ball_dy = hit_pos * (BALL_SPEED * 0.8)

        # Score: ball passes paddle (left or right)
        if ball.right <= 0:
            score2 += 1
            reset_ball(-1)
        if ball.left >= WIDTH:
            score1 += 1
            reset_ball(1)

        draw()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
