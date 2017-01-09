# Pygame template - skeleton for a new pygame project
import os
import random
from os import path

import pygame

from objects.explosion import Explosion
from objects.mob import Mob
from objects.player import *
from objects.settings import *

# set up asset folders


game_folder = path.join(os.path.dirname(__file__), 'resources')
img_dir = path.join(game_folder, 'img')
snd_dir = path.join(game_folder, 'snd')

# initialize pygame and create window
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, random.choice(['sfx_laser1.ogg', 'sfx_laser2.ogg'])))
explosion_sounds = [pygame.mixer.Sound(path.join(snd_dir, snd)) for snd in ['expl3.wav', 'expl6.wav']]
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()

meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, 'Explosions_kenney', filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player(player_img, bullet_img, shoot_sound, all_sprites, bullets)

all_sprites.add(player)
font_name = pygame.font.match_font('arial')


def new_mob():
    m = Mob(meteor_images)
    all_sprites.add(m)
    mobs.add(m)


for i in range(8):
    new_mob()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGTH = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGTH)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGTH)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


# Game loop
running = True
game_over = False
score = 0
pygame.mixer.music.play(loops=-1)

while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False


    if game_over:
        mobs.empty()
        all_sprites.empty()

    # Update
    all_sprites.update(screen)

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        random.choice(explosion_sounds).play()
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center, 'lg', explosion_anim)
        all_sprites.add(expl)
        new_mob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        new_mob()
        expl = Explosion(hit.rect.center, 'sm', explosion_anim)
        random.choice(explosion_sounds).play()
        all_sprites.add(expl)
        if player.shield <= 0:
            game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH // 2, 20)
    draw_shield_bar(screen, 7, 7, player.shield)

    if game_over:
        draw_text(screen, "Game over", 50, WIDTH // 2, HEIGHT // 2 - 70)
        draw_text(screen, str(score), 50, WIDTH // 2, HEIGHT // 2)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
