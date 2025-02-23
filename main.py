import pygame as pg

# Настройки игры
FPS = 25
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500

def main():
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
        pg.display.update()
        fps_clock.tick(FPS)

if __name__ == '__main__':
    main()