import pygame  # Импортируем библиотеку Pygame для создания игр и работы с графикой
import random  # Импортируем библиотеку random для генерации случайных чисел

# Инициализация Pygame
pygame.init()  # Инициализация всех модулей Pygame

# Константы
SCREEN_WIDTH = 50  # Ширина игрового поля
SCREEN_HEIGHT = 600  # Высота игрового поля
BLUE_SIZE = 50  # Размер синего квадрата
CIRCLE_RADIUS = 5  # Радиус красного круга
FPS = 60  # Частота обновления экрана (кадров в секунду)
REMOVE_DELAY = 500  # Задержка удаления красных кругов в миллисекундах
BUTTON_WIDTH = 150  # Ширина кнопки
BUTTON_HEIGHT = 50  # Высота кнопки
BUTTON_X = SCREEN_WIDTH + 10  # Положение кнопки по оси x
BUTTON_Y = SCREEN_HEIGHT - BUTTON_HEIGHT - 10  # Положение кнопки по оси y
MOVE_SPEED = 3  # Скорость перемещения синего квадрата
SENSOR_HEIGHT = 5  # Высота сенсоров

# Цвета
BLACK = (0, 0, 0)  # Черный цвет
WHITE = (255, 255, 255)  # Белый цвет
RED = (255, 0, 0)  # Красный цвет
BLUE = (0, 0, 255)  # Синий цвет
GRAY = (200, 200, 200)  # Серый цвет

# Настройки экрана
WINDOW_WIDTH = SCREEN_WIDTH + BUTTON_WIDTH + 30  # Ширина окна с дополнительным пространством для кнопки
screen = pygame.display.set_mode((WINDOW_WIDTH, SCREEN_HEIGHT))  # Создаем окно игры с заданными размерами
pygame.display.set_caption("Cleaning System Model")  # Устанавливаем заголовок окна

# Шрифт для отображения текста
font = pygame.font.Font(None, 24)  # Создаем объект шрифта с размером 24

# Создание красных кругов
circles = []  # Список для хранения кругов
for _ in range(50):  # Количество красных кругов
    x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)  # Случайная позиция круга по оси x
    y = random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS)  # Случайная позиция круга по оси y
    circles.append((x, y))  # Добавление круга в список

# Синий квадрат в начальной позиции
blue_rect = pygame.Rect((SCREEN_WIDTH - BLUE_SIZE) // 2, 0, BLUE_SIZE, BLUE_SIZE)  # Создание синего квадрата
holding_space = False  # Флаг удержания пробела
last_remove_time = 0  # Время последнего удаления круга
start_press_time = 0  # Время начала нажатия пробела
auto_mode = False  # Флаг автоматического режима
remaining_hold_time = 0  # Оставшееся время удержания

# Флаг направления движения
direction = "down"


def auto_clean():
    """Функция для автоматического режима"""
    global holding_space, start_press_time, last_remove_time, remaining_hold_time

    for y in range(0, SCREEN_HEIGHT, BLUE_SIZE):
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
                blue_rect.y -= MOVE_SPEED
                if blue_rect.y <= target_y:
                    blue_rect.y = target_y
                    reached_target = True

            # Проверка сенсоров во время движения
            top_sensor = pygame.Rect(blue_rect.left, blue_rect.top - SENSOR_HEIGHT, blue_rect.width, SENSOR_HEIGHT)
            bottom_sensor = pygame.Rect(blue_rect.left, blue_rect.bottom, blue_rect.width, SENSOR_HEIGHT)
            circle_count += sum(circle_inside_sensor(top_sensor, circle) for circle in circles)
            circle_count += sum(circle_inside_sensor(bottom_sensor, circle) for circle in circles)

            draw_game_screen()
            pygame.display.flip()
            clock.tick(FPS)

        hold_and_clean(circle_count)

def hold_and_clean(circle_count):
    """Удержание пробела для очистки кругов"""
    global holding_space, start_press_time, last_remove_time, remaining_hold_time
    if circle_count > 0:
        hold_time = circle_count * 1  # 1 секунда за каждый круг
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
    screen.fill(WHITE)  # Заполнение экрана белым цветом

    # Рисование красных кругов
    for circle in circles:
        pygame.draw.circle(screen, RED, circle, CIRCLE_RADIUS)  # Рисуем красные круги

    # Рисование синего квадрата
    pygame.draw.rect(screen, BLUE, blue_rect)  # Рисуем синий квадрат

    # Рисование сенсоров
    top_sensor = pygame.Rect(blue_rect.left, blue_rect.top - SENSOR_HEIGHT, blue_rect.width, SENSOR_HEIGHT)
    bottom_sensor = pygame.Rect(blue_rect.left, blue_rect.bottom, blue_rect.width, SENSOR_HEIGHT)
    pygame.draw.rect(screen, GRAY, top_sensor)  # Рисуем верхний сенсор
    pygame.draw.rect(screen, GRAY, bottom_sensor)  # Рисуем нижний сенсор

    # Отображение таймера, если удерживается пробел
    if holding_space and remaining_hold_time > 0:
        timer_text = font.render(f"{remaining_hold_time:.1f}s", True, BLACK)  # Отображение оставшегося времени
        screen.blit(timer_text, (blue_rect.right + 5, blue_rect.centery - timer_text.get_height() // 2))  # Отображение текста на экране

    # Рисование кнопки
    pygame.draw.rect(screen, GRAY, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))  # Рисуем кнопку
    button_text = font.render("Auto Mode", True, BLACK)  # Текст кнопки
    button_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))  # Центрирование текста кнопки
    screen.blit(button_text, button_rect)  # Отображение текста кнопки

