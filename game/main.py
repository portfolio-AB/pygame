import random

import pygame
from os import path
from random import randint, randrange

FPS = 60
HEIGHT = 900
WIDTH = 450
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
score = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test game")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(0.9 * self.rect.width / 2)
        # pygame.draw.circle(self.image, (250, 250, 250), self.rect.center, self.radius)
        self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.speed_x = 0
        self.rot = 0

    def colour_change(self):
        self.image.fill((randint(0, 255), randint(0, 255), randint(0, 255)))

    def update(self):
        self.speed_x = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speed_x = -10
        if key_state[pygame.K_RIGHT]:
            self.speed_x = 10

        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top)
        projectiles.add(projectile)
        sprites.add(projectile)
        shoot_snd.play()


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
        # pygame.draw.circle(self.image, (250, 250, 250), self.rect.center, self.radius)
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


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 25))
        self.image.set_colorkey(BLACK)
        self.image = projectile_img
        self.rect = self.image.get_rect()
        self.speed_y = -15
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.top < 0:
            self.kill()


font_name = pygame.font.match_font("arial")


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


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

pygame.mixer.music.load(path.join(snd_dir,"BossMain.wav"))
pygame.mixer.music.play(-1)




sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
player = Player()
sprites.add(player)
for i in range(8):
    mob = Mob()
    mobs.add(mob)
    sprites.add(mob)

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
            if event.key == pygame.K_SPACE:
                player.shoot()

    sprites.update()
    mobs.update()
    projectiles.update()
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False
    group_hits = pygame.sprite.groupcollide(mobs, projectiles, True, True)
    for i in group_hits:
        score += 50 - i.radius

        if i.radius <=10:
            tiny_target_snd.play()
        elif 10< i.radius <=20:
            small_target_snd.play()
        else:
            big_target_snd.play()

        mob = Mob()
        mobs.add(mob)
        sprites.add(mob)

    screen.fill(BLACK)
    screen.blit(bg, bg_rect)

    sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH // 2, 20)
    pygame.display.flip()

pygame.quit()
