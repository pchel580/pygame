import pygame as pg
import random

# Настройки игры
FPS = 25
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
BLOCK_SIZE, CUP_HEIGHT, CUP_WIDTH = 20, 20, 10

# Отступы для игрового поля
SIDE_MARGIN = int((WINDOW_WIDTH - CUP_WIDTH * BLOCK_SIZE) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (CUP_HEIGHT * BLOCK_SIZE) - 5

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

def draw_cup():
    """Отрисовка стакана."""
    pg.draw.rect(display_surf, (255, 255, 255), (SIDE_MARGIN, TOP_MARGIN, CUP_WIDTH * BLOCK_SIZE, CUP_HEIGHT * BLOCK_SIZE), 2)

def draw_figure(figure, x, y):
    """Отрисовка фигуры."""
    for i, row in enumerate(figure):
        for j, cell in enumerate(row):
            if cell == 'x':
                pg.draw.rect(display_surf, (255, 0, 0), (x + j * BLOCK_SIZE, y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    global display_surf
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption('Tetris Lite')

    figure = random.choice(list(FIGURES.values()))
    x, y = SIDE_MARGIN, TOP_MARGIN

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    x -= BLOCK_SIZE
                elif event.key == pg.K_RIGHT:
                    x += BLOCK_SIZE
                elif event.key == pg.K_DOWN:
                    y += BLOCK_SIZE

        display_surf.fill((0, 0, 0))  # Черный фон
        draw_cup()
        draw_figure(figure, x, y)
        pg.display.update()
        fps_clock.tick(FPS)

if __name__ == '__main__':
    main()