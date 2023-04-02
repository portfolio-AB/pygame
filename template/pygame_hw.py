import pygame
from random import randint
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.up = False
        self.down = False
        self.left = False
        self.right = True

    def colour_change(self):
        self.image.fill((randint(0, 255), randint(0, 255), randint(0, 255)))

    def direction_change(self, right, left, up, down):
        self.right = right
        self.left = left
        self.up = up
        self.down = down

    def update(self):
        if self.rect.bottom + 10 > HEIGHT and self.rect.right + 10 > WIDTH:
            self.direction_change(False, True, False, False)

        elif self.rect.top - 10 < 0 and self.rect.left - 10 < 0:
            self.direction_change(True, False, False, False)

        if self.rect.right + 10 > WIDTH and self.rect.top - 10 < 0:
            self.direction_change(False, False, False, True)

        elif self.rect.left - 10 < 0 and self.rect.bottom + 10 > HEIGHT:
            self.direction_change(False, False, True, False)

        if self.left:
            self.rect.x -= 5
        if self.right:
            self.rect.x += 5

        if self.up:
            self.rect.y -= 5
        if self.down:
            self.rect.y += 5


WIDTH = 800
HEIGHT = 450
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test game")
clock = pygame.time.Clock()
sprites = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "../game/img")
img = pygame.image.load(os.path.join(img_folder, "")).convert()

player = Player()
sprites.add(player)


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sprites.update()
    screen.fill((15, 7, 21))

    sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
