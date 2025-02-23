import pygame as pg

# Настройки игры
FPS = 25
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
BLOCK_SIZE, CUP_HEIGHT, CUP_WIDTH = 20, 20, 10

# Отступы для игрового поля
SIDE_MARGIN = int((WINDOW_WIDTH - CUP_WIDTH * BLOCK_SIZE) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (CUP_HEIGHT * BLOCK_SIZE) - 5

def draw_cup():
    """Отрисовка стакана."""
    pg.draw.rect(display_surf, (255, 255, 255), (SIDE_MARGIN, TOP_MARGIN, CUP_WIDTH * BLOCK_SIZE, CUP_HEIGHT * BLOCK_SIZE), 2)

def main():
    global display_surf
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption('Tetris Lite')

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return

        display_surf.fill((0, 0, 0))  # Черный фон
        draw_cup()
        pg.display.update()
        fps_clock.tick(FPS)

if __name__ == '__main__':
    main()