import random
from os import path
from random import randrange
from threading import Timer
from player import Player

import pygame

FPS = 60
HEIGHT = 900
WIDTH = 450
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
BAR_LENGTH = 400
BAR_HEIGHT = 5
score = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test game")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")
exp_dir = path.join(img_dir, "explosion_anim")


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.random_size = random.choice(asteroids)
        self.img_orig = random.choice(self.random_size)
        self.img_orig.set_colorkey(BLACK)
        self.image = pygame.Surface((20, 20))
        self.image = self.img_orig.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(0.9 * self.rect.width / 2)
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-100, -30)
        if self.random_size == meteor_images_l:
            self.speed_y = randrange(1, 3)
            self.speed_x = randrange(-1, 1)
        else:
            self.speed_y = randrange(2, 5)
            self.speed_x = randrange(-1, 1)
        self.rot = 0
        self.rot_speed = randrange(-5, 5)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = randrange(WIDTH - self.rect.width)
            self.rect.y = randrange(-100, -30)
            self.speed_y = randrange(1, 5)
            self.speed_x = randrange(-1, 1)

        self.rotate()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 40:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.img_orig, self.rot)
            old_centre = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_centre


class Explosion(pygame.sprite.Sprite):
    def __init__(self, centre, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[size][0]
        self.rect = self.image.get_rect()
        self.rect.center = centre
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 45

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(explosion_anim[self.size]):
                self.kill()
            else:
                centre = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = centre


font_name = pygame.font.match_font("arial")


def stop_game():
    global running
    running = False


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def new_mob():
    mob = Mob()
    mobs.add(mob)
    sprites.add(mob)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_fullness = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, bar_fullness, BAR_HEIGHT)

    fill_rect.center = (x, y)
    outline_rect.center = (x, y)

    pygame.draw.rect(surf, WHITE, outline_rect)
    pygame.draw.rect(surf, (175, 35, 100), fill_rect)


bg = pygame.image.load(path.join(img_dir, "darkPurple.png")).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg_rect = bg.get_rect()

meteor_images_l = []
meteor_images_ms = []
meteor_list_l = ["meteorGrey_big1.png", "meteorGrey_big4.png"]
meteor_list_ms = ["meteorGrey_small1.png", "meteorGrey_med2.png", "meteorGrey_med2.png", "meteorGrey_tiny2.png"]
asteroids = [meteor_images_l, meteor_images_ms]

for i in meteor_list_l:
    meteor_images_l.append(pygame.image.load(path.join(img_dir, i)).convert())
for i in meteor_list_ms:
    meteor_images_ms.append(pygame.image.load(path.join(img_dir, i)).convert())

player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
mob_img = pygame.image.load(path.join(img_dir, "meteorGrey_small1.png")).convert()
projectile_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()

shoot_snd = pygame.mixer.Sound(path.join(snd_dir, "lazer.wav"))
big_target_snd = pygame.mixer.Sound(path.join(snd_dir, "target hit big.wav"))
small_target_snd = pygame.mixer.Sound(path.join(snd_dir, "target hit small.wav"))
tiny_target_snd = pygame.mixer.Sound(path.join(snd_dir, "target hit tiny.wav"))

pygame.mixer.music.load(path.join(snd_dir, "BossMain.wav"))
pygame.mixer.music.play(-1)

sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
player = Player()
sprites.add(player)

explosion_anim = {"lrg": [], "small": []}
for i in range(9):
    file_name = "regularExplosion0{}.png".format(i)
    image = pygame.image.load(path.join(exp_dir, file_name)).convert()
    image.set_colorkey(BLACK)
    img_lrg = pygame.transform.scale(image, (75, 75))
    explosion_anim["lrg"].append(img_lrg)
    img_small = pygame.transform.scale(image, (30, 30))
    explosion_anim["small"].append(img_small)

for _ in range(8):
    new_mob()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or score >= 150:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -10
            if event.key == pygame.K_RIGHT:
                player.speed_x = 10

    sprites.update()
    mobs.update()
    projectiles.update()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.sheild_health -= hit.radius
        explosion = Explosion(hit.rect.center, "small")
        sprites.add(explosion)
        if player.sheild_health <= 0:
            explosion = Explosion(player.rect.center, "lrg")
            sprites.add(explosion)
            player.kill()

            t = Timer(1, stop_game)
            t.start()

        new_mob()

    group_hits = pygame.sprite.groupcollide(mobs, projectiles, True, True)
    for i in group_hits:
        score += 50 - i.radius
        size = "small"

        if i.radius <= 10:
            tiny_target_snd.play()
        elif 10 < i.radius <= 20:
            small_target_snd.play()
        else:
            size = "lrg"
            big_target_snd.play()

        explosion = Explosion(i.rect.center, size)
        sprites.add(explosion)
        new_mob()

    screen.fill(BLACK)
    screen.blit(bg, bg_rect)

    sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH // 2, 20)
    draw_shield_bar(screen, WIDTH // 2, 50, player.sheild_health)
    pygame.display.flip()

pygame.quit()
