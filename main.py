import sys
import pygame as pg
import time
import random


class Tank:
    def __init__(self, x,y, image_path):
        self.x = x
        self.y = y
        self.image = pg.image.load(image_path)
        # self.rect = self.image.get_rect()
        # self.rect.center = x, y

    def move_left(self, distance, min_x):
        self.x -= distance
        if self.x < min_x:
            self.x = min_x

    def move_right(self, distance, max_x):
        self.x += distance
        if self.x > max_x - self.image.get_width():
            self.x = max_x - self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, [self.x, self.y])

class Shield(pg.sprite.Sprite):
    """
    tabキーを押すと重力バリアが発動する
    """
    def __init__(self, tank:Tank,  size: int ,life: int):
        super().__init__()
        self.tank = tank
        self.image = pg.Surface((2*size, 2*size))
        self.image.set_alpha(50)
        pg.draw.circle(self.image, (1, 0, 0), (size, size), size)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.tank.x + self.tank.image.get_width() / 2
        self.rect.centery = self.tank.y
        self.life = life

    def update(self):
        """
        発動してからlifeがゼロになるまで発動し、ゼロになったらkillされる
        """
        self.rect.centerx = self.tank.x + self.tank.image.get_width() / 2
        self.rect.centery = self.tank.y
        self.life -= 1
        if self.life < 0:
            self.kill()


def main():
    pg.display.set_caption("弾幕ゲー")
    screen = pg.display.set_mode((600, 600))
    clock = pg.time.Clock()

    bg_img = pg.image.load("ex05/fig/background.png")
    tank = Tank(300, 500, "ex05/fig/player1.gif")
    sheild = pg.sprite.Group()

    obstacles = []
    next_obstacle_time = time.time() + random.randint(1, 3)

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
        tank.draw(screen)

        sheild.update()
        sheild.draw(screen)
        pg.display.update()
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
