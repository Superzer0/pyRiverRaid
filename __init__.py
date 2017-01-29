# Pygame template - skeleton for a new pygame project
import configparser
import os

from objects.enemy import Enemy
from objects.explosion import Explosion
from objects.mobs.randommeteor import RandomMeteor
from objects.mobs.rotatingmeteor import RotatingMeteor
from objects.player import *
from objects.powerup_generators import *
from objects.resources.ImgResources import ImgResources
from objects.resources.MiscResources import MiscResources
from objects.resources.ResourcesContext import ResourceContext
from objects.resources.SoundResources import SoundResources
from objects.settings import *
from objects.spritescontext import SpritesContext

# set up asset folders

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

resourceContext = ResourceContext()

try:
    game_folder = os.path.dirname(__file__)
    config = configparser.ConfigParser()
    config.read('resources.ini')
    # initialize pygame and create window

    resourceContext.soundResources = SoundResources(game_folder, config)
    resourceContext.soundResources.load_default_music()
    resourceContext.miscResources = MiscResources(game_folder, config)
    resourceContext.imgResources = ImgResources(game_folder, config)
except IOError:
    print("Cannot load resources.")
    raise  # TODO: add logging here


pygame.display.set_caption("Space Raid")
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies_shots = pygame.sprite.Group()
context = SpritesContext(mobs, obstacles, bullets, powerups, enemies, enemies_shots)
player = Player(resourceContext.imgResources, resourceContext.soundResources, all_sprites, bullets, context)
shieldGenerator = ShieldGenerator(player, resourceContext.imgResources, all_sprites, powerups)
fuelGenerator = FuelGenerator(player, resourceContext.imgResources, all_sprites, powerups)

all_sprites.add(player)

context._player = player


def new_mob():
    m = RandomMeteor(resourceContext.imgResources.meteor_mobs_img)
    all_sprites.add(m)
    mobs.add(m)


def new_obstacle(i, start_x):
    m = RotatingMeteor(resourceContext.imgResources.meteor_obstacles_img, start_x,
                       random.randrange(-300, (15 * i)), 0, random.randrange(1, 2), random.randrange(-2, 2))
    all_sprites.add(m)
    obstacles.add(m)


def new_enemy():
    enemy = Enemy(all_sprites, enemies, enemies_shots, resourceContext.imgResources)
    enemies.add(enemy)
    all_sprites.add(enemy)


# left obstacles
for i in range(100):
    new_obstacle(i, random.randrange(0, WIDTH_OBSTACLES - 50))

# right obstacles
for i in range(100):
    new_obstacle(i, random.randrange(WIDTH - WIDTH_OBSTACLES - 50, WIDTH - 10))

# for i in range(20):
#     new_mob()

for i in range(5):
    new_enemy()


def draw_text(surf, text, size, x, y):
    font = resourceContext.miscResources.get_font(size)
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


def draw_shield_bar(surf, color, x, y, pct):
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGTH = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGTH)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGTH)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def show_go_screen(imgResources):
    screen.blit(imgResources.background, imgResources.background.get_rect())
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


show_go_screen(resourceContext.imgResources)

# Game loop
running = True
game_over = False
score = 0
pygame.mixer.music.play(loops=-1)


def player_collide(hit, new_object_fun):
    is_terminal_hit = player.was_hit(hit.radius * 2)
    new_object_fun()
    player_explosion = Explosion(hit.rect.center, ImgResources.EXPLOSION_ANIMATIONS_SM,
                                 resourceContext.imgResources.explosion_animations)
    random.choice(resourceContext.soundResources.explosion_sounds).play()
    all_sprites.add(player_explosion)
    if is_terminal_hit:
        print("terminated by:" + str(hit))
        resourceContext.soundResources.player_die_sound.play()
        death_explosion = Explosion(player.rect.center, ImgResources.EXPLOSION_ANIMATIONS_PLAYER,
                                    resourceContext.imgResources.explosion_animations)
        all_sprites.add(death_explosion)
        player.recharge_fuel()
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
        enemies.empty()
        all_sprites.empty()

    # Update
    all_sprites.update(screen)

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        random.choice(resourceContext.soundResources.explosion_sounds).play()
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center, resourceContext.imgResources.EXPLOSION_ANIMATIONS_LG,
                         resourceContext.imgResources.explosion_animations)
        all_sprites.add(expl)
        shieldGenerator.generate()
        new_mob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        game_over = player_collide(hit, lambda: new_mob())

    hits = pygame.sprite.spritecollide(player, obstacles, True, pygame.sprite.collide_circle)
    for hit in hits:
        game_over = player_collide(hit, lambda: new_obstacle(1, hit.rect.x))

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        player.power_up(hit.type)

    hits = pygame.sprite.groupcollide(powerups, bullets, True, True)
    for hit in hits:
        random.choice(resourceContext.soundResources.explosion_sounds).play()
        expl = Explosion(hit.rect.center, resourceContext.imgResources.EXPLOSION_ANIMATIONS_SM,
                         resourceContext.imgResources.explosion_animations)
        all_sprites.add(expl)
        context.playerCanShot = True

    # check to see if a enemy hit the player
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        hit = hits[0]
        game_over = player_collide(hit, lambda: new_obstacle(1, hit.rect.x))
        new_enemy()

    # check to see if a enemy's shot hit the player
    hits = pygame.sprite.spritecollide(player, enemies_shots, True, pygame.sprite.collide_circle)
    for hit in hits:
        game_over = player_collide(hit, lambda: new_enemy())

    # check to see if a player's shot hit the enemy
    hits = pygame.sprite.groupcollide(enemies, bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        context.playerCanShot = True
        death_explosion = Explosion(hit.rect.center, resourceContext.imgResources.EXPLOSION_ANIMATIONS_PLAYER,
                                    resourceContext.imgResources.explosion_animations)
        all_sprites.add(death_explosion)
        hit.kill()
        if len(enemies.sprites()) <= MAX_ENEMIES:
            new_enemy()

    if player.fuel < 0:
        resourceContext.soundResources.player_die_sound.play()
        death_explosion = Explosion(player.rect.center, ImgResources.EXPLOSION_ANIMATIONS_PLAYER,
                                    resourceContext.imgResources.explosion_animations)
        all_sprites.add(death_explosion)
        actual_lives = player.lives - 1
        if death_explosion.alive():
            player.lives = actual_lives
            player.hide()
            player.recharge_fuel()
            player.recover()

    fuelGenerator.generate()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(resourceContext.imgResources.background, resourceContext.imgResources.background.get_rect())
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH / 2, 20)

    draw_text(screen, "SHIELD", 16, 35, 7)
    draw_shield_bar(screen, GREEN, 70, 10, player.shield)

    draw_text(screen, "FUEL ", 16, 35, 27)
    draw_shield_bar(screen, RED, 70, 31, player.fuel)

    draw_lives(screen, WIDTH - 100, 5, player.lives, resourceContext.imgResources.player_mini_img)

    if game_over:
        draw_text(screen, "Game over", 50, WIDTH // 2, HEIGHT // 2 - 70)
        draw_text(screen, str(score), 50, WIDTH // 2, HEIGHT // 2)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
