import pygame
import os


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.bullet_up = pygame.image.load(
            os.path.join("image", "bullet_up.png"))
        self.bullet_down = pygame.image.load(
            os.path.join("image", "bullet_down.png"))
        self.bullet_left = pygame.image.load(
            os.path.join("image", "bullet_left.png"))
        self.bullet_right = pygame.image.load(
            os.path.join("image", "bullet_right.png"))

        # 方向速度生命碎石
        self.dir_x, self.dir_y = 0, 0
        self.speed = 12  # 6
        self.life = False
        self.strong = False

        self.bullet = self.bullet_up
        self.rect = self.bullet.get_rect()
        self.rect.left, self.rect.right = 30 + 12 * 24, 30 + 24 * 24

    def changeImage(self, dir_x, dir_y):
        self.dir_x, self.dir_y = dir_x, dir_y
        if self.dir_x == 0 and self.dir_y == -1:
            self.bullet = self.bullet_up
        elif self.dir_x == 0 and self.dir_y == 1:
            self.bullet = self.bullet_down
        elif self.dir_x == -1 and self.dir_y == 0:
            self.bullet = self.bullet_left
        elif self.dir_x == 1 and self.dir_y == 0:
            self.bullet = self.bullet_right

    def move(self):
        self.rect = self.rect.move(self.speed * self.dir_x,
                                   self.speed * self.dir_y)

        # 碰撞地圖邊緣
        if self.rect.top < 3:
            self.life = False
        #    self.rect.left, self.rect.right = 3 + 12 * 24, 3 + 24 * 24
        if self.rect.bottom > 630 - 3:
            self.life = False
        #    self.rect.left, self.rect.right = 3 + 12 * 24, 3 + 24 * 24
        if self.rect.left < 3:
            self.life = False
        #    self.rect.left, self.rect.right = 3 + 12 * 24, 3 + 24 * 24
        if self.rect.right > 630 - 3:
            self.life = False
        #    self.rect.left, self.rect.right = 3 + 12 * 24, 3 + 24 * 24
