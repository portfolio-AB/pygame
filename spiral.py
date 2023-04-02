import pygame
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((120, 12, 55))
        self.rect = self.image.get_rect()
        self.rect.center = (20, 20)
        self.up = False
        self.down = False
        self.left = False
        self.right = True
        self.border_change = 10
        self.top_border = 0
        self.bottom_border = HEIGHT
        self.left_border = 0
        self.right_border = WIDTH

    def colour_change(self):
        self.image.fill((randint(0, 255), randint(0, 255), randint(0, 255)))

    def direction_change(self, right, left, up, down):
        self.right = right
        self.left = left
        self.up = up
        self.down = down

    def update(self):
        if self.rect.bottom > self.bottom_border and self.rect.right > self.right_border:
            self.direction_change(False, True, False, False)

        if self.rect.top < self.top_border and self.rect.left < self.left_border:
            self.direction_change(True, False, False, False)

        if self.rect.right > self.right_border and self.rect.top < self.top_border:
            self.direction_change(False, False, False, True)

        if self.rect.left < self.left_border and self.rect.bottom > self.bottom_border:
            self.direction_change(False, False, True, False)


        if self.left:
            self.rect.x -= 5
        if self.right:
            self.rect.x += 5

        if self.up:
            self.rect.y -= 5
        if self.down:
            self.rect.y += 5

        # if self.border < WIDTH // 2 and self.border < HEIGHT // 2 and self.loop % 8 == 0:
        #     self.border += 30
        #
        # else:
        #     self.border = self.border


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
