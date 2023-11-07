import math
import random
import sys
import time
from typing import Any
import pygame as pg

WIDTH = 900
HEIGHT = 900


def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（爆弾，こうかとん，ビーム）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

class Tank:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pg.image.load(image_path)

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


class Beam(pg.sprite.Sprite):
    """
    ビームに関するクラス
    """
    def __init__(self, tank: Tank, angle: float):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/beam.png"), angle, 2.0)
        self.vx = math.cos(math.radians(angle))
        self.vy = -math.sin(math.radians(angle))
        self.rect = self.image.get_rect()
        self.rect.centerx = tank.x + tank.image.get_width()/2
        self.rect.centery = tank.y
        self.speed = 10
##ビームの座標についての設定


    def update(self):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rect.move_ip(+self.speed*self.vx, +self.speed*self.vy)
        if check_bound(self.rect) != (True, True):
            self.kill()


def main():
    pg.display.set_caption("弾幕ゲー")
    screen = pg.display.set_mode((600, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/background.png")
    bg_fimg = pg.transform.flip(bg_img, True, False)
    tank = Tank(300, 500, "ex05/fig/player1.gif")
    beams = pg.sprite.Group()

    obstacles = []
    next_obstacle_time = time.time() + random.randint(1, 3)


    tmr = 0
    x = 0
    count = 0
    frame_count = 0

    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                beams.add(Beam(tank, angle=0))
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            tank.move_left(10, 0)
        if keys[pg.K_d]:
            tank.move_right(10, 600)

        if frame_count % 10 == 0:#ビーム自動発射
            beams.add(Beam(tank, angle=90))

        screen.blit(bg_img, [0, 0])
        tank.draw(screen)
        beams.update()
        beams.draw(screen)
        
        pg.display.update()
        tmr += 1
        x += 1
        frame_count += 1
        clock.tick(100)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
