import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 50  # Ширина игрового поля
SCREEN_HEIGHT = 600  # Высота игрового поля
BLUE_SIZE = 50  # Размер синего квадрата
CIRCLE_RADIUS = 10  # Радиус красного круга
FPS = 60  # Частота обновления экрана
REMOVE_DELAY = 250  # Задержка удаления красных кругов в миллисекундах
BUTTON_WIDTH = 150  # Ширина кнопки
BUTTON_HEIGHT = 50  # Высота кнопки
BUTTON_X = SCREEN_WIDTH + 10  # Положение кнопки по оси x
BUTTON_Y = SCREEN_HEIGHT - BUTTON_HEIGHT - 10  # Положение кнопки по оси y
MOVE_SPEED = 2  # Скорость перемещения синего квадрата
SENSOR_HEIGHT = 10  # Высота сенсоров

# Цвета
BLACK = (0, 0, 0)  # Черный
WHITE = (255, 255, 255)  # Белый
RED = (255, 0, 0)  # Красный
BLUE = (0, 0, 255)  # Синий
GRAY = (200, 200, 200)  # Серый

# Настройки экрана
WINDOW_WIDTH = SCREEN_WIDTH + BUTTON_WIDTH + 20  # Дополнительное пространство для кнопки
screen = pygame.display.set_mode((WINDOW_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Game")

# Шрифт для отображения текста
font = pygame.font.Font(None, 24)

# Создание красных кругов
circles = []
for _ in range(50):  # Количество красных кругов
    x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)  # Случайная позиция круга по оси x
    y = random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS)  # Случайная позиция круга по оси y
    circles.append((x, y))  # Добавление круга в список

