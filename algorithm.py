import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Константы
SECTOR_SIZE = 80  # Размер одного квадрата-сектора
SECTOR_COUNT = 10  # Количество обычных секторов
TOTAL_SECTORS = SECTOR_COUNT + 1  # Общее количество секторов, включая зеленый
SCREEN_WIDTH = SECTOR_SIZE  # Ширина экрана равна ширине одного сектора
SCREEN_HEIGHT = SECTOR_SIZE * TOTAL_SECTORS  # Высота экрана равна высоте всех секторов
MINI_MAP_SCALE = 0.5  # Масштаб миникарты
MINI_MAP_WIDTH = int(SCREEN_WIDTH * MINI_MAP_SCALE)  # Ширина миникарты
MINI_MAP_HEIGHT = int(SCREEN_HEIGHT * MINI_MAP_SCALE)  # Высота миникарты
CIRCLE_RADIUS = 10  # Радиус красного круга
BLUE_SIZE = SECTOR_SIZE - 10  # Размер синего квадрата чуть меньше сектора
FPS = 60  # Частота обновления экрана
REMOVE_DELAY = 250  # Задержка удаления красных кругов в миллисекундах
BUTTON_WIDTH = 150  # Ширина кнопки
BUTTON_HEIGHT = 50  # Высота кнопки
BUTTON_X = SCREEN_WIDTH + 10  # Положение кнопки по оси x
BUTTON_Y = SCREEN_HEIGHT - BUTTON_HEIGHT - 10  # Положение кнопки по оси y

# Цвета
BLACK = (0, 0, 0)  # Черный
WHITE = (255, 255, 255)  # Белый
RED = (255, 0, 0)  # Красный
BLUE = (0, 0, 255)  # Синий
GREEN = (0, 255, 0)  # Зеленый
GRAY = (200, 200, 200)  # Серый

