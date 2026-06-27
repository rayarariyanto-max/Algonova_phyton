import pygame
import random
import os

# ==========================
# INIT
# ==========================
pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The TWS Cat Heads")

clock = pygame.time.Clock()

# ==========================
# PATH
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSET = os.path.join(BASE_DIR, "assets")
AUDIO = os.path.join(BASE_DIR, "audio")

# ==========================
# LOAD IMAGE
# ==========================
background = pygame.image.load(os.path.join(ASSET, "background.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

basket = pygame.image.load(os.path.join(ASSET, "Basket.png"))
basket = pygame.transform.scale(basket, (130, 90))

cat = pygame.image.load(os.path.join(ASSET, "Cat.png"))
cat = pygame.transform.scale(cat, (70, 70))

bomb = pygame.image.load(os.path.join(ASSET, "Bomb.png"))
bomb = pygame.transform.scale(bomb, (60, 60))

pygame.display.set_icon(cat)

# ==========================
# BACKGROUND MUSIC
# ==========================
pygame.mixer.music.load(os.path.join(AUDIO, "bgm.mp3"))
pygame.mixer.music.set_volume(0.4)   # Volume 40%
pygame.mixer.music.play(-1)          # Loop selamanya

# ==========================
# FONT
# ==========================
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 60)

# ==========================
# PLAYER
# ==========================
basket_x = WIDTH // 2
basket_y = HEIGHT - 90
basket_speed = 12

# ==========================
# GAME
# ==========================
score = 0
lives = 3

objects = []

spawn_delay = 36
spawn_timer = 0

running = True

# ==========================
# GAME LOOP
# ==========================
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        basket_x -= basket_speed

    if keys[pygame.K_RIGHT]:
        basket_x += basket_speed

    basket_x = max(0, min(WIDTH - 130, basket_x))

    # Spawn Object
    spawn_timer += 1

    if spawn_timer >= spawn_delay:

        spawn_timer = 0

        object_type = random.choice(["cat", "cat", "cat", "bomb"])

        if object_type == "cat":
            speed = random.randint(4, 4)
        else:
            speed = random.randint(4, 6)

        objects.append({
            "type": object_type,
            "x": random.randint(20, WIDTH - 80),
            "y": -70,
            "speed": speed
        })

    basket_rect = pygame.Rect(basket_x, basket_y, 130, 90)

    for obj in objects[:]:

        obj["y"] += obj["speed"]

        obj_rect = pygame.Rect(obj["x"], obj["y"], 70, 70)

        # Catch
        if basket_rect.colliderect(obj_rect):

            if obj["type"] == "cat":
                score += 1
            else:
                lives -= 1

            objects.remove(obj)
            continue

        # Miss
        if obj["y"] > HEIGHT:

            if obj["type"] == "cat":
                lives -= 1

            objects.remove(obj)

    # ==========================
    # DRAW
    # ==========================
    screen.blit(background, (0, 0))
    screen.blit(basket, (basket_x, basket_y))

    for obj in objects:

        if obj["type"] == "cat":
            screen.blit(cat, (obj["x"], obj["y"]))
        else:
            screen.blit(bomb, (obj["x"], obj["y"]))

    score_text = font.render(f"Score : {score}", True, (255,255,255))
    lives_text = font.render(f"Lives : {lives}", True, (255,255,255))

    screen.blit(score_text, (20,20))
    screen.blit(lives_text, (20,55))

    # Game Over
    if lives <= 0:

        pygame.mixer.music.stop()

        over = big_font.render("GAME OVER", True, (255,0,0))
        final = font.render(f"Final Score : {score}", True, (255,255,255))

        screen.blit(over, (170,230))
        screen.blit(final, (285,300))

        pygame.display.update()
        pygame.time.wait(3000)

        running = False

    pygame.display.update()

pygame.quit()