# Синий квадрат в начальной позиции
blue_rect = pygame.Rect((SCREEN_WIDTH - BLUE_SIZE) // 2, 0, BLUE_SIZE, BLUE_SIZE)
holding_space = False  # Флаг удержания пробела
last_remove_time = 0  # Время последнего удаления круга
start_press_time = 0  # Время начала нажатия пробела
auto_mode = False  # Флаг автоматического режима
remaining_hold_time = 0  # Оставшееся время удержания

def auto_clean():
    """Функция для автоматического режима"""
    global holding_space, start_press_time, last_remove_time, remaining_hold_time

    for y in range(0, SCREEN_HEIGHT, BLUE_SIZE):
        target_y = y
        while blue_rect.y != target_y:
            if blue_rect.y < target_y:
                blue_rect.y += MOVE_SPEED
                if blue_rect.y > target_y:
                    blue_rect.y = target_y
            else:
                blue_rect.y -= MOVE_SPEED
                if blue_rect.y < target_y:
                    blue_rect.y = target_y
            draw_game_screen()
            pygame.display.flip()
            clock.tick(FPS)

        if any(circle_inside_blue_rect(circle) for circle in circles):
            hold_time = random.uniform(1, 3)  # Случайное время удержания пробела
            remaining_hold_time = hold_time
            start_press_time = pygame.time.get_ticks()
            last_remove_time = start_press_time
            holding_space = True

            while any(circle_inside_blue_rect(circle) for circle in circles) and remaining_hold_time > 0:
                current_time = pygame.time.get_ticks()
                if current_time - last_remove_time >= REMOVE_DELAY:
                    last_remove_time = current_time
                    circles[:] = [circle for circle in circles if not circle_inside_blue_rect(circle)]
                elapsed_time = (current_time - start_press_time) / 1000
                remaining_hold_time -= elapsed_time
                start_press_time = current_time
                draw_game_screen()
                pygame.display.flip()
                clock.tick(FPS)

            holding_space = False

def circle_inside_blue_rect(circle):
    """Проверка, находится ли круг внутри синего квадрата"""
    x, y = circle
    return blue_rect.left <= x <= blue_rect.right and blue_rect.top <= y <= blue_rect.bottom

def circle_inside_sensor(sensor_rect, circle):
    """Проверка, находится ли круг внутри сенсора"""
    x, y = circle
    return sensor_rect.left <= x <= sensor_rect.right and sensor_rect.top <= y <= sensor_rect.bottom

def draw_game_screen():
    """Функция для рисования всех элементов на экране"""
    # Очистка экрана
    screen.fill(WHITE)

    # Рисование красных кругов
    for circle in circles:
        pygame.draw.circle(screen, RED, circle, CIRCLE_RADIUS)

    # Рисование синего квадрата
    pygame.draw.rect(screen, BLUE, blue_rect)

    # Рисование сенсоров
    top_sensor = pygame.Rect(blue_rect.left, blue_rect.top - SENSOR_HEIGHT, blue_rect.width, SENSOR_HEIGHT)
    bottom_sensor = pygame.Rect(blue_rect.left, blue_rect.bottom, blue_rect.width, SENSOR_HEIGHT)
    pygame.draw.rect(screen, GRAY, top_sensor)
    pygame.draw.rect(screen, GRAY, bottom_sensor)

    # Отображение таймера, если удерживается пробел
    if holding_space and remaining_hold_time > 0:
        timer_text = font.render(f"{remaining_hold_time:.1f}s", True, BLACK)
        screen.blit(timer_text, (blue_rect.right + 5, blue_rect.centery - timer_text.get_height() // 2))

    # Рисование кнопки
    pygame.draw.rect(screen, GRAY, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    button_text = font.render("Auto Mode", True, BLACK)
    button_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(button_text, button_rect)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

moving_up = False
moving_down = False

while running:
    current_time = pygame.time.get_ticks()  # Текущее время в миллисекундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка на закрытие окна
            running = False
        elif event.type == pygame.KEYDOWN and not auto_mode:
            if event.key == pygame.K_UP:  # Начало перемещения вверх
                moving_up = True
            elif event.key == pygame.K_DOWN:  # Начало перемещения вниз
                moving_down = True
            elif event.key == pygame.K_SPACE:  # Удержание пробела
                holding_space = True
                start_press_time = current_time
                last_remove_time = current_time
                remaining_hold_time = random.uniform(1, 3)  # Случайное время удержания пробела
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:  # Остановка перемещения вверх
                moving_up = False
            elif event.key == pygame.K_DOWN:  # Остановка перемещения вниз
                moving_down = False
            elif event.key == pygame.K_SPACE:  # Отпускание пробела
                holding_space = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                auto_mode = not auto_mode  # Переключение режима
                if auto_mode:
                    auto_clean()  # Запуск автоматического режима

    # Плавное перемещение синего квадрата
    if moving_up and blue_rect.top > 0:
        blue_rect.y -= MOVE_SPEED
    if moving_down and blue_rect.bottom < SCREEN_HEIGHT:
        blue_rect.y += MOVE_SPEED

    # Сенсоры
    top_sensor = pygame.Rect(blue_rect.left, blue_rect.top - SENSOR_HEIGHT, blue_rect.width, SENSOR_HEIGHT)
    bottom_sensor = pygame.Rect(blue_rect.left, blue_rect.bottom, blue_rect.width, SENSOR_HEIGHT)

    # Проверка сенсоров и начало очистки
    if not holding_space and (any(circle_inside_sensor(top_sensor, circle) for circle in circles) or any(circle_inside_sensor(bottom_sensor, circle) for circle in circles)):
        holding_space = True
        start_press_time = current_time
        last_remove_time = current_time
        remaining_hold_time = random.uniform(1, 3)  # Случайное время удержания пробела

    # Удаление красных кругов при удержании пробела
    if holding_space:
        if current_time - last_remove_time >= REMOVE_DELAY:  # Проверка задержки удаления
            last_remove_time = current_time
            circles[:] = [circle for circle in circles if not circle_inside_blue_rect(circle)]
        elapsed_time = (current_time - start_press_time) / 1000
        remaining_hold_time -= elapsed_time
        start_press_time = current_time
        if remaining_hold_time <= 0:
            holding_space = False

    # Очистка экрана и рисование всех элементов
    draw_game_screen()

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)  # Ограничение FPS

pygame.quit()  # Завершение Pygame
