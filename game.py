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
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Player
player_width = 50
player_height = 40
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - player_height - 20, player_width, player_height)
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

# Power-ups
POWERUP_SIZE = 20
powerups = []
weapon_level = 1

# Game variables
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Stars (background)
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# Enemy types
ENEMY_TYPES = ['bee', 'butterfly', 'boss']

class PowerUp:
    def __init__(self, x):
        self.rect = pygame.Rect(x, -POWERUP_SIZE, POWERUP_SIZE, POWERUP_SIZE)
        self.color = (0, 255, 0)  # Green
        self.speed = 2

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)  # White border


def draw_player(surface, rect):
    # Main body of the ship
    pygame.draw.polygon(surface, (100, 100, 255), [
        (rect.left + rect.width // 2, rect.top),
        (rect.left, rect.bottom),
        (rect.right, rect.bottom)
    ])

    # Cockpit
    pygame.draw.ellipse(surface, (200, 200, 255),
                        (rect.centerx - 10, rect.centery - 5, 20, 20))

    # Wings
    pygame.draw.polygon(surface, (50, 50, 200), [
        (rect.left, rect.bottom),
        (rect.left - 15, rect.bottom + 10),
        (rect.left + 10, rect.bottom - 5)
    ])
    pygame.draw.polygon(surface, (50, 50, 200), [
        (rect.right, rect.bottom),
        (rect.right + 15, rect.bottom + 10),
        (rect.right - 10, rect.bottom - 5)
    ])

    # Engines
    pygame.draw.rect(surface, (255, 100, 0),
                     (rect.left + 5, rect.bottom, 10, 5))
    pygame.draw.rect(surface, (255, 100, 0),
                     (rect.right - 15, rect.bottom, 10, 5))

    # Engine glow
    pygame.draw.polygon(surface, (255, 200, 0), [
        (rect.left + 5, rect.bottom + 5),
        (rect.left + 10, rect.bottom + 15),
        (rect.left + 15, rect.bottom + 5)
    ])
    pygame.draw.polygon(surface, (255, 200, 0), [
        (rect.right - 15, rect.bottom + 5),
        (rect.right - 10, rect.bottom + 15),
        (rect.right - 5, rect.bottom + 5)
    ])

def draw_enemy(surface, enemy):
    rect = enemy['rect']
    enemy_type = enemy['type']

    if enemy_type == 'bee':
        # Draw bee-like enemy (yellow)
        pygame.draw.rect(surface, YELLOW, (rect.left, rect.top, rect.width, rect.height // 2))
        pygame.draw.rect(surface, YELLOW, (rect.left + rect.width // 4, rect.centery, rect.width // 2, rect.height // 2))
        # Wings
        pygame.draw.circle(surface, YELLOW, (rect.left, rect.centery), rect.width // 4)
        pygame.draw.circle(surface, YELLOW, (rect.right, rect.centery), rect.width // 4)
        # Eyes
        pygame.draw.circle(surface, BLACK, (rect.left + rect.width // 3, rect.top + rect.height // 3), 2)
        pygame.draw.circle(surface, BLACK, (rect.right - rect.width // 3, rect.top + rect.height // 3), 2)

    elif enemy_type == 'butterfly':
        # Draw butterfly-like enemy (cyan)
        pygame.draw.rect(surface, CYAN, (rect.left, rect.top, rect.width, rect.height // 2))
        # Wings
        pygame.draw.circle(surface, CYAN, (rect.left, rect.centery), rect.width // 2)
        pygame.draw.circle(surface, CYAN, (rect.right, rect.centery), rect.width // 2)
        # Antennae
        pygame.draw.line(surface, CYAN, (rect.centerx - 5, rect.top), (rect.centerx - 10, rect.top - 10), 2)
        pygame.draw.line(surface, CYAN, (rect.centerx + 5, rect.top), (rect.centerx + 10, rect.top - 10), 2)

    elif enemy_type == 'boss':
        # Draw boss-like enemy (magenta)
        pygame.draw.rect(surface, MAGENTA, rect)
        # Eyes
        pygame.draw.circle(surface, WHITE, (rect.left + rect.width // 4, rect.centery), rect.width // 8)
        pygame.draw.circle(surface, WHITE, (rect.right - rect.width // 4, rect.centery), rect.width // 8)
        pygame.draw.circle(surface, BLACK, (rect.left + rect.width // 4, rect.centery), rect.width // 16)
        pygame.draw.circle(surface, BLACK, (rect.right - rect.width // 4, rect.centery), rect.width // 16)
        # Mouth
        pygame.draw.arc(surface, WHITE, (rect.left + rect.width // 4, rect.centery, rect.width // 2, rect.height // 2), 3.14, 2 * 3.14, 2)

def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_size)
    y = -enemy_size
    enemy_type = random.choice(ENEMY_TYPES)
    enemies.append({'rect': pygame.Rect(x, y, enemy_size, enemy_size), 'type': enemy_type})

def spawn_powerup():
    x = random.randint(0, WIDTH - POWERUP_SIZE)
    powerups.append(PowerUp(x))


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
                if weapon_level == 1:
                    bullets.append(pygame.Rect(player.centerx - bullet_width // 2, player.top, bullet_width, bullet_height))
                elif weapon_level == 2:
                    bullets.append(pygame.Rect(player.left + 5, player.top, bullet_width, bullet_height))
                    bullets.append(pygame.Rect(player.right - 5 - bullet_width, player.top, bullet_width, bullet_height))
                elif weapon_level == 3:
                    bullets.append(pygame.Rect(player.centerx - bullet_width // 2, player.top, bullet_width, bullet_height))
                    bullets.append(pygame.Rect(player.left + 5, player.top, bullet_width, bullet_height))
                    bullets.append(pygame.Rect(player.right - 5 - bullet_width, player.top, bullet_width, bullet_height))

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
        enemy['rect'].y += enemy_speed
        if enemy['rect'].top > HEIGHT:
            enemies.remove(enemy)
            lives -= 1

    # Spawn enemies
    spawn_timer += 1
    if spawn_timer >= 60:
        spawn_enemy()
        spawn_timer = 0

    # Spawn power-ups
    if random.randint(1, 500) == 1:  # Adjust frequency as needed
        spawn_powerup()

# Move and remove off-screen power-ups
    for powerup in powerups[:]:
        powerup.move()
        if powerup.rect.top > HEIGHT:
            powerups.remove(powerup)

    # Check collisions
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy['rect'].colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10
                break
        if enemy['rect'].colliderect(player):
            enemies.remove(enemy)
            lives -= 1
            weapon_level = 1  # Reset weapon level

    # Check collision with power-ups
    for powerup in powerups[:]:
        if player.colliderect(powerup.rect):
            powerups.remove(powerup)
            weapon_level = min(weapon_level + 1, 3)

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

    # Draw power-ups
    for powerup in powerups:
        powerup.draw(screen)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    weapon_text = font.render(f"Weapon: Level {weapon_level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))
    screen.blit(weapon_text, (10, 40))

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
