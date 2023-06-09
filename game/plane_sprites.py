import random
import pygame

# 游戏屏幕的尺寸
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 游戏的刷新帧率
FRAME_PER_SEC = 60
# 敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
Hero_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """游戏精灵基类"""

    def __init__(self, image_name, speed=1):
        # 调用父类的初始方法
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        # 记录速度
        self.speed = speed

    def update(self, *args):
        # 默认在垂直方向移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):

        # 1.调用父类方法实现精灵的创建(image/rect/speed)
        image_name = "./images/background.png"
        super().__init__(image_name)
        # 2.判断是否交替图片，如果是，将图片设置到屏幕顶部
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self, *args):

        # 1.调用父类方法实现
        super().update()
        # 2.判断是否移出屏幕，如移出，将图像设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        # 1.调用父类方法创建敌机精灵，并指定敌机图像
        super().__init__("./images/enemy1.png")
        # 2.设置敌机的随机速度(初始) 1~3
        self.speed = random.randint(1, 3)
        # 3.设置敌机的随机位置（初始）水平方向
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self, *args):
        # 1.调用父类让敌机在垂直方向移动
        super().update()
        # 2.判断是否飞出屏幕,如果是，需将敌机删除
        if self.rect.y >= SCREEN_RECT.height:
            print("敌机飞出屏幕...")
            # 3.将精灵从所有组中删除
            self.kill()

    def __del__(self):
        print("敌机挂了　%s" % self.rect)


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):
        super().__init__("./images/me1.png", 0)
        # 设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # 每隔 0.5s 发射一次子弹
        pygame.time.set_timer(Hero_FIRE_EVENT, 500)
        # 1.创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self, *args):
        # 英雄飞机在水平方向运动
        self.rect.x += self.speed
        # 判断屏幕边界
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("发射子弹...")
        # 实现一次发射三枚子弹
        for i in (1, 2, 3):
            # 1.创建子弹精灵
            bullet = Bullet()
            # 2.设置子弹精灵位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 3.将子弹精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self, *args):
        super().update()
        # 判断是否飞出屏幕，飞出删除
        if self.rect.bottom < 0:
            self.kill()
