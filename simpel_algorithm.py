import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы для экрана и объектов
SCREEN_WIDTH = 50  # Ширина экрана
SCREEN_HEIGHT = 900  # Высота экрана
BLUE_SIZE = 50  # Размер синего квадрата
CIRCLE_RADIUS = 5  # Радиус красных кругов
FPS = 60  # Частота кадров в секунду
REMOVE_DELAY = 100  # Задержка перед удалением кругов (в миллисекундах)
BUTTON_WIDTH = 150  # Ширина кнопки "Auto Mode"
BUTTON_HEIGHT = 50  # Высота кнопки "Auto Mode"
BUTTON_X = SCREEN_WIDTH + 10  # Положение кнопки "Auto Mode" по X
BUTTON_Y = SCREEN_HEIGHT - BUTTON_HEIGHT - 10  # Положение кнопки "Auto Mode" по Y
MOVE_SPEED = 5  # Скорость перемещения синего квадрата
DAMAGE_PER_TICK = 2  # Количество урона, наносимого за тик

# Цвета
BLACK = (0, 0, 0)  # Черный цвет
WHITE = (255, 255, 255)  # Белый цвет
RED = (255, 0, 0)  # Красный цвет
BLUE = (0, 0, 255)  # Синий цвет
GRAY = (200, 200, 200)  # Серый цвет

# Настройки экрана
WINDOW_WIDTH = SCREEN_WIDTH + BUTTON_WIDTH + 100  # Ширина окна с учетом кнопки и области ввода
screen = pygame.display.set_mode((WINDOW_WIDTH, SCREEN_HEIGHT))  # Создание экрана Pygame
pygame.display.set_caption("Cleaning System Model")  # Установка заголовка окна

# Шрифт для текста
font = pygame.font.Font(None, 24)  # Шрифт для отображения текста

# Создание красных кругов с добавлением здоровья (в миллисекундах)
circles = []
for _ in range(75):
    x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)
    y = random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS)
    health = random.randint(500, 1000)  # Здоровье (время для уборки) от 1 до 5 секунд
    circles.append([x, y, health])

# Начальное положение синего квадрата
blue_rect = pygame.Rect((SCREEN_WIDTH - BLUE_SIZE) // 2, 0, BLUE_SIZE, BLUE_SIZE)
auto_mode = False  # Флаг автоматического режима
move_up = False  # Флаг движения вверх
move_down = False  # Флаг движения вниз
last_remove_time = pygame.time.get_ticks()  # Время последнего удаления круга

# Переменные для ввода количества циклов
input_active = False  # Флаг активности ввода текста
input_box = pygame.Rect(BUTTON_X, BUTTON_Y - 60, BUTTON_WIDTH, 40)  # Прямоугольник для ввода текста
input_text = '1'  # Текст по умолчанию для ввода
auto_mode_cycles = int(input_text) * 2  # Количество циклов для автоматического режима

def auto_move(cycles):
    global blue_rect, MOVE_SPEED, auto_mode, last_remove_time
    direction = 1  # Направление движения: 1 - вниз, -1 - вверх
    cycle_count = 0  # Счетчик циклов

    while auto_mode and cycle_count < cycles:
        blue_rect.y += MOVE_SPEED * direction  # Перемещение синего квадрата
        if blue_rect.top <= 0 or blue_rect.bottom >= SCREEN_HEIGHT:
            direction *= -1  # Смена направления при достижении края экрана
            cycle_count += 1  # Увеличение счетчика циклов

        clean_circles()  # Очистка кругов

        draw_game_screen()  # Отрисовка игрового экрана
        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)  # Ограничение частоты кадров

def clean_circles():
    global circles, last_remove_time
    current_time = pygame.time.get_ticks()  # Получение текущего времени

    for circle in circles[:]:
        x, y, health = circle
        if blue_rect.collidepoint(x, y):  # Проверка столкновения синего квадрата с кругом
            health -= DAMAGE_PER_TICK * (current_time - last_remove_time)  # Уменьшение здоровья круга
            if health <= 0:
                circles.remove(circle)  # Удаление круга при нулевом здоровье
            else:
                circle[2] = health  # Обновление здоровья круга

    last_remove_time = current_time  # Обновление времени последнего удаления круга

def draw_game_screen():
    screen.fill(WHITE)  # Заполнение экрана белым цветом

    for circle in circles:
        pygame.draw.circle(screen, RED, (circle[0], circle[1]), CIRCLE_RADIUS)  # Отрисовка красных кругов

    pygame.draw.rect(screen, BLUE, blue_rect)  # Отрисовка синего квадрата

    pygame.draw.rect(screen, GRAY, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))  # Отрисовка кнопки
    button_text = font.render("Auto Mode", True, BLACK)  # Текст на кнопке
    button_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(button_text, button_rect)  # Отображение текста на кнопке

    pygame.draw.rect(screen, GRAY, input_box, 2)  # Отрисовка прямоугольника ввода
    input_text_surface = font.render(input_text, True, BLACK)  # Текст в прямоугольнике ввода
    screen.blit(input_text_surface, (input_box.x + 5, input_box.y + 5))  # Отображение текста в прямоугольнике ввода
    input_box.w = max(50, input_text_surface.get_width() + 10)  # Обновление ширины прямоугольника ввода

running = True  # Флаг работы игрового цикла
clock = pygame.time.Clock()  # Объект для ограничения частоты кадров

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка события выхода
            running = False
        elif event.type == pygame.KEYDOWN:  # Проверка нажатия клавиши
            if event.key == pygame.K_UP:  # Нажата клавиша вверх
                move_up = True
                move_down = False
            elif event.key == pygame.K_DOWN:  # Нажата клавиша вниз
                move_down = True
                move_up = False
            elif event.key == pygame.K_RETURN:  # Нажата клавиша ввода
                if input_active:
                    try:
                        auto_mode_cycles = int(input_text) * 2  # Обновление количества циклов
                    except ValueError:
                        auto_mode_cycles = 1 * 2  # Значение по умолчанию в случае ошибки преобразования
            elif input_active:
                if event.key == pygame.K_BACKSPACE:  # Нажата клавиша Backspace
                    input_text = input_text[:-1]  # Удаление последнего символа в тексте
                else:
                    input_text += event.unicode  # Добавление символа в текст
        elif event.type == pygame.KEYUP:  # Проверка отпускания клавиши
            if event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Проверка нажатия кнопки мыши
            mouse_x, mouse_y = event.pos
            if input_box.collidepoint(event.pos):  # Проверка попадания в прямоугольник ввода
                input_active = not input_active  # Переключение состояния активности ввода
            else:
                input_active = False  # Деактивация ввода

            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                auto_mode = not auto_mode  # Переключение автоматического режима
                if auto_mode:
                    auto_move(auto_mode_cycles)  # Запуск автоматического перемещения

    if move_up and blue_rect.top > 0:  # Перемещение вверх
        blue_rect.y -= MOVE_SPEED
    if move_down and blue_rect.bottom < SCREEN_HEIGHT:  # Перемещение вниз
        blue_rect.y += MOVE_SPEED

    if not auto_mode:
        clean_circles()  # Очистка кругов при ручном режиме

    draw_game_screen()  # Отрисовка игрового экрана
    pygame.display.flip()  # Обновление экрана
    clock.tick(FPS)  # Ограничение частоты кадров

pygame.quit()  # Завершение работы Pygame
