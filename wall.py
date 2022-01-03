import pygame
import os

WIDTH = 630
HEIGHT = 630
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
brickImage = os.path.join("image", "brick.png")
ironImage = os.path.join("image", "stone.png")


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

        # 数字代表地图中的位置
        # # 画砖块
        X1379 = [3.5, 4.5, 20, 21]
        Y1379 = [2, 3, 4, 5, 21, 22, 23, 24]
        X28 = [9, 10, 11, 14, 15, 16, 17]
        Y28 = [10, 10.75]
        X46 = [4.5, 5, 5.5, 19, 20]
        Y46 = [13, 14, 14.5]
        X5 = [12.5, 13, 14, 15, 16, 17]
        Y5 = [17, 18]
        X6 = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        Y6 = [2.75, 3, 4]
        X0Y0 = [(11, 23), (12, 23), (13, 23), (14, 23),
                (11, 24), (14, 24), (11, 25), (14, 25)]
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
        for x in X6:
            for y in Y6:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brickGroup.add(self.brick)
        for x, y in X0Y0:
            self.brick = Brick()
            self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
            self.brickGroup.add(self.brick)
        # 画石头
        for x, y in [(3.5, 6), (3.5, 7), (4, 6), (4, 7), (9, 17), (9, 17.5), (10, 17), (10, 17.5), (11, 17), (11, 17.5), (12, 10), (13, 10), (12, 10.25), (13, 10.25), (20, 6), (20, 7), (20.5, 6), (20.5, 7), ]:
            self.iron = Iron()
            self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
            self.ironGroup.add(self.iron)

        # 畫大本營
        self.base = Base()
        self.all_sprites.add(self.base)
