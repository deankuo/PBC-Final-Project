# -*- coding: utf-8 -*-
import enemyTank
import food
import myTank
import os
import sys
import time
import traceback
import pygame
import wall
import wall2


def main(ige, lev):
    # pygame 初始化
    pygame.init()
    pygame.mixer.init()

    # 視窗基礎設定
    resolution = (630, 630)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption(" Tank War! ", 'middle')

    # 復活次數展示圖
    player_img = pygame.image.load(os.path.join(
        "image", "tank_T1_0.png")).subsurface((0, 0), (48, 48)).convert()
    player_mini_img = pygame.transform.scale(player_img, (25, 19))

    # 放入背景圖片、音樂、音效、特效
    background_image = pygame.image.load(
        os.path.join("image", ige))

    home_image = pygame.image.load(os.path.join("image", "home.png"))
    home_destroyed_image = pygame.image.load(
        os.path.join("image", "home_destroyed.png"))

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

    expl_anim = {}
    expl_anim['enemy_tank'] = []
    expl_anim['my_tank'] = []
    for i in range(9):
        expl_img = pygame.image.load(
            os.path.join("image", f"expl{i}.png")).convert()
        expl_img.set_colorkey((0, 0, 0))
        expl_anim['enemy_tank'].append(
            pygame.transform.scale(expl_img, (48, 48)))
        expl_anim['my_tank'].append(pygame.transform.scale(expl_img, (48, 48)))
        player_expl_img = pygame.image.load(
            os.path.join("image", f"player_expl{i}.png")).convert()
        player_expl_img.set_colorkey((0, 0, 0))
    bang_sound = pygame.mixer.Sound(os.path.join("music", "bang.wav"))
    bang_sound.set_volume(1)
    fire_sound = pygame.mixer.Sound(os.path.join("music", "fire.wav"))
    start_sound = pygame.mixer.Sound(os.path.join("music", "start.wav"))
    start_sound.play()

    # 定義精靈組
    allTankGroup = pygame.sprite.Group()  # 所有坦克
    mytankGroup = pygame.sprite.Group()  # 我方坦克
    allEnemyGroup = pygame.sprite.Group()  # 所有敵方坦克
    redEnemyGroup = pygame.sprite.Group()  # 敵方紅色坦克
    greenEnemyGroup = pygame.sprite.Group()  # 敵方綠色坦克
    otherEnemyGroup = pygame.sprite.Group()  # 敵方其他坦克
    enemyBulletGroup = pygame.sprite.Group()  # 敵方子彈
    explosionList = []  # 儲存爆炸

    # 創建生命顯示圖
    def draw_life(surf, lives, img, x, y):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 32*i
            img_rect.y = y
            surf.blit(img, img_rect)

    # 爆炸動畫
    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center, tank_ca):
            pygame.sprite.Sprite.__init__(self)
            self.tank_ca = tank_ca
            self.image = expl_anim[self.tank_ca][0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50
            self.Life = True

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(expl_anim[self.tank_ca]):  # 動畫到最後一張
                    self.Life = False
                else:
                    self.image = expl_anim[self.tank_ca][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center

        def displayExplode(self):
            screen.blit(self.image, self.rect)

    # 玩家復活時暫時隱藏玩家坦克
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (3 + 24 * 8, 3 + 24 * 24)

    # 創建地圖
    if lev == 1:
        bgMap = wall.Map()
    elif lev == 2:
        bgMap = wall2.Map()

    # 創建食物/道具 但不顯示
    prop = food.Food()

    # 創建我方坦克
    myTank_T1 = myTank.MyTank(1)
    allTankGroup.add(myTank_T1)
    mytankGroup.add(myTank_T1)

    # 創建敵方坦克
    for i in range(1, 5):
        enemy = enemyTank.EnemyTank(i)
        allTankGroup.add(enemy)
        allEnemyGroup.add(enemy)
        if enemy.isred == True:
            redEnemyGroup.add(enemy)
            continue
        elif enemy.isgreen == True:
            greenEnemyGroup.add(enemy)
            continue
        else:
            otherEnemyGroup.add(enemy)

    # 敵方坦克出現動畫
    appearance_image = pygame.image.load(
        os.path.join("image", "appear.png")).convert_alpha()
    appearance = []
    appearance.append(appearance_image.subsurface((0, 0), (48, 48)))
    appearance.append(appearance_image.subsurface((48, 0), (48, 48)))
    appearance.append(appearance_image.subsurface((96, 0), (48, 48)))

    # 自定義事件
    # 創建敵方坦克延遲200
    DELAYEVENT = pygame.constants.USEREVENT
    pygame.time.set_timer(DELAYEVENT, 200)
    # 創建 敵方子彈延遲1000
    ENEMYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 1
    pygame.time.set_timer(ENEMYBULLETNOTCOOLINGEVENT, 1000)
    # 創建 我方子彈延遲200
    MYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 2
    pygame.time.set_timer(MYBULLETNOTCOOLINGEVENT, 200)
    # 敵方坦克 靜止8000
    NOTMOVEEVENT = pygame.constants.USEREVENT + 3
    pygame.time.set_timer(NOTMOVEEVENT, 8000)

    delay = 100
    moving = 0
    movdir = 0
    enemyNumber = 4
    enemyCouldMove = True
    switch_R1_R2_image = True
    homeSurvive = True
    running_T1 = True
    running = True
    clock = pygame.time.Clock()

    while running:
        # 畫背景
        screen.blit(background_image, (0, 0))
        # 畫磚頭
        for each in bgMap.brickGroup:
            screen.blit(each.image, each.rect)
        # 畫石頭
        for each in bgMap.ironGroup:
            screen.blit(each.image, each.rect)
        # 畫大本營
        if homeSurvive:
            screen.blit(home_image, (3 + 12 * 24, 3 + 24 * 24))
        else:
            screen.blit(home_destroyed_image, (3 + 12 * 24, 3 + 24 * 24))
        # 畫生命
        draw_life(screen, myTank_T1.life, player_mini_img, 0, 12)
        # 畫大本營血條
        draw_health(screen, base.health, 520, 15)

        # 畫爆炸
        for explode in explosionList:
            if explode.Life:
                explode.displayExplode()
                explode.update()
            else:
                explosionList.remove(explode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 我方子彈冷卻事件
            if event.type == MYBULLETNOTCOOLINGEVENT:
                myTank_T1.bulletNotCooling = True

            # 敵方子彈冷卻事件
            if event.type == ENEMYBULLETNOTCOOLINGEVENT:
                for each in allEnemyGroup:
                    each.bulletNotCooling = True

            # 敵方坦克靜止事件
            if event.type == NOTMOVEEVENT:
                enemyCouldMove = True

            # 創建敵方坦克延遲
            if event.type == DELAYEVENT:
                if enemyNumber <= 4:
                    if enemy.isred == True:
                        redEnemyGroup.add(enemy)
                    elif enemy.isgreen == True:
                        greenEnemyGroup.add(enemy)
                    else:
                        otherEnemyGroup.add(enemy)

            if event.type == pygame.KEYDOWN:  # 按下x 退出遊戲
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()

        # 檢查玩家鍵盤操作
        key_pressed = pygame.key.get_pressed()

        # 玩家一的移動操作
        if moving:
            moving -= 1
            if movdir == 0:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.all_sprites):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True
            if movdir == 1:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.all_sprites):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True
            if movdir == 2:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.all_sprites):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True
            if movdir == 3:
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.all_sprites):
                    moving += 1
                allTankGroup.add(myTank_T1)
                running_T1 = True

        if not moving:
            if key_pressed[pygame.K_UP]:  # 上鍵向上移動
                moving = 7
                movdir = 0
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.all_sprites):
                    moving = 0
                allTankGroup.add(myTank_T1)
            elif key_pressed[pygame.K_DOWN]:  # 下鍵向下移動
                moving = 7
                movdir = 1
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.all_sprites):
                    moving = 0
                allTankGroup.add(myTank_T1)
            elif key_pressed[pygame.K_LEFT]:  # 左鍵向左移動
                moving = 7
                movdir = 2
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.all_sprites):
                    moving = 0
                allTankGroup.add(myTank_T1)
            elif key_pressed[pygame.K_RIGHT]:  # 右鍵向右移動
                moving = 7
                movdir = 3
                running_T1 = True
                allTankGroup.remove(myTank_T1)
                if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup, bgMap.all_sprites):
                    moving = 0
                allTankGroup.add(myTank_T1)
        # 射擊
        if key_pressed[pygame.K_SPACE]:  # 空白鍵射擊
            if not myTank_T1.bullet.life and myTank_T1.bulletNotCooling:
                fire_sound.play()
                myTank_T1.shoot()
                myTank_T1.bulletNotCooling = False

        # 畫我方坦克
        if not (delay % 5):
            switch_R1_R2_image = not switch_R1_R2_image
        if switch_R1_R2_image and running_T1:
            screen.blit(myTank_T1.tank_R0,
                        (myTank_T1.rect.left, myTank_T1.rect.top))
            running_T1 = False
        else:
            screen.blit(myTank_T1.tank_R1,
                        (myTank_T1.rect.left, myTank_T1.rect.top))

        # 畫敵方坦克
        for each in allEnemyGroup:
            # 判斷特效是否播放
            if each.flash:
                #　判斷畫左動作還是右動作
                if switch_R1_R2_image:
                    screen.blit(each.tank_R0, (each.rect.left, each.rect.top))
                    if enemyCouldMove:
                        allTankGroup.remove(each)
                        each.move(allTankGroup, bgMap.brickGroup,
                                  bgMap.ironGroup, all_sprites)
                        allTankGroup.add(each)
                else:
                    screen.blit(each.tank_R1, (each.rect.left, each.rect.top))
                    if enemyCouldMove:
                        allTankGroup.remove(each)
                        each.move(allTankGroup, bgMap.brickGroup,
                                  bgMap.ironGroup, all_sprites)
                        allTankGroup.add(each)
            else:
                # 播放敵方坦克出場特效
                if each.times > 0:
                    each.times -= 1
                    if each.times <= 10:
                        screen.blit(appearance[2], (3 + each.x * 12 * 15, 3))
                    elif each.times <= 20:
                        screen.blit(appearance[1], (3 + each.x * 12 * 15, 3))
                    elif each.times <= 30:
                        screen.blit(appearance[0], (3 + each.x * 12 * 15, 3))
                    elif each.times <= 40:
                        screen.blit(appearance[2], (3 + each.x * 12 * 15, 3))
                    elif each.times <= 50:
                        screen.blit(appearance[1], (3 + each.x * 12 * 15, 3))
                    elif each.times <= 60:
                        screen.blit(appearance[0], (3 + each.x * 12 * 15, 3))
                    elif each.times <= 70:
                        screen.blit(appearance[2], (3 + each.x * 12 * 15, 3))
                    elif each.times <= 80:
                        screen.blit(appearance[1], (3 + each.x * 12 * 15, 3))
                    elif each.times <= 90:
                        screen.blit(appearance[0], (3 + each.x * 12 * 15, 3))
                if each.times == 0:
                    each.flash = True

        # 繪製我方子彈
        if myTank_T1.bullet.life:
            myTank_T1.bullet.move()
            screen.blit(myTank_T1.bullet.bullet, myTank_T1.bullet.rect)

            # 子彈 碰撞子彈
            for each in enemyBulletGroup:
                if each.life:
                    if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                        myTank_T1.bullet.life = False
                        each.life = False
                        pygame.sprite.spritecollide(
                            myTank_T1.bullet, enemyBulletGroup, True, None)

            # 子彈 碰撞敵方坦克
            if pygame.sprite.spritecollide(myTank_T1.bullet, redEnemyGroup, False, None):
                prop.change()
                bang_sound.play()
                enemyNumber -= 1
                # hits為發生碰撞的位置列表
                hits = pygame.sprite.spritecollide(  # 如果子彈碰到敵方紅色坦克，爆炸動畫
                    myTank_T1.bullet, redEnemyGroup, True)
                for hit in hits:
                    expl = Explosion(hit.rect.center, 'enemy_tank')
                    explosionList.append(expl)
                myTank_T1.bullet.life = False
                if enemyNumber == 0:
                    # time.sleep(0.5)
                    running = False
            elif pygame.sprite.spritecollide(myTank_T1.bullet, greenEnemyGroup, False, None):
                for each in greenEnemyGroup:
                    if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                        if each.life == 1:
                            bang_sound.play()
                            enemyNumber -= 1
                            expl = Explosion(each.rect.center, 'enemy_tank')
                            each.kill()
                            explosionList.append(expl)
                            each.life -= 1
                            if enemyNumber == 0:
                                # time.sleep(0.5)
                                running = False
                        elif each.life == 2:
                            each.life -= 1
                myTank_T1.bullet.life = False
            elif pygame.sprite.spritecollide(myTank_T1.bullet, otherEnemyGroup, False, None):
                bang_sound.play()
                enemyNumber -= 1
                hits = pygame.sprite.spritecollide(
                    myTank_T1.bullet, otherEnemyGroup, True)
                for hit in hits:
                    expl = Explosion(hit.rect.center, 'enemy_tank')
                    explosionList.append(expl)
                myTank_T1.bullet.life = False
                if enemyNumber == 0:
                    # time.sleep(0.5)
                    running = False

            # 子弹 碰撞 brickGroup
            if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.brickGroup, True, None):
                myTank_T1.bullet.life = False
                myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24

            # 子弹 碰撞 ironGroup
            if myTank_T1.bullet.strong:
                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, True, None):
                    myTank_T1.bullet.life = False
                    myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            else:
                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, False, None):
                    myTank_T1.bullet.life = False
                    myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24

            # 子弹 碰撞 base
            if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.all_sprites, False, None):
                myTank_T1.bullet.life = False
                myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24

        # 繪製敵人子彈
        for each in allEnemyGroup:
            # 如果子彈没有生命，就賦予子彈生命
            if not each.bullet.life and each.bulletNotCooling and enemyCouldMove:
                enemyBulletGroup.remove(each.bullet)
                each.shoot()
                enemyBulletGroup.add(each.bullet)
                each.bulletNotCooling = False
            # 如果特效播放完畢 並且 子彈存活 則繪製敵方子彈
            if each.flash:
                if each.bullet.life:
                    # 如果敵方可以移動
                    if enemyCouldMove:
                        each.bullet.move()
                    screen.blit(each.bullet.bullet, each.bullet.rect)

                    # 敵方子彈 碰撞 我方坦克
                    if pygame.sprite.collide_rect(each.bullet, myTank_T1):
                        bang_sound.play()
                        myTank_T1.life -= 1
                        death_expl = Explosion(
                            myTank_T1.rect.center, 'my_tank')
                        explosionList.append(death_expl)
                        hide(myTank_T1)
                        myTank_T1.rect.left, myTank_T1.rect.top = 3 + 8 * 24, 3 + 24 * 24
                        each.bullet.life = False
                        moving = 0  # 重置移動控制參數

                    # 子彈 碰撞brickGroup
                    if pygame.sprite.spritecollide(each.bullet, bgMap.brickGroup, True, None):
                        each.bullet.life = False

                    # 子彈 碰撞homeGroup
                    if pygame.sprite.spritecollide(each.bullet, bgMap.all_sprites, False, None):
                        myTank_T1.bullet.life = False
                        myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                        hits = pygame.sprite.spritecollide(
                            each.bullet, bgMap.all_sprites, False, None)
                        for hit in hits:
                            base.health -= 20
                            if base.health <= 0:
                                show_init = True
                        all_sprites.update()

                    # 子彈 碰撞ironGroup
                    if each.bullet.strong:
                        if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, True, None):
                            each.bullet.life = False
                    else:
                        if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, False, None):
                            each.bullet.life = False

        # 食物/道具部分
        if prop.life:
            screen.blit(prop.image, prop.rect)

            # 我方坦克碰撞 食物/道具
            if pygame.sprite.collide_rect(myTank_T1, prop):
                if prop.kind == 1:  # 敵人全毀
                    for each in allEnemyGroup:
                        if pygame.sprite.spritecollide(each, allEnemyGroup, True, None):
                            bang_sound.play()
                            enemyNumber -= 1
                    prop.life = False
                if prop.kind == 2:  # 敵人静止
                    enemyCouldMove = False
                    prop.life = False
                if prop.kind == 3:  # 子弹增强
                    myTank_T1.bullet.strong = True
                    prop.life = False
                if prop.kind == 4:  # 大本營得到保護
                    for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
                        bgMap.iron = wall.Iron()
                        bgMap.iron.rect.left, bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                        bgMap.ironGroup.add(bgMap.iron)
                    prop.life = False
                if prop.kind == 5:  # 坦克無敵
                    prop.life = False
                    pass
                if prop.kind == 6:  # 坦克生命+1
                    if myTank_T1.life < 3:
                        myTank_T1.life += 1
                    else:
                        myTank_T1.life = 3
                    prop.life = False

        # 生命歸0，遊戲結束
        if myTank_T1.life == 0:
            running = False
        if base.health == 0:
            running = False

        # 延遲
        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)


pygame.init()
WIDTH = 630
HEIGHT = 630
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("TANK")

background_jpg = pygame.image.load(
    os.path.join("image", "background_revise.jpg")).convert()

font_name = pygame.font.match_font("arial")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_init():
    screen.blit(background_jpg, (0, 0))
    draw_text(screen, "NTU Tank War", 64, WIDTH/2, HEIGHT/6)
    draw_text(screen, "Shoot = Space, Move = Arrow keys",
              32, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Press any button to start",
              26, WIDTH/2, HEIGHT*(5/6))
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
show_init = True

if show_init:
    draw_init()
    show_init = False
clock.tick(FPS)
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

screen.fill(BLACK)
screen.blit(background_jpg, (0, 0))
all_sprites.draw(screen)
draw_health(screen, base.health, 520, 15)
pygame.display.update()

if __name__ == "__main__":
    try:
        main("map.png", 1)
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
    time.sleep(2)
    try:
        main("socialscience_back.png", 2)
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
pygame.quit()
