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

import random
import time

class Obstacle:
    def __init__(self, x, y, width, height):
        '''
        障害物を生成する
        '''
        self.rect = pg.Rect(x, y, width, height)
        self.created_time = time.time()

    def is_expired(self, duration):
        '''
        障害物が duration 秒経過したかどうかを返す
        '''
        return time.time() - self.created_time > duration
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
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/background.png")

    bg_fimg = pg.transform.flip(bg_img, True, False)
    tank = Tank(300, 500, "ex05/fig/player1.gif")
    beams = pg.sprite.Group()

    obstacles = []
    next_obstacle_time = time.time() + random.randint(1, 3)


    tank = Tank(300, 500, "ex05/fig/player1.gif")
    sheild = pg.sprite.Group()

    tank_img = pg.image.load("ex05/fig/player1.gif")
    emys = pg.sprite.Group()

    tmr = 0
    x = 0
    count = 0
    frame_count = 0


    obstacles = [] # 障害物のリスト
    next_obstacle_time = time.time() + random.randint(1, 3) # 障害物を生成する時刻

    count = 0

    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:

                return 0
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                beams.add(Beam(tank, angle=0))
                return
            

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            tank.move_left(10, 0)
        if keys[pg.K_d]:
            tank.move_right(10, 600)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB :
                    sheild.add(Shield(tank, 100, 300))


        if count < 5:
            emys.add(Enemy())

        if frame_count % 10 == 0:#ビーム自動発射
            beams.add(Beam(tank, angle=90))

        screen.blit(bg_img, [0, 0])
        tank.draw(screen)
        beams.update()
        beams.draw(screen)
        
        pg.display.update()

        # 障害物を生成
        if time.time() > next_obstacle_time and len(obstacles) < 5:
            obstacles.append(Obstacle(random.randint(0, 600), random.randint(200, 400), 100, 20))
            next_obstacle_time = time.time() + random.randint(1, 3) # 次の障害物を生成する時刻を更新

        # 障害物を描画
        for obstacle in obstacles[:]:
            pg.draw.rect(screen, (126, 126, 126), obstacle.rect)
            if obstacle.is_expired(15):
                obstacles.remove(obstacle)

        emys.update()
        emys.draw(screen)
        pg.display.update()
        count+=1
        tmr += 1

        x += 1
        frame_count += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()