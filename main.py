import pygame as pg
import random
import time

# Настройки игры
FPS = 25
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
BLOCK_SIZE, CUP_HEIGHT, CUP_WIDTH = 20, 20, 10

# Отступы для игрового поля
SIDE_MARGIN = int((WINDOW_WIDTH - CUP_WIDTH * BLOCK_SIZE) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (CUP_HEIGHT * BLOCK_SIZE) - 5

# Цвета
COLORS = [
    (0, 0, 0),        # Черный (фон)
    (255, 0, 0),      # Красный
    (0, 255, 0),      # Зеленый
    (0, 0, 255),      # Синий
    (255, 255, 0),    # Желтый
    (255, 165, 0),    # Оранжевый
    (128, 0, 128),    # Фиолетовый
    (0, 255, 255)     # Голубой
]

# Фигуры
FIGURES = {
    'I': [['xxxx']],
    'O': [['xx', 'xx']],
    'T': [['xxx', ' x ']],
    'S': [[' xx', 'xx ']],
    'Z': [['xx ', ' xx']],
    'J': [['x  ', 'xxx']],
    'L': [['  x', 'xxx']]
}

def draw_cup(cup):
    """Отрисовка стакана."""
    pg.draw.rect(display_surf, COLORS[0], (SIDE_MARGIN, TOP_MARGIN, CUP_WIDTH * BLOCK_SIZE, CUP_HEIGHT * BLOCK_SIZE))
    for x in range(CUP_WIDTH):
        for y in range(CUP_HEIGHT):
            if cup[x][y]:
                pg.draw.rect(display_surf, COLORS[cup[x][y]],
                             (SIDE_MARGIN + x * BLOCK_SIZE, TOP_MARGIN + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_figure(figure, x, y, color):
    """Отрисовка фигуры."""
    for i, row in enumerate(figure):
        for j, cell in enumerate(row):
            if cell == 'x':
                pg.draw.rect(display_surf, COLORS[color],
                             (x + j * BLOCK_SIZE, y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(cup, figure, x, y):
    """Проверка столкновения фигуры с дном или другими фигурами."""
    for i, row in enumerate(figure):
        for j, cell in enumerate(row):
            if cell == 'x':
                cup_x = (x - SIDE_MARGIN) // BLOCK_SIZE + j
                cup_y = (y - TOP_MARGIN) // BLOCK_SIZE + i
                if cup_x < 0 or cup_x >= CUP_WIDTH or cup_y >= CUP_HEIGHT or cup[cup_x][cup_y]:
                    return True
    return False

def add_to_cup(cup, figure, x, y, color):
    """Добавление фигуры в стакан."""
    for i, row in enumerate(figure):
        for j, cell in enumerate(row):
            if cell == 'x':
                cup_x = (x - SIDE_MARGIN) // BLOCK_SIZE + j
                cup_y = (y - TOP_MARGIN) // BLOCK_SIZE + i
                cup[cup_x][cup_y] = color

def clear_lines(cup):
    """Удаление заполненных строк."""
    lines_to_clear = [i for i, row in enumerate(zip(*cup)) if all(row)]
    for i in lines_to_clear:
        del cup[i]
        cup.insert(0, [0 for _ in range(CUP_HEIGHT)])
    return len(lines_to_clear)

def calculate_speed(level):
    """Вычисление скорости падения фигур."""
    return 1.0 - (level * 0.1)

def draw_info(points, level):
    """Отрисовка информации о счете и уровне."""
    points_surf = font.render(f'Points: {points}', True, (255, 255, 255))
    level_surf = font.render(f'Level: {level}', True, (255, 255, 255))
    display_surf.blit(points_surf, (WINDOW_WIDTH - 150, 20))
    display_surf.blit(level_surf, (WINDOW_WIDTH - 150, 50))

def main():
    global display_surf, font
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption('Tetris Lite')
    font = pg.font.SysFont('Arial', 20)

    cup = [[0 for _ in range(CUP_HEIGHT)] for _ in range(CUP_WIDTH)]
    figure = random.choice(list(FIGURES.values()))
    next_figure = random.choice(list(FIGURES.values()))
    x, y = SIDE_MARGIN, TOP_MARGIN
    last_fall = time.time()
    points = 0
    level = 1
    color = random.randint(1, len(COLORS) - 1)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    if not check_collision(cup, figure, x - BLOCK_SIZE, y):
                        x -= BLOCK_SIZE
                elif event.key == pg.K_RIGHT:
                    if not check_collision(cup, figure, x + BLOCK_SIZE, y):
                        x += BLOCK_SIZE
                elif event.key == pg.K_DOWN:
                    if not check_collision(cup, figure, x, y + BLOCK_SIZE):
                        y += BLOCK_SIZE
                elif event.key == pg.K_UP:
                    rotated_figure = list(zip(*figure[::-1]))
                    if not check_collision(cup, rotated_figure, x, y):
                        figure = rotated_figure

        if time.time() - last_fall > calculate_speed(level):
            if not check_collision(cup, figure, x, y + BLOCK_SIZE):
                y += BLOCK_SIZE
            else:
                add_to_cup(cup, figure, x, y, color)
                cleared_lines = clear_lines(cup)
                points += cleared_lines * 100
                level = 1 + points // 500
                figure = next_figure
                next_figure = random.choice(list(FIGURES.values()))
                x, y = SIDE_MARGIN, TOP_MARGIN
                color = random.randint(1, len(COLORS) - 1)
                if check_collision(cup, figure, x, y):
                    break  # Игра окончена
            last_fall = time.time()

        display_surf.fill((0, 0, 0))
        draw_cup(cup)
        draw_figure(figure, x, y, color)
        draw_info(points, level)
        pg.display.update()
        fps_clock.tick(FPS)

    # Экран завершения игры
    display_surf.fill((0, 0, 0))
    game_over_surf = font.render('Game Over!', True, (255, 255, 255))
    display_surf.blit(game_over_surf, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))
    pg.display.update()
    time.sleep(2)
    pg.quit()

if __name__ == '__main__':
    main()