# Настройки экрана
WINDOW_WIDTH = SCREEN_WIDTH + MINI_MAP_WIDTH + BUTTON_WIDTH + 30  # Дополнительное пространство для миникарты и кнопки
screen = pygame.display.set_mode((WINDOW_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Game")

# Шрифт для отображения времени нажатия пробела и кнопки
font = pygame.font.Font(None, 24)

# Создание секторов с красными кругами
sectors = []
time_pressed = [0] * TOTAL_SECTORS  # Время нажатия пробела для каждого сектора
hold_times = [random.uniform(1, 3) for _ in range(SECTOR_COUNT)]  # Случайное время удержания пробела для каждого сектора
for i in range(SECTOR_COUNT):
    num_circles = random.randint(1, 5)  # Случайное количество кругов в секторе
    circles = []
    for _ in range(num_circles):
        x = random.randint(CIRCLE_RADIUS, SECTOR_SIZE - CIRCLE_RADIUS)  # Случайная позиция круга по оси x
        y = (i + 1) * SECTOR_SIZE + random.randint(CIRCLE_RADIUS, SECTOR_SIZE - CIRCLE_RADIUS)  # Случайная позиция круга по оси y
        circles.append((x, y))  # Добавление круга в список
    sectors.append(circles)  # Добавление сектора в список

# Синий квадрат в центре зеленого сектора
blue_rect = pygame.Rect((SECTOR_SIZE - BLUE_SIZE) // 2, (SECTOR_SIZE - BLUE_SIZE) // 2, BLUE_SIZE, BLUE_SIZE)
current_sector = 0  # Изначально синий квадрат находится в зеленом секторе
holding_space = False  # Флаг удержания пробела
last_remove_time = 0  # Время последнего удаления круга
start_press_time = 0  # Время начала нажатия пробела
auto_mode = False  # Флаг автоматического режима

def auto_clean_sectors(sector_index):
    """Рекурсивная функция для автоматического режима"""
    global current_sector, holding_space, start_press_time, last_remove_time

    if sector_index == SECTOR_COUNT:
        # Вернуться в зеленый сектор
        current_sector = 0
        blue_rect.y = current_sector * SECTOR_SIZE + (SECTOR_SIZE - BLUE_SIZE) // 2
        return

    # Переместить синий квадрат в нужный сектор
    current_sector = sector_index + 1
    blue_rect.y = current_sector * SECTOR_SIZE + (SECTOR_SIZE - BLUE_SIZE) // 2

    # Удерживать пробел на заданное количество времени
    hold_time = hold_times[sector_index]
    start_press_time = pygame.time.get_ticks()
    last_remove_time = start_press_time
    holding_space = True

    while sectors[sector_index] and (pygame.time.get_ticks() - start_press_time) / 1000 < hold_time:
        current_time = pygame.time.get_ticks()
        if current_time - last_remove_time >= REMOVE_DELAY:
            last_remove_time = current_time
            sectors[sector_index].pop()
        time_pressed[current_sector] += (current_time - start_press_time) / 1000
        start_press_time = current_time
        # Рисовать обновление на экране в автоматическом режиме
        draw_game_screen()
        pygame.display.flip()
        clock.tick(FPS)

    holding_space = False

    # Рекурсивно перейти к следующему сектору
    auto_clean_sectors(sector_index + 1)

def draw_game_screen():
    """Функция для рисования всех элементов на экране"""
    # Очистка экрана
    screen.fill(WHITE)

    # Рисование зеленого сектора
    pygame.draw.rect(screen, GREEN, (0, 0, SECTOR_SIZE, SECTOR_SIZE))

    # Рисование остальных секторов и красных кругов
    for i, circles in enumerate(sectors):
        pygame.draw.rect(screen, BLACK, (0, (i + 1) * SECTOR_SIZE, SECTOR_SIZE, SECTOR_SIZE), 1)
        for circle in circles:
            pygame.draw.circle(screen, RED, circle, CIRCLE_RADIUS)

    # Рисование синего квадрата
    pygame.draw.rect(screen, BLUE, blue_rect)

    # Рисование миникарты
    for i in range(TOTAL_SECTORS):
        mini_rect = pygame.Rect(SCREEN_WIDTH + 10, i * MINI_MAP_SCALE * SECTOR_SIZE, MINI_MAP_WIDTH, MINI_MAP_SCALE * SECTOR_SIZE)
        pygame.draw.rect(screen, GREEN if i == 0 else BLACK, mini_rect, 1)
        time_text = font.render(f"{time_pressed[i]:.1f}s", True, BLACK)
        text_rect = time_text.get_rect(center=(SCREEN_WIDTH + 10 + MINI_MAP_WIDTH // 2, i * MINI_MAP_SCALE * SECTOR_SIZE + MINI_MAP_SCALE * SECTOR_SIZE // 2))
        screen.blit(time_text, text_rect)

    # Рисование кнопки
    pygame.draw.rect(screen, GRAY, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    button_text = font.render("Auto Mode", True, BLACK)
    button_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(button_text, button_rect)

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()  # Текущее время в миллисекундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка на закрытие окна
            running = False
        elif event.type == pygame.KEYDOWN and not auto_mode:
            if event.key == pygame.K_UP and current_sector > 0:  # Перемещение вверх
                current_sector -= 1
                blue_rect.y = current_sector * SECTOR_SIZE + (SECTOR_SIZE - BLUE_SIZE) // 2
            elif event.key == pygame.K_DOWN and current_sector < SECTOR_COUNT:  # Перемещение вниз
                current_sector += 1
                blue_rect.y = current_sector * SECTOR_SIZE + (SECTOR_SIZE - BLUE_SIZE) // 2
            elif event.key == pygame.K_SPACE:  # Удержание пробела
                holding_space = True
                start_press_time = current_time
                last_remove_time = current_time
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:  # Отпускание пробела
                holding_space = False
                if current_sector > 0:
                    time_pressed[current_sector] += (current_time - start_press_time) / 1000  # Обновление времени нажатия
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                auto_mode = not auto_mode  # Переключение режима
                if auto_mode:
                    auto_clean_sectors(0)  # Запуск автоматического режима

    # Удаление красных кругов при удержании пробела
    if holding_space and current_sector > 0:
        if current_time - last_remove_time >= REMOVE_DELAY:  # Проверка задержки удаления
            last_remove_time = current_time
            if sectors[current_sector - 1]:  # Удаление круга из текущего сектора
                sectors[current_sector - 1].pop()

    # Очистка экрана и рисование всех элементов
    draw_game_screen()

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)  # Ограничение FPS

pygame.quit()  # Завершение Pygame


"""
Автоматический режим в данной игре реализован через рекурсивную функцию `auto_clean_sectors`, которая выполняет следующие шаги:

1. Инициализация:
   - При нажатии кнопки на экране активируется автоматический режим, и запускается функция `auto_clean_sectors`, начиная с сектора 0 (зелёного).

2. Проверка конца рекурсии:
   - Если текущий сектор равен количеству обычных секторов (`SECTOR_COUNT`), функция завершает работу и возвращает синий квадрат в зелёный сектор. Это условие прекращает дальнейшие рекурсивные вызовы.

3. Перемещение в нужный сектор:
   - Синий квадрат перемещается в центр следующего сектора. Координаты синего квадрата обновляются для отображения в новом секторе.

4. Удержание пробела:
   - Удержание пробела имитируется путём установки флага `holding_space` в `True`.
   - Начальное время удержания пробела (`start_press_time`) и время последнего удаления красного круга (`last_remove_time`) обновляются текущим временем.
   - Время удержания пробела (`hold_time`) для текущего сектора задаётся из заранее сгенерированного списка `hold_times`.

5. Удаление красных кругов:
   - Внутри цикла функция продолжает удалять красные круги, пока они существуют в текущем секторе и не истекло заданное время удержания пробела.
   - Время удержания пробела отслеживается путём сравнения текущего времени с `start_press_time`.
   - Красные круги удаляются с задержкой, заданной константой `REMOVE_DELAY`.

6. Обновление времени нажатия пробела:
   - Время, в течение которого удерживался пробел в каждом секторе, обновляется и сохраняется в массиве `time_pressed`.

7. Рекурсивный переход к следующему сектору:
   - После очистки текущего сектора функция рекурсивно вызывает саму себя с индексом следующего сектора.
   - Этот процесс продолжается до тех пор, пока не будут очищены все сектора или не достигнут конец списка секторов.

8. Возвращение в зелёный сектор:
   - После очистки всех секторов синий квадрат возвращается в зелёный сектор, завершая выполнение автоматического режима.

Основной принцип работы:
Автоматический режим циклично перемещает синий квадрат по всем секторам, удерживает пробел для удаления красных кругов и обновляет экран. Процесс повторяется рекурсивно, пока все секторы не будут очищены, после чего синий квадрат возвращается в начальный зелёный сектор.
"""