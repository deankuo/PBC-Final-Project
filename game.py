import pygame
import os
pygame.init()
WIDTH = 630
HEIGHT = 630
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("TANK War!", "middle")

background_jpg = pygame.image.load(
    os.path.join("image", "background.jpg")).convert()

font_name = pygame.font.match_font("arial")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_init():
    screen.blit(background_jpg, (0, 0))
    draw_text(screen, "NTU Tank War", 64, WIDTH/2, HEIGHT/6)
    draw_text(screen, "Shoot = Space, Move = Arrow keys",
              32, WIDTH/2, HEIGHT/2, WHITE)
    draw_text(screen, "Press any button to start",
              26, WIDTH/2, HEIGHT*(5/6), WHITE)
    pygame.display.update()
    wating = True
    while wating:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                wating = False


def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 150))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, 630)
        self.health = 100


all_sprites = pygame.sprite.Group()
base = Base()
all_sprites.add(base)

FPS = 60
running = True
show_init = True
while running:
    if show_init:
        draw_init()
        show_init = False
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # hits = pygame.sprite.spritecollide(base, bullet, True)
        # for hit in hits:
        # 	base.health -= 20
        # 	if base.health <= 0:
        # 		show_init = True
    all_sprites.update()

    screen.fill(BLACK)
    screen.blit(background_jpg, (0, 0))
    all_sprites.draw(screen)
    draw_health(screen, base.health, 520, 15)
    pygame.display.update()
