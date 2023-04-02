import pygame
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((120, 12, 55))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.up = True
        self.left = True

    def colour_change(self):
        self.image.fill((randint(0, 255), randint(0, 255), randint(0, 255)))

    def update(self):
        # self.rect.x +=5
        # if self.rect.left > WIDTH:
        #     self.rect.right = 0

        # self.rect.y += 5
        # if self.rect.top > HEIGHT:
        #     self.rect.bottom = 0

        if self.rect.bottom > HEIGHT:
            self.up = True
            self.colour_change()
        elif self.rect.top < 0:
            self.up = False
            self.colour_change()

        if self.up:
            self.rect.y -= 5
        else:
            self.rect.y += 5

        if self.rect.right > WIDTH:
            self.left = True
            self.colour_change()
        elif self.rect.left < 0:
            self.left = False
            self.colour_change()

        if self.left:
            self.rect.x -= 5
        else:
            self.rect.x += 5


WIDTH = 800
HEIGHT = 450
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test game")
clock = pygame.time.Clock()
sprites = pygame.sprite.Group()
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
