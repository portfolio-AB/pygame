import pygame
from os import path
import random
from random import randrange

HEIGHT = 900
WIDTH = 450
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

img_dir = path.join(path.dirname(__file__), "img")
boost_img = {"shield": pygame.image.load(path.join(img_dir, "shield_gold.png")).convert(),
             "bolt": pygame.image.load(path.join(img_dir, "bolt_gold.png")).convert()}


class Boost(pygame.sprite.Sprite):
    def __init__(self, centre):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'bolt'])
        self.image = boost_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = centre
        self.speed_y = 4

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.top > HEIGHT:
            self.kill()
