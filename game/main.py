import random
from os import path

import pygame
from threading import Timer
from explosion import Explosion
from mob import Mob
from player import Player, player_img
from projectile import Projectile, pow_projectile_img
from boost import Boost

FPS = 60
HEIGHT = 900
WIDTH = 450
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
BAR_LENGTH = 180
BAR_HEIGHT = 15
LIFE_SIDES = 20
POPULATION = 8
SCORE = 0
LEVEL = 1
SPAWN_RATE = 4_000
IS_SPAWN_AVAILABLE = True
GAME_OVER = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test game")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")
bg_dir = path.join(img_dir, "backgrounds")

font_name = pygame.font.match_font("arial")


def shoot(pl):
    now = pygame.time.get_ticks()

    if now - pl.last_shot > pl.shoot_delay:
        pl.last_shot = now
        if pl.pow_bullets > 0 and pl.bull_type == 1:
            pow_shoot_snd.play()
            projectile = Projectile(pl.rect.centerx, pl.rect.top, "Blue")
            projectiles.add(projectile)
            sprites.add(projectile)
            pl.pow_bullets -= 1
        else:
            projectile = Projectile(pl.rect.centerx, pl.rect.top)
            projectiles.add(projectile)
            sprites.add(projectile)
            shoot_snd.play()

        pow_shoot_snd.play()


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
    mob.level = LEVEL


def draw_shield_bar(surf, x, y, pct):
    extra = 0
    full = pct
    if pct < 0:
        pct = 0
        full = 0
    elif pct > 100:
        full = 100
        extra = pct - 100
    m_bar_fullness = (full / 100) * BAR_LENGTH
    ex_bar_fullness = (extra / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, m_bar_fullness, BAR_HEIGHT)
    extra_rect = pygame.Rect(x, y, ex_bar_fullness, 0.5 * BAR_HEIGHT)

    fill_rect.center = (x, y)
    outline_rect.center = (x, y)
    extra_rect.center = (x, y + 25)

    pygame.draw.rect(surf, WHITE, outline_rect)
    pygame.draw.rect(surf, (175, 35, 100), fill_rect)
    pygame.draw.rect(surf, (100, 235, 200), extra_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        life = img.get_rect()
        life.y = y
        life.x = x + i * 50
        surf.blit(img, life)


def draw_ultra_bullets(surf, x, y, quant, img):
    for i in range(quant):
        ultra_bullet = img.get_rect()
        ultra_bullet.y = y
        ultra_bullet.x = x + i * 13
        surf.blit(img, ultra_bullet)


def draw_game_over(surf, x, y, img):
    game_over = img.get_rect()
    game_over.y = y
    game_over.x = x
    surf.blit(img, game_over)


def population_increase(val):
    global POPULATION
    POPULATION += val


lvl_bg = []
for i in range(6):
    bg = pygame.image.load(path.join(bg_dir, f"background_lvl{i + 1}.png")).convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    lvl_bg.append(bg)
bg_rect = lvl_bg[0].get_rect()

game_over_img = pygame.image.load(path.join(img_dir, "game_over_screen.png")).convert()
game_over_title = pygame.transform.scale(game_over_img, (WIDTH, 250))

lives_img = pygame.transform.scale(player_img, (30, 30))
lives_img.set_colorkey(BLACK)
pow_img = pygame.transform.scale(pow_projectile_img, (5, 10))
pow_img.set_colorkey(BLACK)

shoot_snd = pygame.mixer.Sound(path.join(snd_dir, "lazer.wav"))
pow_shoot_snd = pygame.mixer.Sound(path.join(snd_dir, "pow_lazer.wav"))
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

population_event = pygame.USEREVENT + 1

for _ in range(POPULATION):
    new_mob()

running = True
while running:
    clock.tick(FPS)

    sprites.update()
    mobs.update()
    projectiles.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or SCORE >= 1500:
            running = False
        if event.type == population_event:
            population_increase(1)
            IS_SPAWN_AVAILABLE = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -10
            if event.key == pygame.K_RIGHT:
                player.speed_x = 10
            if event.key == pygame.K_SPACE:
                shoot(player)
            if event.key == pygame.K_x:
                player.bull_type *= -1
    if len(mobs) < POPULATION:
        new_mob()
    if LEVEL < 6:
        if SCORE >= 100:
            LEVEL += 1
            population_increase(1)
            SCORE = 0
    else:
        if IS_SPAWN_AVAILABLE:
            IS_SPAWN_AVAILABLE = False
            pygame.time.set_timer(population_event, SPAWN_RATE)

    boost_gain = pygame.sprite.spritecollide(player, boosts, True, pygame.sprite.collide_circle)
    for b in boost_gain:
        if b.type == "bolt":
            if player.pow_bullets < 10:
                player.pow_bullets += 1
        if b.type == "shield":
            if player.lives == 3:
                if player.shield_health >= 50:
                    player.shield_health += 200 - player.shield_health
                else:
                    player.shield_health = 100
            elif player.lives < 3:
                player.lives += 1

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield_health -= hit.radius * 3
        explosion = Explosion(hit.rect.center, hit.random_size[1])
        sprites.add(explosion)
        if player.shield_health <= 0:
            explosion = Explosion(player.rect.center, "death")
            sprites.add(explosion)
            player.hide()
            player.lives -= 1
            player.shield_health = 100
        if player.lives == 0:
            t = Timer(0.90, stop_game)
            GAME_OVER = True
            t.start()

    group_hits = pygame.sprite.groupcollide(mobs, projectiles, False, True)
    for i in group_hits:
        hit_num = random.randint(1, 5)
        size = "small"

        if i.radius <= 10:
            tiny_target_snd.play()
        elif 10 < i.radius <= 20:
            size = "med"
            small_target_snd.play()
        else:
            size = "lrg"
            big_target_snd.play()
        for k in group_hits[i]:
            if k.type == "Red":
                i.health -= 25
            else:
                i.health -= 75
        if i.health <= 0:
            i.kill()
            SCORE += (i.radius + int(i.init_health)) // 2
            if hit_num == 1:
                boost = Boost(i.rect.center)
                boosts.add(boost)
                sprites.add(boost)

        explosion = Explosion(i.rect.center, size)
        sprites.add(explosion)

    screen.fill(BLACK)
    screen.blit(lvl_bg[LEVEL - 1], bg_rect)

    sprites.draw(screen)
    draw_text(screen, str(SCORE), 20, WIDTH // 2, 20)
    draw_text(screen, "LVL:" + str(LEVEL), 20, WIDTH // 2, 45)
    draw_shield_bar(screen, WIDTH - 100, 30, player.shield_health)
    draw_lives(screen, 30, 20, player.lives, lives_img)
    draw_ultra_bullets(screen, 35, 60, player.pow_bullets, pow_img)

    if GAME_OVER:
        draw_game_over(screen, 0, HEIGHT // 2 - 200, game_over_title)
    pygame.display.flip()

pygame.quit()
