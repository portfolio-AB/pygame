import pygame
from os import path

HEIGHT = 900
WIDTH = 450
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
img_dir = path.join(path.dirname(__file__), "img")
exp_dir = path.join(img_dir, "explosion_anim")


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


explosion_anim = {"lrg": [], "med": [], "small": []}
for i in range(9):
    file_name = "regularExplosion0{}.png".format(i)
    image = pygame.image.load(path.join(exp_dir, file_name)).convert()
    image.set_colorkey(BLACK)
    img_lrg = pygame.transform.scale(image, (75, 75))
    explosion_anim["lrg"].append(img_lrg)
    img_med = pygame.transform.scale(image, (45, 45))
    explosion_anim["med"].append(img_med)
    img_small = pygame.transform.scale(image, (30, 30))
    explosion_anim["small"].append(img_small)

image = pygame.image.load(path.join(exp_dir, file_name)).convert()
