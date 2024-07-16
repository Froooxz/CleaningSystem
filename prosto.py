import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 500
BLUE_SIZE = 50
CIRCLE_RADIUS = 5
FPS = 60
REMOVE_DELAY = 100
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_X = SCREEN_WIDTH + 10
BUTTON_Y = SCREEN_HEIGHT - BUTTON_HEIGHT - 10
MOVE_SPEED = 7
PROHODI = 2
HOLD_TIME = 100

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Настройки экрана
WINDOW_WIDTH = SCREEN_WIDTH + BUTTON_WIDTH + 30
screen = pygame.display.set_mode((WINDOW_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cleaning System Model")

# Шрифт
font = pygame.font.Font(None, 24)

# Создание красных кругов
circles = [(random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS),
            random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS)) for _ in range(50)]

# Положение синего квадрата
blue_rect = pygame.Rect((SCREEN_WIDTH - BLUE_SIZE) // 2, 0, BLUE_SIZE, BLUE_SIZE)
holding_space = False
last_remove_time = 0
start_press_time = 0
auto_mode = False
remaining_hold_time = 0
passes_completed = 0  # Счетчик завершенных проходов

def auto_clean(direction):
    global passes_completed
    step = BLUE_SIZE if direction == 'down' else -BLUE_SIZE
    start = 0 if direction == 'down' else SCREEN_HEIGHT - BLUE_SIZE
    end = SCREEN_HEIGHT -BLUE_SIZE if direction == 'down' else 0

    for y in range(start, end, step):
        hold_and_clean()
        move_blue_rect(y + step)

        if direction == 'up' and blue_rect.top <= 0:  # Проверка на верхний предел
            passes_completed += 1
            if passes_completed >= PROHODI:  # Проверка на количество проходов
                return  # Остановить выполнение функции

    if direction == 'down':
        auto_clean('up')

def move_blue_rect(target_y):
    while blue_rect.y != target_y:
        blue_rect.y += MOVE_SPEED if blue_rect.y < target_y else -MOVE_SPEED
        if (blue_rect.y > target_y and blue_rect.y - MOVE_SPEED < target_y) or \
           (blue_rect.y < target_y and blue_rect.y + MOVE_SPEED > target_y):
            blue_rect.y = target_y
        draw_game_screen()
        pygame.display.flip()
        clock.tick(FPS)

def hold_and_clean():
    global holding_space, start_press_time, last_remove_time, remaining_hold_time
    remaining_hold_time = HOLD_TIME
    start_press_time = pygame.time.get_ticks()
    last_remove_time = start_press_time
    holding_space = True

    while remaining_hold_time > 0:
        current_time = pygame.time.get_ticks()
        if current_time - last_remove_time >= REMOVE_DELAY:
            last_remove_time = current_time
            circles[:] = [circle for circle in circles if not circle_inside_blue_rect(circle)]
        elapsed_time = current_time - start_press_time
        remaining_hold_time -= elapsed_time
        start_press_time = current_time

        draw_game_screen()
        pygame.display.flip()
        clock.tick(FPS)

    holding_space = False

def circle_inside_blue_rect(circle):
    x, y = circle
    return blue_rect.left <= x <= blue_rect.right and blue_rect.top <= y <= blue_rect.bottom

def draw_game_screen():
    screen.fill(WHITE)
    for circle in circles:
        pygame.draw.circle(screen, RED, circle, CIRCLE_RADIUS)
    pygame.draw.rect(screen, BLUE, blue_rect)
    pygame.draw.rect(screen, GRAY, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    button_text = font.render("Auto Mode", True, BLACK)
    button_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(button_text, button_rect)

running = True
clock = pygame.time.Clock()
moving_up = False
moving_down = False

while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not auto_mode:
            if event.key == pygame.K_UP:
                moving_up = True
            elif event.key == pygame.K_DOWN:
                moving_down = True
            elif event.key == pygame.K_SPACE:
                holding_space = True
                start_press_time = current_time
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                moving_up = False
            elif event.key == pygame.K_DOWN:
                moving_down = False
            elif event.key == pygame.K_SPACE:
                holding_space = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                auto_mode = not auto_mode
                if auto_mode:
                    passes_completed = 0  # Сброс счетчика проходов
                    for _ in range(PROHODI):
                        auto_clean('down')

    if moving_up and blue_rect.top > 0:
        blue_rect.y -= MOVE_SPEED
    if moving_down and blue_rect.bottom < SCREEN_HEIGHT:
        blue_rect.y += MOVE_SPEED

    if blue_rect.bottom >= SCREEN_HEIGHT and not auto_mode:
        auto_clean('up')

    if holding_space:
        if current_time - last_remove_time >= REMOVE_DELAY:
            last_remove_time = current_time
            circles[:] = [circle for circle in circles if not circle_inside_blue_rect(circle)]
        elapsed_time = current_time - start_press_time
        remaining_hold_time -= elapsed_time
        start_press_time = current_time
        if remaining_hold_time <= 0:
            holding_space = False

    draw_game_screen()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
