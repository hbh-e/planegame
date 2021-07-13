import random
import pygame

# 游戏屏幕大小常量
WINDOW_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PRE_SEC = 60
# 创建敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战飞机精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类初始化方法
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.speed = speed
        self.rect = self.image.get_rect()

    def update(self):
        # 竖直方向移动
        self.rect.y += self.speed


class Backgroup(GameSprite):
    """背景精灵"""

    def __init__(self, tick):

        # 1.调用父类方法
        super().__init__("./images/background.png")
        # 2.改变图的垂直位置
        if tick:
            self.rect.y = -self.rect.height

    def update(self):

        # 1.调用父类方法
        super().update()
        # 2.背景移出屏幕回到屏幕顶上
        if self.rect.y >= WINDOW_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""

    def __init__(self):
        """加载图片，确定速度 ，确定x位置"""

        # 调用父类方法加载图片
        super().__init__("./images/enemy1.png")
        # 随机生成敌机速度
        self.speed = random.randint(1, 5)
        # 随机生成敌机位置
        self.rect.x = random.randint(0, WINDOW_RECT.width-self.rect.width)

    def update(self):

        super().update()
        # 销毁出屏幕的敌机
        if self.rect.y >= WINDOW_RECT.height:
            self.kill()
    """ 
    #这是一个测试代码，测试敌机是否被销毁      
    def __del__(self):
        print('死了')
    """


class Hero(GameSprite):

    def __init__(self):

        # 调用父类方法，加载英雄图片
        super().__init__("./images/me1.png", 0)

        # 设置英雄的位置
        self.rect.bottom = WINDOW_RECT.height - 120
        self.rect.centerx = WINDOW_RECT.centerx
        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        """因为父类方法不适合，就重写update，而不是扩展update"""

        self.rect.x += self.speed

        # 判断英雄是否出界,把英雄留在屏幕内
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WINDOW_RECT.right:
            self.rect.right = WINDOW_RECT.right

    def fire(self):
        # 三连射
        for increment in range(3):
            # 1.创建子弹精灵
            bullet_1 = Bullet()
            # 2,设定子弹位置
            bullet_1.rect.centerx = self.rect.centerx
            bullet_1.rect.bottom = self.rect.y - 20 * increment
            # 3,把子弹精灵加入精灵组
            self.bullet_group.add(bullet_1)


class Bullet(GameSprite):
    """属性：位置，速度
       方法： 可以扩展父类的方法，还要消除出屏幕的子弹对象
    """

    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self):

        super().update()
        if self.rect.bottom <= 0:
            self.kill()


