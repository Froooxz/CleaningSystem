import pygame  # Импорт библиотеки Pygame
import random  # Импорт модуля для генерации случайных чисел

# Инициализация Pygame
pygame.init()

# Константы для экрана и объектов
SCREEN_WIDTH = 50  # Ширина экрана
SCREEN_HEIGHT = 500  # Высота экрана
BLUE_SIZE = 50  # Размер синего квадрата
CIRCLE_RADIUS = 5  # Радиус красных кругов
FPS = 60  # Частота кадров в секунду
REMOVE_DELAY = 500  # Задержка перед удалением кругов (в миллисекундах)
BUTTON_WIDTH = 150  # Ширина кнопки "Auto Mode"
BUTTON_HEIGHT = 50  # Высота кнопки "Auto Mode"
BUTTON_X = SCREEN_WIDTH + 10  # Положение кнопки "Auto Mode" по X
BUTTON_Y = SCREEN_HEIGHT - BUTTON_HEIGHT - 10  # Положение кнопки "Auto Mode" по Y
MOVE_SPEED = 7  # Скорость перемещения синего квадрата
SENSOR_HEIGHT = 5  # Высота сенсоров (областей для детектирования)

# Цвета
BLACK = (0, 0, 0)  # Черный цвет
WHITE = (255, 255, 255)  # Белый цвет
RED = (255, 0, 0)  # Красный цвет
BLUE = (0, 0, 255)  # Синий цвет
GRAY = (200, 200, 200)  # Серый цвет

# Настройки экрана
WINDOW_WIDTH = SCREEN_WIDTH + BUTTON_WIDTH + 30  # Ширина окна с учетом кнопки
screen = pygame.display.set_mode((WINDOW_WIDTH, SCREEN_HEIGHT))  # Создание экрана Pygame
pygame.display.set_caption("Cleaning System Model")  # Установка заголовка окна

# Шрифт для текста
font = pygame.font.Font(None, 24)

# Создание красных кругов
circles = []
for _ in range(50):
    x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)
    y = random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS)
    circles.append((x, y))

