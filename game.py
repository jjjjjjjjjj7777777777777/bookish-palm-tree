import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бей Крота")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

target_img = pygame.image.load("krot.png")
target_img = pygame.transform.scale(target_img, (CELL_SIZE - 20, CELL_SIZE - 20))

background_img = pygame.image.load("polyana.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 2)

def draw_target(row, col):
    x = col * CELL_SIZE + (CELL_SIZE - (CELL_SIZE - 20)) // 2
    y = row * CELL_SIZE + (CELL_SIZE - (CELL_SIZE - 20)) // 2
    screen.blit(target_img, (x, y))

current_row = random.randint(0, GRID_SIZE - 1)
current_col = random.randint(0, GRID_SIZE - 1)

score = 0
score_target = 100
time_limit = 60
start_time = pygame.time.get_ticks()
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

game_over = False
win = False

MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 1200)

def restart_game():
    global current_row, current_col, score, start_time, game_over, win
    current_row = random.randint(0, GRID_SIZE - 1)
    current_col = random.randint(0, GRID_SIZE - 1)
    score = 0
    start_time = pygame.time.get_ticks()
    game_over = False
    win = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == MOVE_EVENT:
                current_row = random.randint(0, GRID_SIZE - 1)
                current_col = random.randint(0, GRID_SIZE - 1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_col = mouse_x // CELL_SIZE
                clicked_row = mouse_y // CELL_SIZE
                
                if clicked_row == current_row and clicked_col == current_col:
                    score += 1
                    current_row = random.randint(0, GRID_SIZE - 1)
                    current_col = random.randint(0, GRID_SIZE - 1)
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game()

    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = max(0, time_limit - elapsed_time)
        
        if score >= score_target:
            game_over = True
            win = True
        elif remaining_time <= 0:
            game_over = True
            win = False

    screen.blit(background_img, (0, 0))
    draw_grid()
    draw_target(current_row, current_col)
    
    score_text = font.render(f"{score}/{score_target}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    if not game_over:
        time_text = font.render(f"{int(remaining_time)}", True, BLACK)
        screen.blit(time_text, (10, 50))
    else:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 255, 0) if win else (255, 0, 0))
        screen.blit(overlay, (0, 0))
        
        msg = "WIN!" if win else "LOSE!"
        msg_text = font.render(msg, True, BLACK)
        screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, HEIGHT // 2 - 50))
        
        restart_text = font.render("PRESS R TO RESTART", True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()