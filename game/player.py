import pygame
from os import path
from projectile import Projectile

HEIGHT = 900
WIDTH = 450
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
shoot_snd = pygame.mixer.Sound(path.join(snd_dir, "lazer.wav"))

sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
mobs = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(0.9 * self.rect.width / 2)
        self.rect.center = (WIDTH / 2, HEIGHT - 100)
        self.speed_x = 0
        self.rot = 0
        self.sheild_health = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speed_x = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speed_x = -10
        if key_state[pygame.K_RIGHT]:
            self.speed_x = 10
        if key_state[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            projectile = Projectile(self.rect.centerx, self.rect.top)
            projectiles.add(projectile)
            sprites.add(projectile)
            shoot_snd.play()
