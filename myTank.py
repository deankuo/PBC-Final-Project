import pygame
import bulletClass
import os

tank_T1_0 = os.path.join("image", "tank_T1_0.png")
tank_T1_1 = os.path.join("image", "tank_T1_1.png")
tank_T1_2 = os.path.join("image", "tank_T1_2.png")


class MyTank(pygame.sprite.Sprite):
    def __init__(self, playerNumber):
        pygame.sprite.Sprite.__init__(self)

        # 設定只有一個玩家
        if playerNumber == 1:
            self.tank_L0_image = pygame.image.load(tank_T1_0).convert_alpha()
            self.tank_L1_image = pygame.image.load(tank_T1_1).convert_alpha()
            self.tank_L2_image = pygame.image.load(tank_T1_2).convert_alpha()
        self.tank = self.tank_L0_image  # 玩家坦克

        # 運動中的兩種圖片
        self.tank_R0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_R1 = self.tank.subsurface((48, 0), (48, 48))
        self.rect = self.tank_R0.get_rect()  # 判斷碰撞
        if playerNumber == 1:
            self.rect.left, self.rect.top = (3 + 24 * 8, 3 + 24 * 24)

        # 我方坦克初始設定
        self.level = 1  # 坦克等級，預設為1，目前不調整
        self.life = True  # 玩家生命
        self.speed = 3  # 坦克速度
        self.dir_x, self.dir_y = 0, -1  # 坦克方向
        self.life = 3  # 坦克生命
        if self.life > 3:  # 最多只有三條命
            self.life = 3
        self.bulletNotCooling = True  # 子彈冷卻
        self.bullet = bulletClass.Bullet()
        self.bullet.rect.left, self.bullet.rect.right = 3 + 12 * 24, 3 + 20 * 20

    def shoot(self):
        # 子彈
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

        # 等級/食物強化
        if self.level == 1:
            self.bullet.speed = 14
            self.bullet.strong = False

    # 回傳True代表發生碰撞
    def moveUp(self, tankGroup, brickGroup, ironGroup, all_sprites):  # 應該還要考慮大本營不能碰到！
        self.dir_x, self.dir_y = 0, -1
        self.rect = self.rect.move(
            self.speed * self.dir_x, self.speed * self.dir_y)
        self.tank_R0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_R1 = self.tank.subsurface((48, 0), (48, 48))
        if self.rect.top < 3:  # 如果碰到地圖邊緣
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
                or pygame.sprite.spritecollide(self, ironGroup, False, None)\
                or pygame.sprite.spritecollide(self, all_sprites, False, None):  # 碰到磚頭或鋼鐵或大本營
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):  # 碰到其他坦克
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return True
        return False

    def moveDown(self, tankGroup, brickGroup, ironGroup, all_sprites):  # 應該還要考慮大本營不能碰到！
        self.dir_x, self.dir_y = 0, 1
        self.rect = self.rect.move(
            self.speed * self.dir_x, self.speed * self.dir_y)
        self.tank_R0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_R1 = self.tank.subsurface((48, 48), (48, 48))
        if self.rect.bottom > 630 - 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
                or pygame.sprite.spritecollide(self, ironGroup, False, None)\
                or pygame.sprite.spritecollide(self, all_sprites, False, None):
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return True
        return False

    def moveLeft(self, tankGroup, brickGroup, ironGroup, all_sprites):  # 應該還要考慮大本營不能碰到！
        self.dir_x, self.dir_y = -1, 0
        self.rect = self.rect.move(
            self.speed * self.dir_x, self.speed * self.dir_y)
        self.tank_R0 = self.tank.subsurface((0, 96), (48, 48))
        self.tank_R1 = self.tank.subsurface((48, 96), (48, 48))
        if self.rect.left < 3:
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
                or pygame.sprite.spritecollide(self, ironGroup, False, None)\
                or pygame.sprite.spritecollide(self, all_sprites, False, None):
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return True
        return False

    def moveRight(self, tankGroup, brickGroup, ironGroup, all_sprites):  # 應該還要考慮大本營不能碰到！
        self.dir_x, self.dir_y = 1, 0
        self.rect = self.rect.move(
            self.speed * self.dir_x, self.speed * self.dir_y)
        self.tank_R0 = self.tank.subsurface((0, 144), (48, 48))
        self.tank_R1 = self.tank.subsurface((48, 144), (48, 48))
        if self.rect.right > 630 - 3:
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
                or pygame.sprite.spritecollide(self, ironGroup, False, None)\
                or pygame.sprite.spritecollide(self, all_sprites, False, None):
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return True
        return False
