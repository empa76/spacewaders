import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Defender")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player
player_width = 40
player_height = 30
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - player_height - 10, player_width, player_height)
player_speed = 5

# Bullets
bullet_width = 5
bullet_height = 10
bullets = []
bullet_speed = 7

# Enemies
enemy_size = 30
enemies = []
enemy_speed = 2

# Game variables
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Stars (background)
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

def draw_player(surface, rect):
    pygame.draw.polygon(surface, GREEN, [
        (rect.left + rect.width // 2, rect.top),
        (rect.left, rect.bottom),
        (rect.right, rect.bottom)
    ])

def draw_enemy(surface, rect):
    pygame.draw.circle(surface, RED, rect.center, rect.width // 2)

def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_size)
    y = -enemy_size
    enemies.append(pygame.Rect(x, y, enemy_size, enemy_size))

# Game loop
clock = pygame.time.Clock()
running = True
spawn_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.centerx - bullet_width // 2, player.top, bullet_width, bullet_height))

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            lives -= 1

    # Spawn enemies
    spawn_timer += 1
    if spawn_timer >= 60:
        spawn_enemy()
        spawn_timer = 0

    # Check collisions
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10
                break
        if enemy.colliderect(player):
            enemies.remove(enemy)
            lives -= 1

    # Draw everything
    screen.fill(BLACK)

    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 1)

    draw_player(screen, player)

    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, bullet)

    for enemy in enemies:
        draw_enemy(screen, enemy)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))

    pygame.display.flip()

    # Check game over
    if lives <= 0:
        running = False

    clock.tick(60)

# Game over screen
screen.fill(BLACK)
game_over_text = font.render("GAME OVER", True, WHITE)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 50))
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

pygame.quit()
