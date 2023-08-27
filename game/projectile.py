import pygame
from os import path

HEIGHT = 900
WIDTH = 450
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

img_dir = path.join(path.dirname(__file__), "img")
projectile_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()
pow_projectile_img = pygame.image.load(path.join(img_dir, "laserBlue01.png")).convert()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, type="Red"):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 25))
        self.image.set_colorkey(BLACK)
        self.type = type
        if type == "Red":
            self.image = projectile_img
        elif type == "Blue":
            self.image = pow_projectile_img
        self.rect = self.image.get_rect()
        self.speed_y = -15
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.top < 0:
            self.kill()
