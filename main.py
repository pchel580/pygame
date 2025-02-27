import pygame as pg
import random
import time
import sys
from pygame.constants import (
    K_SPACE, K_LEFT, K_RIGHT, K_DOWN, K_UP, K_RETURN, K_ESCAPE, QUIT, KEYUP, KEYDOWN
)

# Настройки игры
FPS = 25
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
BLOCK_SIZE, CUP_HEIGHT, CUP_WIDTH = 20, 20, 10

# Частота перемещения фигур в сторону и вниз
SIDE_FREQ, DOWN_FREQ = 0.15, 0.1

# Отступы для игрового поля
SIDE_MARGIN = int((WINDOW_WIDTH - CUP_WIDTH * BLOCK_SIZE) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (CUP_HEIGHT * BLOCK_SIZE) - 5

# Цвета
COLORS = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))  # синий, зеленый, красный, желтый
LIGHT_COLORS = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))  # светлые оттенки

WHITE, GRAY, BLACK = (255, 255, 255), (185, 185, 185), (0, 0, 0)
# Цвета
# Цвета
BG_COLOR = (236, 240, 241)  # Светло-серый фон
TEXT_COLOR = (44, 62, 80)  # Темно-синий текст
ACCENT_COLOR = (231, 76, 60)  # Красный акцент
BORDER_COLOR = (189, 195, 199)  # Серая рамка

# Размеры фигур
FIGURE_WIDTH, FIGURE_HEIGHT = 5, 5
EMPTY = 'o'