# Основной игровой цикл
running = True  # Флаг для работы основного цикла игры
clock = pygame.time.Clock()  # Создание объекта для отслеживания времени

moving_up = False  # Флаг перемещения вверх
moving_down = False  # Флаг перемещения вниз

while running:
    current_time = pygame.time.get_ticks()  # Текущее время в миллисекундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка на закрытие окна
            running = False  # Завершение основного цикла
        elif event.type == pygame.KEYDOWN and not auto_mode:
            if event.key == pygame.K_UP:  # Начало перемещения вверх
                moving_up = True
            elif event.key == pygame.K_DOWN:  # Начало перемещения вниз
                moving_down = True
            elif event.key == pygame.K_SPACE:  # Удержание пробела
                holding_space = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:  # Остановка перемещения вверх
                moving_up = False
            elif event.key == pygame.K_DOWN:  # Остановка перемещения вниз
                moving_down = False
            elif event.key == pygame.K_SPACE:  # Отпускание пробела
                holding_space = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos  # Позиция мыши
            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                auto_mode = not auto_mode  # Переключение режима
                if auto_mode:
                    auto_clean()  # Запуск автоматического режима

    # Плавное перемещение синего квадрата
    if moving_up and blue_rect.top > 0:
        blue_rect.y -= MOVE_SPEED  # Перемещение вверх
    if moving_down and blue_rect.bottom < SCREEN_HEIGHT:
        blue_rect.y += MOVE_SPEED  # Перемещение вниз

    # Сенсоры
    top_sensor = pygame.Rect(blue_rect.left, blue_rect.top - SENSOR_HEIGHT, blue_rect.width, SENSOR_HEIGHT)
    bottom_sensor = pygame.Rect(blue_rect.left, blue_rect.bottom, blue_rect.width, SENSOR_HEIGHT)

    # Удаление красных кругов при удержании пробела
    if holding_space:
        if current_time - last_remove_time >= REMOVE_DELAY:  # Проверка задержки удаления
            last_remove_time = current_time
            circles[:] = [circle for circle in circles if not circle_inside_blue_rect(circle)]  # Удаление кругов внутри синего квадрата
        elapsed_time = (current_time - start_press_time) / 1000  # Вычисление прошедшего времени
        remaining_hold_time -= elapsed_time  # Обновление оставшегося времени удержания
        start_press_time = current_time
        if remaining_hold_time <= 0:
            holding_space = False  # Сброс флага удержания пробела

    # Очистка экрана и рисование всех элементов
    draw_game_screen()

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)  # Ограничение FPS

pygame.quit()  # Завершение Pygame