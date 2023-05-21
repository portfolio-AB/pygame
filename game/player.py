import pygame
from os import path

HEIGHT = 900
WIDTH = 450
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

img_dir = path.join(path.dirname(__file__), "img")
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()


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
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.lives = 3
        self.last_shot = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH // 2, HEIGHT + 200)

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer >= 1000:
            self.hidden = False
            self.rect.center = (WIDTH // 2, HEIGHT - 100)

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
