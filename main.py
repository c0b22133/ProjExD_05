import sys
import pygame as pg
from pygame.sprite import AbstractGroup
import random
import time
import math

WIDTH = 600  # タンクの初期 x 座標
HEIGHT = 600  # タンクの初期 y 座標


def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（爆弾，戦車，ビーム）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate


class Enemy(pg.sprite.Sprite):
    imgs = [pg.image.load(f"test/fig/alien{i}.png") for i in range(1, 3)]

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


class Tank:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pg.image.load(image_path)
        self.width = self.image.get_width()

    def move_left(self, distance, min_x):
        self.x -= distance
        if self.x < min_x:
            self.x = min_x

    def move_right(self, distance, max_x):
        self.x += distance
        if self.x > max_x - self.width:
            self.x = max_x - self.width

    def draw(self, screen):
        screen.blit(self.image, [self.x, self.y])


class Beam(pg.sprite.Sprite):
    """
    ビームに関するクラス
    """
    def __init__(self, tank: Tank, angle: float):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load(f"test/fig/beam.png"), angle, 2.0)
        self.vx = math.cos(math.radians(angle))
        self.vy = -math.sin(math.radians(angle))
        self.rect = self.image.get_rect()
        self.rect.centerx = tank.x + tank.image.get_width()/2
        self.rect.centery = tank.y
        self.speed = 10


    def update(self):
        self.rect.move_ip(+self.speed*self.vx, +self.speed*self.vy)
        # self.rect.x += self.vx * self.speed
        # self.rect.y += self.vy * self.speed
        # 画面外に出たらビームをリセットする
        if not check_bound(self.rect)[1]:  # 縦方向のチェック
            self.kill()  # Sprite グループからこの Sprite を削除


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
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("test/fig/background.png")
    tank = Tank(300, 500, "test/fig/player1.gif")
    beams = pg.sprite.Group()
    emys = pg.sprite.Group()
    shield = pg.sprite.Group()

    obstacles = [] # 障害物のリスト
    next_obstacle_time = time.time() + random.randint(1, 3) # 障害物を生成する時刻

    tmr = 0
    count = 0
    frame_count = 0

    while True:
        screen.blit(bg_img, [0, 0])  # 背景画像を最初に描画
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            tank.move_left(10, 0)  # 左に移動
        if keys[pg.K_d]:
            tank.move_right(10, WIDTH)  # 右に移動
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB :
                shield.add(Shield(tank, 100, 300))

        if count < 5:
            emys.add(Enemy())

        if frame_count % 10 == 0:  # ビーム自動発射
            beams.add(Beam(tank, angle=90))

        # 障害物を生成
        if time.time() > next_obstacle_time and len(obstacles) < 3:
            obstacles.append(Obstacle(random.randint(0, 600), random.randint(200, 400), 100, 20))
            next_obstacle_time = time.time() + random.randint(1, 3)

        # 障害物を描画
        for obstacle in obstacles[:]:
            pg.draw.rect(screen, (126, 126, 126), obstacle.rect)
            if obstacle.is_expired(15):
                obstacles.remove(obstacle)

        tank.draw(screen)
        beams.update()
        beams.draw(screen)
        emys.update()
        emys.draw(screen)
        shield.update()
        shield.draw(screen)
        pg.display.update()
        count += 1
        tmr += 1
        frame_count += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
