import pygame
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((120, 12, 55))
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 5
        self.up = False
        self.down = False
        self.left = False
        self.right = True
        self.speed = 20
        self.border_change = 30
        self.top_border = 0
        self.bottom_border = HEIGHT
        self.left_border = 0
        self.right_border = WIDTH

    #  this is an experiment

    def colour_change(self):
        self.image.fill((randint(0, 255), randint(0, 255), randint(0, 255)))

    def direction_change(self, right, down, left, up):
        self.right = right
        self.left = left
        self.up = up
        self.down = down

    def update(self):
        if self.bottom_border - self.top_border <= 0 or self.right_border - self.left_border <= 0:
            return

        if self.left:
            self.rect.x -= self.speed
            if self.rect.left <= self.left_border:
                self.direction_change(False, False, False, True)
                self.left_border += self.border_change
                return

        if self.right:
            self.rect.x += self.speed
            if self.rect.right >= self.right_border:
                self.direction_change(False, True, False, False)
                self.right_border -= self.border_change
                return

        if self.up:
            self.rect.y -= self.speed
            if self.rect.top <= self.top_border:
                self.direction_change(True, False, False, False)
                self.top_border += self.border_change
                return

        if self.down:
            self.rect.y += self.speed
            if self.rect.bottom >= self.bottom_border:
                self.direction_change(False, False, True, False)
                self.bottom_border -= self.border_change
                return


WIDTH = 450
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