# Фигуры
FIGURES = {
    'S': [['ooooo', 'ooooo', 'ooxxo', 'oxxoo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxxo', 'oooxo', 'ooooo']],
    'Z': [['ooooo', 'ooooo', 'oxxoo', 'ooxxo', 'ooooo'],
          ['ooooo', 'ooxoo', 'oxxoo', 'oxooo', 'ooooo']],
    'J': [['ooooo', 'oxooo', 'oxxxo', 'ooooo', 'ooooo'],
          ['ooooo', 'ooxxo', 'ooxoo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'oooxo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxoo', 'oxxoo', 'ooooo']],
    'L': [['ooooo', 'oooxo', 'oxxxo', 'ooooo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxoo', 'ooxxo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'oxooo', 'ooooo'],
          ['ooooo', 'oxxoo', 'ooxoo', 'ooxoo', 'ooooo']],
    'I': [['ooxoo', 'ooxoo', 'ooxoo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'xxxxo', 'ooooo', 'ooooo']],
    'O': [['ooooo', 'ooooo', 'oxxoo', 'oxxoo', 'ooooo']],
    'T': [['ooooo', 'ooxoo', 'oxxxo', 'ooooo', 'ooooo'],
          ['ooooo', 'ooxoo', 'ooxxo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooooo', 'oxxxo', 'ooxoo', 'ooooo'],
          ['ooooo', 'ooxoo', 'oxxoo', 'ooxoo', 'ooooo']]
}


def pause_screen():
    """Отрисовка экрана паузы."""
    pause = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA)
    pause.fill((44, 62, 80, 200))  # Полупрозрачный темно-синий
    display_surf.blit(pause, (0, 0))

    # Текст "Пауза"
    pause_surf = big_font.render('Pause', True, ACCENT_COLOR)
    pause_rect = pause_surf.get_rect()
    pause_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    display_surf.blit(pause_surf, pause_rect)


def main():
    """Основная функция игры."""
    global fps_clock, display_surf, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Загрузка шрифтов
    basic_font = pg.font.SysFont('Arial', 20)
    big_font = pg.font.SysFont('Verdana', 45, bold=True)
    pg.display.set_caption('Just Tetris')
    show_text('Just Tetris')
    while True:
        run_tetris()
        pause_screen()
        show_text('Игра закончена')


def run_tetris():
    """Запуск игры Тетрис."""
    cup = create_empty_cup()
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_down = False
    going_left = False
    going_right = False
    points = 0
    level, fall_speed = calculate_speed(points)
    falling_fig = get_new_figure()
    next_fig = get_new_figure()

    while True:
        if falling_fig is None:
            falling_fig = next_fig
            next_fig = get_new_figure()
            last_fall = time.time()

            if not check_position(cup, falling_fig):
                return
        quit_game()
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pause_screen()
                    show_text('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:
                if event.key == K_LEFT and check_position(cup, falling_fig, adjX=-1):
                    falling_fig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and check_position(cup, falling_fig, adjX=1):
                    falling_fig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                elif event.key == K_UP:
                    falling_fig['rotation'] = (falling_fig['rotation'] + 1) % len(FIGURES[falling_fig['shape']])
                    if not check_position(cup, falling_fig):
                        falling_fig['rotation'] = (falling_fig['rotation'] - 1) % len(FIGURES[falling_fig['shape']])

                elif event.key == K_DOWN:
                    going_down = True
                    if check_position(cup, falling_fig, adjY=1):
                        falling_fig['y'] += 1
                    last_move_down = time.time()

                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, CUP_HEIGHT):
                        if not check_position(cup, falling_fig, adjY=i):
                            break
                    falling_fig['y'] += i - 1

        if (going_left or going_right) and time.time() - last_side_move > SIDE_FREQ:
            if going_left and check_position(cup, falling_fig, adjX=-1):
                falling_fig['x'] -= 1
            elif going_right and check_position(cup, falling_fig, adjX=1):
                falling_fig['x'] += 1
            last_side_move = time.time()

        if going_down and time.time() - last_move_down > DOWN_FREQ and check_position(cup, falling_fig, adjY=1):
            falling_fig['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:
            if not check_position(cup, falling_fig, adjY=1):
                add_to_cup(cup, falling_fig)
                points += clear_completed(cup)
                level, fall_speed = calculate_speed(points)
                falling_fig = None
            else:
                falling_fig['y'] += 1
                last_fall = time.time()

        display_surf.fill(BG_COLOR)
        draw_title()
        draw_cup(cup)
        draw_info(points, level)
        draw_next_figure(next_fig)
        if falling_fig is not None:
            draw_figure(falling_fig)
        pg.display.update()
        fps_clock.tick(FPS)


def create_text_objects(text, font, color):
    """Создание текстового объекта."""
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def stop_game():
    """Завершение игры."""
    pg.quit()
    sys.exit()


def check_keys():
    """Проверка нажатия клавиш."""
    quit_game()
    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def show_text(text):
    """Отображение текста на экране."""
    title_surf, title_rect = create_text_objects(text, big_font, ACCENT_COLOR)
    title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
    display_surf.blit(title_surf, title_rect)

    press_key_surf, press_key_rect = create_text_objects('Press any key', basic_font, TEXT_COLOR)
    press_key_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
    display_surf.blit(press_key_surf, press_key_rect)

    while check_keys() is None:
        pg.display.update()
        fps_clock.tick()


def quit_game():
    """Выход из игры."""
    for event in pg.event.get(QUIT):
        stop_game()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stop_game()
        pg.event.post(event)


def calculate_speed(points):
    """Вычисление скорости падения фигур."""
    level = int(points / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed


def get_new_figure():
    """Создание новой фигуры."""
    shape = random.choice(list(FIGURES.keys()))
    new_figure = {
        'shape': shape,
        'rotation': random.randint(0, len(FIGURES[shape]) - 1),
        'x': int(CUP_WIDTH / 2) - int(FIGURE_WIDTH / 2),
        'y': -2,
        'color': random.randint(0, len(COLORS) - 1)
    }
    return new_figure


def add_to_cup(cup, figure):
    """Добавление фигуры в стакан."""
    for x in range(FIGURE_WIDTH):
        for y in range(FIGURE_HEIGHT):
            if FIGURES[figure['shape']][figure['rotation']][y][x] != EMPTY:
                cup[x + figure['x']][y + figure['y']] = figure['color']


def create_empty_cup():
    """Создание пустого стакана."""
    cup = []
    for i in range(CUP_WIDTH):
        cup.append([EMPTY] * CUP_HEIGHT)
    return cup


def is_in_cup(x, y):
    """Проверка нахождения в пределах стакана."""
    return 0 <= x < CUP_WIDTH and y < CUP_HEIGHT


def check_position(cup, figure, adjX=0, adjY=0):
    """Проверка позиции фигуры."""
    for x in range(FIGURE_WIDTH):
        for y in range(FIGURE_HEIGHT):
            above_cup = y + figure['y'] + adjY < 0
            if above_cup or FIGURES[figure['shape']][figure['rotation']][y][x] == EMPTY:
                continue
            if not is_in_cup(x + figure['x'] + adjX, y + figure['y'] + adjY):
                return False
            if cup[x + figure['x'] + adjX][y + figure['y'] + adjY] != EMPTY:
                return False
    return True


def is_completed(cup, y):
    """Проверка заполненности ряда."""
    for x in range(CUP_WIDTH):
        if cup[x][y] == EMPTY:
            return False
    return True


def clear_completed(cup):
    """Очистка заполненных рядов."""
    removed_lines = 0
    y = CUP_HEIGHT - 1
    while y >= 0:
        if is_completed(cup, y):
            for push_down_y in range(y, 0, -1):
                for x in range(CUP_WIDTH):
                    cup[x][push_down_y] = cup[x][push_down_y - 1]
            for x in range(CUP_WIDTH):
                cup[x][0] = EMPTY
            removed_lines += 1
        else:
            y -= 1
    return removed_lines


def convert_coords(block_x, block_y):
    """Конвертация координат."""
    return (SIDE_MARGIN + (block_x * BLOCK_SIZE)), (TOP_MARGIN + (block_y * BLOCK_SIZE))


def draw_block(block_x, block_y, color, pixelx=None, pixely=None):
    """Отрисовка блока в минималистичном стиле."""
    if color == EMPTY:
        return
    if pixelx is None and pixely is None:
        pixelx, pixely = convert_coords(block_x, block_y)

    # Рисуем простой квадрат без закруглений и градиентов
    pg.draw.rect(display_surf, COLORS[color], (pixelx, pixely, BLOCK_SIZE, BLOCK_SIZE))

    # Добавляем тонкую рамку для разделения блоков
    pg.draw.rect(display_surf, (200, 200, 200), (pixelx, pixely, BLOCK_SIZE, BLOCK_SIZE), 1)


def draw_cup(cup):
    """Отрисовка игрового поля."""
    # Фон игрового поля
    pg.draw.rect(display_surf, BG_COLOR, (SIDE_MARGIN, TOP_MARGIN, BLOCK_SIZE * CUP_WIDTH, BLOCK_SIZE * CUP_HEIGHT))

    # Рамка игрового поля
    pg.draw.rect(display_surf, BORDER_COLOR,
                 (SIDE_MARGIN - 4, TOP_MARGIN - 4, (CUP_WIDTH * BLOCK_SIZE) + 8, (CUP_HEIGHT * BLOCK_SIZE) + 8), 3)

    # Отрисовка блоков
    for x in range(CUP_WIDTH):
        for y in range(CUP_HEIGHT):
            draw_block(x, y, cup[x][y])


def draw_title():
    """Отрисовка заголовка."""
    title_surf = big_font.render('Just Tetris', True, ACCENT_COLOR)
    title_rect = title_surf.get_rect()
    title_rect.topleft = (20, 20)  # Расположение в верхнем левом углу
    display_surf.blit(title_surf, title_rect)


def draw_info(points, level):
    """Отрисовка информации о счете и уровне."""
    # Очки
    points_surf = basic_font.render(f'Score: {points}', True, TEXT_COLOR)
    points_rect = points_surf.get_rect()
    points_rect.topleft = (20, 100)
    display_surf.blit(points_surf, points_rect)

    # Уровень
    level_surf = basic_font.render(f'Level: {level}', True, TEXT_COLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (20, 130)
    display_surf.blit(level_surf, level_rect)

    # Управление
    controls_surf = basic_font.render('Controls: ← → ↓ ↑', True, TEXT_COLOR)
    controls_rect = controls_surf.get_rect()
    controls_rect.topleft = (20, WINDOW_HEIGHT - 60)
    display_surf.blit(controls_surf, controls_rect)


def draw_figure(figure, pixelx=None, pixely=None):
    """Отрисовка фигуры."""
    figure_to_draw = FIGURES[figure['shape']][figure['rotation']]
    if pixelx is None and pixely is None:
        pixelx, pixely = convert_coords(figure['x'], figure['y'])

    for x in range(FIGURE_WIDTH):
        for y in range(FIGURE_HEIGHT):
            if figure_to_draw[y][x] != EMPTY:
                draw_block(None, None, figure['color'], pixelx + (x * BLOCK_SIZE), pixely + (y * BLOCK_SIZE))


def draw_next_figure(figure):
    """Отрисовка следующей фигуры."""
    next_surf = basic_font.render('Next:', True, TEXT_COLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOW_WIDTH - 150, 100)
    display_surf.blit(next_surf, next_rect)
    draw_figure(figure, pixelx=WINDOW_WIDTH - 150, pixely=150)


if __name__ == '__main__':
    main()
