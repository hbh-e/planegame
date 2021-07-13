import pygame
from plane_sprites import *


class GameMain(object):
    """游戏主类"""

    def __init__(self):
        """游戏的初始化"""

        # 1.游戏窗口建立
        self.window = pygame.display.set_mode(WINDOW_RECT.size)
        # 2.创建游戏时钟
        self.clock = pygame.time.Clock()
        # 3.创建精灵
        self.__create_sprites()
        # 4.设置生成敌机定时器
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # 5 设置生成子弹的定时器
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        """创建精灵和精灵组"""

        # 1.创建背景精灵
        bg_1 = Backgroup(False)
        bg_2 = Backgroup(True)
        # 2.创建背景精灵组
        self.back_group = pygame.sprite.Group(bg_1, bg_2)
        # 3创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 4创建英雄精灵
        self.hero = Hero()
        # 创建英雄组
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        """游戏循环"""

        while True:
            # 1.设置帧率
            self.clock.tick(FRAME_PRE_SEC)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新精灵组
            self.__upadte_sprites()
            # 5.更新显示
            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameMain.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # 1创建敌机精灵
                enemys = Enemy()
                # 2把敌机精灵加到组内
                self.enemy_group.add(enemys)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 获得按键列表，按下为1
        key_pressed = pygame.key.get_pressed()
        # 右键按下往右移
        if key_pressed[pygame.K_RIGHT] == 1:
            self.hero.speed = 2
        # 左键按下往左移
        elif key_pressed[pygame.K_LEFT] == 1:
            self.hero.speed = -2
        # 其他情况不移动
        else:
            self.hero.speed = 0

    def __check_collide(self):

        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.enemy_group, self.hero.bullet_group, True, True)
        # 敌机撞毁英雄,这里返回的是被摧毁敌机的列表
        bad_enemy = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        # 通过判断摧毁敌机的列表来判断英雄是否撞机
        if len(bad_enemy):
            self.hero.kill()
            GameMain.__game_over()

    def __upadte_sprites(self):
        """更新精灵和精灵组"""

        # 更新背景精灵组
        self.back_group.update()
        # 在哪里画
        self.back_group.draw(self.window)

        # 更新敌机精灵组和画出来
        self.enemy_group.update()
        self.enemy_group.draw(self.window)

        # 更新英雄精灵组和画出来
        self.hero_group.update()
        self.hero_group.draw(self.window)

        # 更新子弹精灵组和画出来
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.window)

    @staticmethod
    def __game_over():
        """结束游戏,这是一个静态方法"""

        # 释放pygame资源
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = GameMain()
    game.start_game()