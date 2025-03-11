import pygame
import random

# Initialize pygame
pygame.init()
# initialize mixer
pygame.mixer.init()
# font init
font = pygame.font.Font(None, 72)
score_font = pygame.font.Font(None, 48)  # Font for score display



# Game constants
WIDTH, HEIGHT = 800, 1000
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Sounds
pygame.mixer.music.load("./assets/sounds/background.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

shoot_sound = pygame.mixer.Sound("./assets/sounds/fire.mp3")
shoot_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound("./assets/sounds/explosion.wav")
game_over_sound = pygame.mixer.Sound("./assets/sounds/game_over.wav")
game_over_sound.set_volume(0.5)

# Spaceship properties
ship_width, ship_height = 60, 90
ship_x, ship_y = WIDTH // 2 - ship_width // 2, HEIGHT - 150
ship_speed = 5

# Ship Image
ship_image = pygame.image.load("./assets/images/ship.png").convert_alpha()
ship_image = pygame.transform.scale(ship_image, (ship_width, ship_height))
ship_mask = pygame.mask.from_surface(ship_image)


# Bullets
bullets = []
bullet_speed = 5
bullet_acceleration = 17
bullet_width, bullet_height = 12, 60

# Bullet Image
bullet_image = pygame.image.load("./assets/images/bullet.png").convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))
bullet_mask = pygame.mask.from_surface(bullet_image)

# Function to create a new bullet
def create_new_bullet():
    bullets.append({'rect': pygame.Rect(ship_x + ship_width // 2-bullet_width // 2, ship_y, bullet_width, bullet_height), 'mask': bullet_mask})

# Enemy properties
enemies = []
enemy_width, enemy_height = 30, 30

# Enemy image
enemy_image = pygame.image.load("./assets/images/enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
enemy_mask = pygame.mask.from_surface(enemy_image)

def create_enemy():
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-500, -40)
    enemies.append({'rect': pygame.Rect(x, y, enemy_width, enemy_height), 'mask': enemy_mask, 'speed': random.randint(2, 3)})


# Background stars
background_star_image = pygame.image.load("./assets/images/stars.jpg")
background_star_image = pygame.transform.scale(background_star_image, (WIDTH, HEIGHT))
background_1_y = 0
background_2_y = -HEIGHT
background_speed = 1.2



# Score
score = 0

def draw_score():
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

ship_destroyed = False
running = True
clock = pygame.time.Clock()
show_text = True
last_toggle_time = pygame.time.get_ticks()

while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    if current_time - last_toggle_time > 500:
        show_text = not show_text
        last_toggle_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                create_new_bullet()
                shoot_sound.play()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_x > 0:
        ship_x -= ship_speed
    if keys[pygame.K_RIGHT] and ship_x < WIDTH - ship_width:
        ship_x += ship_speed
    if keys[pygame.K_UP] and ship_y > 0:
        ship_y -= ship_speed
    if keys[pygame.K_DOWN] and ship_y < HEIGHT - ship_height:
        ship_y += ship_speed


    for enemy in enemies[:]:
        enemy_rect = enemy['rect']
        offset = (enemy_rect.x - ship_x, enemy_rect.y - ship_y)
        if ship_mask.overlap(enemy['mask'], offset):
            ship_destroyed = True

    if not ship_destroyed:
        background_1_y += background_speed
        background_2_y += background_speed
        if background_1_y > HEIGHT:
            background_1_y = -HEIGHT
        if background_2_y > HEIGHT:
            background_2_y = -HEIGHT

        for bullet in bullets[:]:
            bullet['rect'].y -= (bullet_speed+bullet_acceleration)
            if bullet['rect'].y < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy['rect'].y += enemy['speed']
            if enemy['rect'].y > HEIGHT:
                enemies.remove(enemy)
                create_enemy()

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                enemy_rect = enemy['rect']
                offset = (bullet['rect'].x - enemy_rect.x, bullet['rect'].y - enemy_rect.y)
                if enemy['mask'].overlap(bullet['mask'], offset):
                    explosion_sound.play()
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10  # Increase score when an enemy is destroyed
                    create_enemy()
                    break

        screen.blit(background_star_image, (0, background_1_y))
        screen.blit(background_star_image, (0, background_2_y))
        screen.blit(ship_image, (ship_x, ship_y))
        draw_score()


        for bullet in bullets:
            screen.blit(bullet_image, (bullet['rect'].x, bullet['rect'].y))

        for enemy in enemies:
            screen.blit(enemy_image, (enemy['rect'].x, enemy['rect'].y))

        if len(enemies) < 15:
            create_enemy()
    else:
        game_over_sound.play()
        if show_text:
            text = font.render("Game Over", True, YELLOW)
        else:
            text = font.render("Game Over", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
