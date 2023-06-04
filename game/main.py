import random
from os import path

import pygame
from threading import Timer
from explosion import Explosion
from mob import Mob
from player import Player, player_img
from projectile import Projectile
from boost import Boost

FPS = 60
HEIGHT = 900
WIDTH = 450
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
BAR_LENGTH = 180
BAR_HEIGHT = 15
LIFE_SIDES = 20
score = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test game")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")


def shoot(pl):
    now = pygame.time.get_ticks()

    if now - pl.last_shot > pl.shoot_delay:
        pl.last_shot = now
        projectile = Projectile(pl.rect.centerx, pl.rect.top)
        projectiles.add(projectile)
        sprites.add(projectile)
        shoot_snd.play()


font_name = pygame.font.match_font("arial")


def stop_game():
    global running
    running = False


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def new_mob():
    mob = Mob()
    mobs.add(mob)
    sprites.add(mob)


def draw_shield_bar(surf, x, y, pct):
    extra = 0
    full = pct
    if pct < 0:
        pct = 0
        full = 0
    elif pct > 100:
        full = 100
        extra = pct - 100
    bar_fullness = (full / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, bar_fullness, BAR_HEIGHT)

    fill_rect.center = (x, y)
    outline_rect.center = (x, y)

    pygame.draw.rect(surf, WHITE, outline_rect)
    pygame.draw.rect(surf, (175 - extra, 35 + (2*extra), 100 + extra), fill_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        life = img.get_rect()
        life.y = y
        life.x = x + i * 50
        surf.blit(img, life)


bg = pygame.image.load(path.join(img_dir, "darkPurple.png")).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg_rect = bg.get_rect()

lives_img = pygame.transform.scale(player_img, (30, 30))
lives_img.set_colorkey(BLACK)

shoot_snd = pygame.mixer.Sound(path.join(snd_dir, "lazer.wav"))
big_target_snd = pygame.mixer.Sound(path.join(snd_dir, "target hit big.wav"))
small_target_snd = pygame.mixer.Sound(path.join(snd_dir, "target hit small.wav"))
tiny_target_snd = pygame.mixer.Sound(path.join(snd_dir, "target hit tiny.wav"))

pygame.mixer.music.load(path.join(snd_dir, "BossMain.wav"))
pygame.mixer.music.play(-1)

sprites = pygame.sprite.Group()
boosts = pygame.sprite.Group()
mobs = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
player = Player()
sprites.add(player)

for _ in range(8):
    new_mob()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or score >= 1500:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -10
            if event.key == pygame.K_RIGHT:
                player.speed_x = 10
            if event.key == pygame.K_SPACE:
                shoot(player)

    sprites.update()
    mobs.update()
    projectiles.update()

    boost_gain = pygame.sprite.spritecollide(player, boosts, True, pygame.sprite.collide_circle)
    for b in boost_gain:
        if b.type == "bolt":
            pass
        if b.type == "shield":
            if player.lives == 3 and player.sheild_health <= 100:
                player.sheild_health += 100
            elif player.lives < 3:
                player.lives += 1

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.sheild_health -= hit.radius
        explosion = Explosion(hit.rect.center, "small")
        sprites.add(explosion)
        if player.sheild_health <= 0:
            explosion = Explosion(player.rect.center, "lrg")
            sprites.add(explosion)
            player.hide()
            player.lives -= 1
            player.sheild_health = 100
        if player.lives == 0:
            t = Timer(0.90, stop_game)
            t.start()

        new_mob()

    group_hits = pygame.sprite.groupcollide(mobs, projectiles, False, True)
    for i in group_hits:
        hit_num = random.randint(1,1)
        size = "small"

        if i.radius <= 10:
            tiny_target_snd.play()
        elif 10 < i.radius <= 20:
            size = "med"
            small_target_snd.play()
        else:
            size = "lrg"
            big_target_snd.play()
        i.health -= 25
        if i.health <= 0:
            i.kill()
            new_mob()
            score += i.radius
            if hit_num == 1:
                boost = Boost(i.rect.center)
                boosts.add(boost)
                sprites.add(boost)

        explosion = Explosion(i.rect.center, size)
        sprites.add(explosion)

    screen.fill(BLACK)
    screen.blit(bg, bg_rect)

    sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH // 2, 20)
    draw_shield_bar(screen, WIDTH - 100, 30, player.sheild_health)
    draw_lives(screen, 30, 20, player.lives, lives_img)
    pygame.display.flip()

pygame.quit()
