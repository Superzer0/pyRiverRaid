# Pygame template - skeleton for a new pygame project
import os
import random
from os import path

from objects.explosion import Explosion
from objects.mobs.randommeteor import RandomMeteor
from objects.mobs.rotatingmeteor import RotatingMeteor
from objects.player import *
from objects.powerup import Powerup
from objects.settings import *

# set up asset folders


game_folder = path.join(os.path.dirname(__file__), 'resources')
img_dir = path.join(game_folder, 'img')
snd_dir = path.join(game_folder, 'snd')
misc_dir = path.join(game_folder, 'misc')

# initialize pygame and create window
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("New River Raid")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, random.choice(['sfx_laser1.ogg', 'sfx_laser2.ogg'])))
explosion_sounds = [pygame.mixer.Sound(path.join(snd_dir, snd)) for snd in ['expl3.wav', 'expl6.wav']]
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip2_blue.png")).convert()
player_power_up_img = pygame.image.load(path.join(img_dir, "playerShip3_blue.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()

meteors_file_names_list = ['meteor_big1.png', 'meteor_big2.png', 'meteor_big3.png', 'meteor_big4.png',
                           'meteor_med1.png',
                           'meteor_med2.png', 'meteor_small1.png', 'meteor_small2.png',
                           'meteor_tiny1.png', 'meteor_tiny2.png']

meteor_mobs_images = [pygame.image.load(path.join(img_dir, 'meteors', 'brown', img)).convert() for img in
                      meteors_file_names_list]

meteor_obstacles_images = [pygame.image.load(path.join(img_dir, 'meteors', 'grey', img)).convert() for img in
                           meteors_file_names_list]

explosion_animations = {'lg': [], 'sm': [], 'player': []}

player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

power_up_images = {'shield': pygame.image.load(path.join(img_dir, 'powerups', 'shield_gold.png')).convert(),
                   'gun': pygame.image.load(path.join(img_dir, 'powerups', 'bolt_gold.png')).convert()}


def load_explosions_animations(image_directory, filename_prefix):
    img_filename = filename_prefix.format(i)
    explosion_image = pygame.image.load(path.join(image_directory, 'Explosions_kenney', img_filename)).convert()
    explosion_image.set_colorkey(BLACK)
    return explosion_image


for i in range(9):
    # regular explosion
    img = load_explosions_animations(img_dir, 'regularExplosion0{}.png')

    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_animations['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_animations['sm'].append(img_sm)

    # player explosion
    img = load_explosions_animations(img_dir, 'sonicExplosion0{}.png')
    explosion_animations['player'].append(img)

mobs = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player(player_img, player_power_up_img, bullet_img, shoot_sound, all_sprites, bullets)
powerups = pygame.sprite.Group()
all_sprites.add(player)
font_name = path.join(misc_dir, 'kenvector_future_thin.ttf')


def new_mob():
    m = RandomMeteor(meteor_mobs_images)
    all_sprites.add(m)
    mobs.add(m)


def new_obstacle(i, start_x):
    m = RotatingMeteor(meteor_obstacles_images, start_x,
                       random.randrange(-300, (15 * i)), 0, random.randrange(1, 2), random.randrange(-2, 2))
    all_sprites.add(m)
    obstacles.add(m)


# left obstacles
for i in range(100):
    new_obstacle(i, random.randrange(0, WIDTH_OBSTACLES - 50))

# right obstacles
for i in range(100):
    new_obstacle(i, random.randrange(WIDTH - WIDTH_OBSTACLES - 50, WIDTH - 10))


# for i in range(20):
#     new_mob()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, player_live_img):
    for live in range(lives):
        img_rect = player_live_img.get_rect()
        img_rect.x = x + 30 * live
        img_rect.y = y
        surf.blit(player_live_img, img_rect)


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


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Space river raid", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


show_go_screen()

# Game loop
running = True
game_over = False
score = 0
pygame.mixer.music.play(loops=-1)


def player_collide(hit, new_object_fun):
    is_terminal_hit = player.was_hit(hit.radius * 2)
    new_object_fun()
    player_explosion = Explosion(hit.rect.center, 'sm', explosion_animations)
    random.choice(explosion_sounds).play()
    all_sprites.add(player_explosion)
    if is_terminal_hit:
        player_die_sound.play()
        death_explosion = Explosion(player.rect.center, 'player', explosion_animations)
        all_sprites.add(death_explosion)
        player.hide()
        if not player.is_alive() and death_explosion.alive():
            return True
    return False


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
        expl = Explosion(hit.rect.center, 'lg', explosion_animations)
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Powerup(hit.rect.center, power_up_images)
            all_sprites.add(pow)
            powerups.add(pow)

        new_mob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        game_over = player_collide(hit, lambda: new_mob())

    hits = pygame.sprite.spritecollide(player, obstacles, True, pygame.sprite.collide_circle)
    for hit in hits:
        game_over = player_collide(hit, lambda: new_obstacle(1, hit.rect.x))

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.power_up()

    hits = pygame.sprite.groupcollide(powerups, bullets, True, True)
    for hit in hits:
        random.choice(explosion_sounds).play()
        expl = Explosion(hit.rect.center, 'sm', explosion_animations)
        all_sprites.add(expl)

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH // 2, 20)
    draw_shield_bar(screen, 7, 7, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    if game_over:
        draw_text(screen, "Game over", 50, WIDTH // 2, HEIGHT // 2 - 70)
        draw_text(screen, str(score), 50, WIDTH // 2, HEIGHT // 2)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