# Начальное положение синего квадрата
blue_rect = pygame.Rect((SCREEN_WIDTH - BLUE_SIZE) // 2, 0, BLUE_SIZE, BLUE_SIZE)
holding_space = False  # Флаг удержания клавиши "пробел"
last_remove_time = 0  # Время последнего удаления кругов
start_press_time = 0  # Время начала удержания клавиши "пробел"
auto_mode = False  # Флаг автоматического режима
remaining_hold_time = 0  # Оставшееся время удержания клавиши "пробел"

# Флаг направления
direction = "down"


def auto_clean():
    global holding_space, start_press_time, last_remove_time, remaining_hold_time

    # Автоматическое движение вверх и вниз по экрану
    for y in range(0, SCREEN_HEIGHT-BLUE_SIZE-SENSOR_HEIGHT, BLUE_SIZE):
        target_y = y + BLUE_SIZE
        reached_target = False
        circle_count = 0

        while not reached_target:
            if blue_rect.y < target_y:
                blue_rect.y += MOVE_SPEED
                if blue_rect.y >= target_y:
                    blue_rect.y = target_y
                    reached_target = True
            elif blue_rect.y > target_y:
                target_y = y
                blue_rect.y -= MOVE_SPEED
                if blue_rect.y <= target_y:
                    blue_rect.y = target_y
                    reached_target = True

            # Детектирование кругов в области сенсоров
            top_sensor = pygame.Rect(blue_rect.left, blue_rect.top - SENSOR_HEIGHT, blue_rect.width, SENSOR_HEIGHT)
            bottom_sensor = pygame.Rect(blue_rect.left, blue_rect.bottom, blue_rect.width, SENSOR_HEIGHT)
            circle_count += sum(circle_inside_sensor(top_sensor, circle) for circle in circles)
            circle_count += sum(circle_inside_sensor(bottom_sensor, circle) for circle in circles)

            draw_game_screen()  # Отрисовка игрового экрана
            pygame.display.flip()  # Обновление экрана
            clock.tick(FPS)  # Ограничение частоты кадров

        hold_and_clean(circle_count)  # Удержание и очистка


def hold_and_clean(circle_count):
    global holding_space, start_press_time, last_remove_time, remaining_hold_time
    if circle_count > 0:
        hold_time = circle_count * 1  # Время удержания, зависящее от количества кругов (1 секунда на круг)
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
            draw_game_screen()  # Отрисовка игрового экрана
            pygame.display.flip()  # Обновление экрана
            clock.tick(FPS)  # Ограничение частоты кадров

        holding_space = False


def circle_inside_blue_rect(circle):
    x, y = circle
    return blue_rect.left <= x <= blue_rect.right and blue_rect.top <= y <= blue_rect.bottom


def circle_inside_sensor(sensor_rect, circle):
    x, y = circle
    return sensor_rect.left <= x <= sensor_rect.right and sensor_rect.top <= y <= sensor_rect.bottom


def draw_game_screen():
    screen.fill(WHITE)  # Заполнение экрана белым цветом

    for circle in circles:
        pygame.draw.circle(screen, RED, circle, CIRCLE_RADIUS)  # Отрисовка красных кругов

    pygame.draw.rect(screen, BLUE, blue_rect)  # Отрисовка синего квадрата

    # Отрисовка сенсоров
    top_sensor = pygame.Rect(blue_rect.left, blue_rect.top - SENSOR_HEIGHT, blue_rect.width, SENSOR_HEIGHT)
    bottom_sensor = pygame.Rect(blue_rect.left, blue_rect.bottom, blue_rect.width, SENSOR_HEIGHT)
    pygame.draw.rect(screen, GRAY, top_sensor)
    pygame.draw.rect(screen, GRAY, bottom_sensor)

    # Отображение таймера удержания "пробел"
    if holding_space and remaining_hold_time > 0:
        timer_text = font.render(f"{remaining_hold_time:.1f}s", True, BLACK)
        screen.blit(timer_text, (blue_rect.right + 5, blue_rect.centery - timer_text.get_height() // 2))

    # Отрисовка кнопки "Auto Mode"
    pygame.draw.rect(screen, GRAY, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    button_text = font.render("Auto Mode", True, BLACK)
    button_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(button_text, button_rect)


running = True
clock = pygame.time.Clock()

moving_up = False  # Флаг движения вверх
moving_down = False  # Флаг движения вниз

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():  # Обработка событий Pygame
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not auto_mode:
            if event.key == pygame.K_UP:
                moving_up = True  # Включение движения вверх при нажатии стрелки "вверх"
            elif event.key == pygame.K_DOWN:
                moving_down = True  # Включение движения вниз при нажатии стрелки "вниз"
            elif event.key == pygame.K_SPACE:
                holding_space = True  # Включение удержания "пробел" при его нажатии
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                moving_up = False  # Выключение движения вверх при отпускании стрелки "вверх"
            elif event.key == pygame.K_DOWN:
                moving_down = False  # Выключение движения вниз при отпускании стрелки "вниз"
            elif event.key == pygame.K_SPACE:
                holding_space = False  # Выключение удержания "пробел" при его отпускании
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                auto_mode = not auto_mode  # Включение/выключение автоматического режима при нажатии на кнопку "Auto Mode"
                if auto_mode:
                    auto_clean()  # Запуск функции автоматической очистки

    if moving_up and blue_rect.top > 0:
        blue_rect.y -= MOVE_SPEED  # Движение синего квадрата вверх, если флаг движения вверх включен
    if moving_down and blue_rect.bottom < SCREEN_HEIGHT:
        blue_rect.y += MOVE_SPEED  # Движение синего квадрата вниз, если флаг движения вниз включен

    # Детектирование кругов в области сенсоров при удержании "пробел"
    top_sensor = pygame.Rect(blue_rect.left, blue_rect.top - SENSOR_HEIGHT, blue_rect.width, SENSOR_HEIGHT)
    bottom_sensor = pygame.Rect(blue_rect.left, blue_rect.bottom, blue_rect.width, SENSOR_HEIGHT)

    if holding_space:
        if current_time - last_remove_time >= REMOVE_DELAY:
            last_remove_time = current_time
            circles[:] = [circle for circle in circles if not circle_inside_blue_rect(circle)]
        elapsed_time = (current_time - start_press_time) / 1000
        remaining_hold_time -= elapsed_time
        start_press_time = current_time
        if remaining_hold_time <= 0:
            holding_space = False

    draw_game_screen()  # Отрисовка игрового экрана
    pygame.display.flip()  # Обновление экрана
    clock.tick(FPS)  # Ограничение частоты кадров

pygame.quit()  # Завершение работы Pygame
