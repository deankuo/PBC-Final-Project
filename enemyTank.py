import pygame
import random
import bulletClass
import os


class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, x=None, kind=None, isred=None, isgreen=None):
        pygame.sprite.Sprite.__init__(self)

        # 坦克出現前是否播放動畫
        self.flash = False
        self.times = 90

        # 敵方坦克初始化屬性
        self.speed = 1  # 坦克速度
        self.dir_x, self.dir_y = (0, 1)  # 坦克初始方向
        self.life = 1  # 坦克生命
        self.bulletNotCooling = True  # 坦克子彈生命
        self.bullet = bulletClass.Bullet()  # 坦克子彈延遲

        # 參數：坦克種類（應該要依據關卡判斷？)，現在使用random判斷
        self.kind = kind
        if not kind:
            self.kind = 3
            # random.choice([1, 2, 3, 4])

        if self.kind == 1:
            self.enemy_x_0 = pygame.image.load(
                os.path.join("image", "enemy_1_0.png")).convert_alpha()
            self.enemy_x_1 = pygame.image.load(
                os.path.join("image", "enemy_1_1.png")).convert_alpha()
            self.enemy_x_3 = pygame.image.load(
                os.path.join("image", "enemy_1_3.png")).convert_alpha()
        if self.kind == 2:
            self.enemy_x_0 = pygame.image.load(
                os.path.join("image", "enemy_2_0.png")).convert_alpha()
            self.enemy_x_1 = pygame.image.load(
                os.path.join("image", "enemy_2_1.png")).convert_alpha()
            self.enemy_x_3 = pygame.image.load(
                os.path.join("image", "enemy_2_3.png")).convert_alpha()
        if self.kind == 3:
            self.enemy_x_0 = pygame.image.load(
                os.path.join("image", "enemy_3_0.png")).convert_alpha()
            self.enemy_x_1 = pygame.image.load(
                os.path.join("image", "enemy_3_1.png")).convert_alpha()
            self.enemy_x_3 = pygame.image.load(
                os.path.join("image", "enemy_3_3.png")).convert_alpha()
        if self.kind == 4:
            self.enemy_x_0 = pygame.image.load(
                os.path.join("image", "enemy_4_0.png")).convert_alpha()
            self.enemy_x_1 = pygame.image.load(
                os.path.join("image", "enemy_4_1.png")).convert_alpha()
            self.enemy_x_3 = pygame.image.load(
                os.path.join("image", "enemy_4_3.png")).convert_alpha()
        self.enemy_3_0 = pygame.image.load(
            os.path.join("image", "enemy_3_0.png")).convert_alpha()
        self.enemy_3_1 = pygame.image.load(
            os.path.join("image", "enemy_3_1.png")).convert_alpha()
        self.enemy_3_2 = pygame.image.load(
            os.path.join("image", "enemy_3_2.png")).convert_alpha()

        # 參數：調整敵方坦克屬性
        self.isred = isred  # 紅色特殊坦克，速度為3，（可攜帶食物？）
        self.isgreen = isgreen  # 綠色特殊坦克，血量為2
        if not None:
            self.isred = random.choice(
                (True, False, False, False))  # 25%機會有紅色坦克
        if not None and not isred:
            self.isgreen = random.choice(
                (True, False, False, False, False))  # 20%機會有綠色坦克

        if self.isred:  # 紅色坦克
            self.tank = self.enemy_x_3
            self.speed = 3
        elif self.isgreen:  # 綠色坦克
            self.tank = self.enemy_x_1
            self.life = 2
        else:  # 一般坦克
            self.tank = self.enemy_x_0

        # 參數：敵方坦克位置
        self.x = x
        if not self.x:
            self.x = random.choice([1, 2, 3, 4])
        self.x -= 1

        # 運動中的兩種圖片
        self.tank_R0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_R1 = self.tank.subsurface((48, 48), (48, 48))
        self.rect = self.tank_R0.get_rect()
        self.rect.left, self.rect.top = (3 + self.x * 12 * 15, 3 + 0 * 24)

        # 是否撞牆，撞牆則改變方向
        self.dirChange = False

    def shoot(self):
        # 賦予子彈生命
        self.bullet.life = True
        self.bullet.changeImage(self.dir_x, self.dir_y)

        if self.dir_x == 0 and self.dir_y == -1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top + 1
        elif self.dir_x == 0 and self.dir_y == 1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom - 1
        elif self.dir_x == -1 and self.dir_y == 0:
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.dir_x == 1 and self.dir_y == 0:
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20

    def move(self, tankGroup, brickGroup, ironGroup, all_sprites):
        self.rect = self.rect.move(
            self.speed * self.dir_x, self.speed * self.dir_y)

        if self.dir_x == 0 and self.dir_y == -1:
            self.tank_R0 = self.tank.subsurface((0, 0), (48, 48))
            self.tank_R1 = self.tank.subsurface((48, 0), (48, 48))
        elif self.dir_x == 0 and self.dir_y == 1:
            self.tank_R0 = self.tank.subsurface((0, 48), (48, 48))
            self.tank_R1 = self.tank.subsurface((48, 48), (48, 48))
        elif self.dir_x == -1 and self.dir_y == 0:
            self.tank_R0 = self.tank.subsurface((0, 96), (48, 48))
            self.tank_R1 = self.tank.subsurface((48, 96), (48, 48))
        elif self.dir_x == 1 and self.dir_y == 0:
            self.tank_R0 = self.tank.subsurface((0, 144), (48, 48))
            self.tank_R1 = self.tank.subsurface((48, 144), (48, 48))

        # 碰到地圖邊緣
        if self.rect.top < 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            self.dir_x, self.dir_y = random.choice(
                ([0, 1], [0, -1], [1, 0], [-1, 0]))
        elif self.rect.bottom > 630 - 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            self.dir_x, self.dir_y = random.choice(
                ([0, 1], [0, -1], [1, 0], [-1, 0]))
        elif self.rect.left < 3:
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            self.dir_x, self.dir_y = random.choice(
                ([0, 1], [0, -1], [1, 0], [-1, 0]))
        elif self.rect.right > 630 - 3:
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            self.dir_x, self.dir_y = random.choice(
                ([0, 1], [0, -1], [1, 0], [-1, 0]))

        # 碰到牆體、坦克或大本營
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
                or pygame.sprite.spritecollide(self, ironGroup, False, None) \
                or pygame.sprite.spritecollide(self, tankGroup, False, None)\
                or pygame.sprite.spritecollide(self, all_sprites, False, None):
            self.rect = self.rect.move(
                self.speed * -self.dir_x, self.speed * -self.dir_y)
            self.dir_x, self.dir_y = random.choice(
                ([0, 1], [0, -1], [1, 0], [-1, 0]))
