import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Rocks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - player_size * 2]
player_speed = 7

# Bullet
bullet_size = 5
bullet_speed = 10
bullet_list = []

# Rocks
rock_size = 50
rock_list = []
rock_speed = 5

# Score
score = 0
clock = pygame.time.Clock()

def drop_rocks():
    delay = random.random()
    if len(rock_list) < 5 and delay < 0.05:
        x_pos = random.randint(0, WIDTH - rock_size)
        y_pos = 0
        rock_list.append([x_pos, y_pos])

def draw_rocks():
    for rock_pos in rock_list:
        pygame.draw.rect(screen, BLACK, (rock_pos[0], rock_pos[1], rock_size, rock_size))

def update_rocks(score):
    for index, rock_pos in enumerate(rock_list):
        if rock_pos[1] >= 0 and rock_pos[1] < HEIGHT:
            rock_pos[1] += rock_speed
        else:
            rock_list.pop(index)
            score += 1
    return score

def collision_check():
    for rock_pos in rock_list:
        if detect_collision(rock_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, rock_pos):
    p_x, p_y = player_pos
    r_x, r_y = rock_pos
    if (r_x >= p_x and r_x < (p_x + player_size)) or (p_x >= r_x and p_x < (r_x + rock_size)):
        if (r_y >= p_y and r_y < (p_y + player_size)) or (p_y >= r_y and p_y < (r_y + rock_size)):
            return True
    return False

def draw_player():
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

def move_player(keys):
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

def draw_bullets():
    for bullet in bullet_list:
        pygame.draw.rect(screen, BLACK, (bullet[0], bullet[1], bullet_size, bullet_size))

def move_bullets():
    for bullet in bullet_list:
        bullet[1] -= bullet_speed

def fire_bullet(player_pos):
    x, y = player_pos
    bullet_list.append([x + player_size // 2, y])

def remove_hit_rocks():
    global score
    for bullet in bullet_list:
        for rock_pos in rock_list:
            if detect_collision(bullet, rock_pos):
                rock_list.remove(rock_pos)
                bullet_list.remove(bullet)
                score += 1
                break

game_over = False

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_bullet(player_pos)

    keys = pygame.key.get_pressed()
    move_player(keys)

    screen.fill(WHITE)

    drop_rocks()
    score = update_rocks(score)
    rock_speed += 0.001  # Increase rock speed gradually
    text = "Score: " + str(score)
    label = pygame.font.Font(None, 36).render(text, True, BLACK)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))

    if collision_check():
        game_over = True
        break

    draw_rocks()
    draw_player()

    move_bullets()
    draw_bullets()

    remove_hit_rocks()

    clock.tick(30)
    pygame.display.update()

pygame.quit()