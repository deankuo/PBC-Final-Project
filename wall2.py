import pygame
import os

WIDTH = 630
HEIGHT = 630
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
brickImage = os.path.join("image", "mybook.png")
ironImage = os.path.join("image", "gomi.png")


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(brickImage)
        self.rect = self.image.get_rect()


class Iron(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(ironImage)
        self.rect = self.image.get_rect()


class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 150))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, 630)
        self.health = 100


class Map():
    def __init__(self):
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # 畫磚塊
        # 中間
        X28 = [12, 13, 14]
        Y28 = [2, 3, 4, 9, 10, 11, 12, 15, 16, 17]
        X46 = [8, 9, 10, 16, 17, 18]
        Y46 = [6, 7, 8, 19, 20, 21]

        # 大本營外圍
        X0Y0 = [(11, 23), (12, 23), (13, 23), (14, 23),
                (11, 24), (14, 24), (11, 25), (14, 25)]

        # 外側
        X1379 = [3, 4, 5]
        Y1379 = [2, 3, 4, 13, 14, 15, 23, 24, 25]
        X_edge = [24, 25]
        Y_edge = [4, 5, 9, 10, 17, 18, 22, 23]

        # 填補空隙
        X_mid = [10, 11, 15, 16]
        Y_mid = [4, 5, 9, 10, 17, 18]
        X_out = [0, 1, 2]
        Y_out = [5, 6, 7, 10, 11, 12, 16, 17, 18, 21, 22, 23]
        X_right = [22, 23, 24]
        Y_right = [6, 7, 8, 19, 20, 21]

        # 其他_預設
        X5 = [12, 13]
        Y5 = [16, 17]

        for x in X_edge:
            for y in Y_edge:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brickGroup.add(self.brick)
        for x in X_right:
            for y in Y_right:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brickGroup.add(self.brick)
        for x in X_out:
            for y in Y_out:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brickGroup.add(self.brick)
        for x in X1379:
            for y in Y1379:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brickGroup.add(self.brick)
        for x in X28:
            for y in Y28:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brickGroup.add(self.brick)
        for x in X46:
            for y in Y46:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brickGroup.add(self.brick)
        for x in X5:
            for y in Y5:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brickGroup.add(self.brick)
        for x, y in X0Y0:
            self.brick = Brick()
            self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
            self.brickGroup.add(self.brick)
        for x in X_mid:
            for y in Y_mid:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brickGroup.add(self.brick)

        # 畫石頭
        for x, y in [(0, 9), (22, 14), (23, 14), (3, 1), (2, 1), (10, 1), (11, 1), (24, 3), (25, 3), (2, 20), (3, 20), (13, 13), (13, 14), (12, 14), (12, 13), (19, 22)]:
            self.iron = Iron()
            self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
            self.ironGroup.add(self.iron)

        # 畫大本營
        self.base = Base()
        self.all_sprites.add(self.base)
