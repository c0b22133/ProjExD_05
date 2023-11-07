
import sys
import pygame as pg

def main():
    pg.display.set_caption("弾幕ゲー")
    screen = pg.display.set_mode((600, 600))
    clock = pg.time.Clock()

    bg_img = pg.image.load("ex05/fig/background.png")
    tank = Tank(300, 500, "ex05/fig/player1.gif")
    sheild = pg.sprite.Group()

    tmr = 0
    x = 300  # タンクの初期 x 座標
    y = 500  # タンクの初期 y 座標

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            tank.move_left(10, 0)
        if keys[pg.K_d]:
            tank.move_right(10, 600)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB :
                    sheild.add(Shield(tank, 100, 300))

        screen.blit(bg_img, [0, 0])
        screen.blit(tank_img, [x, y])

        pg.display.update()
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()