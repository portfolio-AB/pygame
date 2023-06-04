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

meteor_images_l = []
meteor_images_m = []
meteor_images_s = []
meteor_list_l = ["meteorGrey_big1.png", "meteorGrey_big4.png"]
meteor_list_m = ["meteorGrey_med2.png", "meteorGrey_med2.png"]
meteor_list_s = ["meteorGrey_small1.png", "meteorGrey_tiny2.png"]
asteroids = [meteor_images_l, meteor_images_m, meteor_images_s ]

for i in meteor_list_l:
    meteor_images_l.append(pygame.image.load(path.join(img_dir, i)).convert())
for i in meteor_list_m:
    meteor_images_m.append(pygame.image.load(path.join(img_dir, i)).convert())
for i in meteor_list_s:
    meteor_images_s.append(pygame.image.load(path.join(img_dir, i)).convert())


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
            self.health = 75
        elif self.random_size == meteor_images_m:
            self.speed_y = randrange(1, 4)
            self.speed_x = randrange(-1, 1)
            self.health = 50
        else:
            self.speed_y = randrange(2, 5)
            self.speed_x = randrange(-1, 1)
            self.health = 25
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
