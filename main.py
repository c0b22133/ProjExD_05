import sys
import pygame as pg
from pygame.sprite import AbstractGroup
import random
import time

WIDTH = 600  # タンクの初期 x 座標
HEIGHT = 600  # タンクの初期 y 座標

class Enemy(pg.sprite.Sprite):

    imgs = [pg.image.load(f"ex05/fig/alien{i}.png") for i in range(1, 3)]

    def __init__(self,):
        super().__init__()
        self.image = random.choice(__class__.imgs)
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(0, WIDTH), 0
        self.vy = +6
        self.bound = random.randint(50, 200)
        self.state = "down"
        self.interaval = random.randint(50, 300)
        self.created_time = time.time()

    def update(self):
        if self.rect.centery > self.bound:
            self.vy = 0
            self.state = "stop"
        self.rect.centery += self.vy
        if self.is_expired(5):
            self.reset()
    def is_expired(self, duration):
        return time.time() - self.created_time > duration
    def reset(self):
        self.rect.center = random.randint(0, WIDTH), 0
        self.vy = +6
        self.bound = random.randint(50, 200)
        self.created_time = time.time()



def main():
    pg.display.set_caption("弾幕ゲー")
    screen = pg.display.set_mode((600, 600))
    clock = pg.time.Clock()

    bg_img = pg.image.load("ex05/fig/background.png")
    tank_img = pg.image.load("ex05/fig/player1.gif")
    emys = pg.sprite.Group()

    tmr = 0
    x = 300  # タンクの初期 x 座標
    y = 500  # タンクの初期 y 座標
    count = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            


        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            x -= 10  # 左に移動
            if x < 0:  # 画面の左端を超えないように
                x = 0
        if keys[pg.K_d]:
            x += 10  # 右に移動
            if x > 600 - tank_img.get_width():
                x = 600 - tank_img.get_width()


        if count < 5:
            emys.add(Enemy())


        screen.blit(bg_img, [0, 0])
        screen.blit(tank_img, [x, y])

        emys.update()
        emys.draw(screen)
        pg.display.update()
        count+=1
        tmr += 1
        clock.tick(100)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
