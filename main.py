import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SECTOR_SIZE = 80  # Размер одного квадрата-сектора
SECTOR_COUNT = 10  # Количество обычных секторов
TOTAL_SECTORS = SECTOR_COUNT + 1  # Общее количество секторов, включая зеленый
SCREEN_WIDTH = SECTOR_SIZE  # Ширина экрана равна ширине одного сектора
SCREEN_HEIGHT = SECTOR_SIZE * TOTAL_SECTORS  # Высота экрана равна высоте всех секторов
MINI_MAP_SCALE = 0.4  # Масштаб миникарты
MINI_MAP_WIDTH = int(SCREEN_WIDTH * MINI_MAP_SCALE)  # Ширина миникарты
MINI_MAP_HEIGHT = int(SCREEN_HEIGHT * MINI_MAP_SCALE)  # Высота миникарты
CIRCLE_RADIUS = 10  # Радиус красного круга
BLUE_SIZE = SECTOR_SIZE - 10  # Размер синего квадрата чуть меньше сектора
FPS = 60  # Частота обновления экрана
REMOVE_DELAY = 250  # Задержка удаления красных кругов в миллисекундах

# Цвета
BLACK = (0, 0, 0)  # Черный
WHITE = (255, 255, 255)  # Белый
RED = (255, 0, 0)  # Красный
BLUE = (0, 0, 255)  # Синий
GREEN = (0, 255, 0)  # Зеленый

# Настройки экрана
WINDOW_WIDTH = SCREEN_WIDTH + MINI_MAP_WIDTH + 20  # Дополнительное пространство для миникарты
screen = pygame.display.set_mode((WINDOW_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Game")

# Шрифт для отображения времени нажатия пробела
font = pygame.font.Font(None, 24)

# Создание секторов с красными кругами
sectors = []
time_pressed = [0] * TOTAL_SECTORS  # Время нажатия пробела для каждого сектора
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

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()  # Текущее время в миллисекундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка на закрытие окна
            running = False
        elif event.type == pygame.KEYDOWN:
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

    # Удаление красных кругов при удержании пробела
    if holding_space and current_sector > 0:
        if current_time - last_remove_time >= REMOVE_DELAY:  # Проверка задержки удаления
            last_remove_time = current_time
            if sectors[current_sector - 1]:  # Удаление круга из текущего сектора
                sectors[current_sector - 1].pop()

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

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)  # Ограничение FPS

pygame.quit()  # Завершение Pygame
