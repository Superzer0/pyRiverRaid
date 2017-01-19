# Pygame template - skeleton for a new pygame project
import os
import random
from objects.context import Context
from objects.enemy import Enemy
from objects.explosion import Explosion
from objects.mobs.randommeteor import RandomMeteor
from objects.mobs.rotatingmeteor import RotatingMeteor
from objects.player import *
from objects.powerup import Powerup
from objects.resource import Resource
from objects.settings import *
from os import path

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("New River Raid")
clock = pygame.time.Clock()

resource = Resource()
context = Context();


for i in range(9):
    # regular explosion
    img = resource.load_explosions_animations(resource.img_dir, 'regularExplosion0{}.png', i)

    img_lg = pygame.transform.scale(img, (75, 75))
    resource.explosion_animations['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    resource.explosion_animations['sm'].append(img_sm)

    # player explosion
    img = resource.load_explosions_animations(resource.img_dir, 'sonicExplosion0{}.png', i)
    resource.explosion_animations['player'].append(img)

player = Player(resource, context)
context.all_sprites.add(player)
context.player = player



# left obstacles
for i in range(100):
    context.new_obstacle(i, random.randrange(0, WIDTH_OBSTACLES - 50))

# right obstacles
for i in range(100):
    context.new_obstacle(i, random.randrange(WIDTH - WIDTH_OBSTACLES - 50, WIDTH - 10))


# for i in range(20):
#     new_mob()

for i in range(5):
    context.new_enemy()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(resource.font_name, size)
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


def show_go_screen():
    screen.blit(resource.background, resource.background_rect)
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
    player_explosion = Explosion(hit.rect.center, 'sm', resource.explosion_animations)
    random.choice(resource.explosion_sounds).play()
    context.all_sprites.add(player_explosion)
    if is_terminal_hit:
        resource.player_die_sound.play()
        death_explosion = Explosion(player.rect.center, 'player', resource.explosion_animations)
        context.all_sprites.add(death_explosion)
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
        context.mobs.empty()
        context.enemies.empty()
        context.all_sprites.empty()

    # Update
    context.all_sprites.update(screen)

    hits = pygame.sprite.groupcollide(context.mobs, context.bullets, True, True)
    for hit in hits:
        random.choice(explosion_sounds).play()
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center, 'lg', explosion_animations)
        all_sprites.add(expl)
        # if random.random() > 0.9:
        #     pow = Powerup(hit.rect.center, power_up_images)
        #     all_sprites.add(pow)
        #     powerups.add(pow)

        new_mob()

    # generate random fuel
    if player.fuel < 50 and random.random() > 0.001:
        fuel = Powerup((random.randint(200, WIDTH - 200), 0), 'fuel', resource.power_up_images)
        context.powerups.add(fuel)
        context.all_sprites.add(fuel)

    # generate random shield
    if random.random() > 0.0001:
        shield = Powerup((random.randint(200, WIDTH - 200), 0), 'shield', resource.power_up_images)
        context.powerups.add(shield)
        context.all_sprites.add(shield)

    hits = pygame.sprite.spritecollide(player, context.mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        game_over = player_collide(hit, lambda: context.new_mob())

    hits = pygame.sprite.spritecollide(player, context.obstacles, True, pygame.sprite.collide_circle)
    for hit in hits:
        game_over = player_collide(hit, lambda: context.new_obstacle(1, hit.rect.x))

    hits = pygame.sprite.spritecollide(player, context.powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.recover()
        if hit.type == 'gun':
            player.power_up()
        if hit.type == 'fuel':
            player.recharge_fuel()

    hits = pygame.sprite.groupcollide(context.powerups, context.bullets, True, True)
    for hit in hits:
        context.playerCanShot = True
        random.choice(resource.explosion_sounds).play()
        expl = Explosion(hit.rect.center, 'sm', resource.explosion_animations)
        context.all_sprites.add(expl)

    # check to see if a enemy hit the player
    hits = pygame.sprite.spritecollide(player, context.enemies, True)
    if hits:
        context.playerCanShot = True
        hit = hits[0]
        game_over = player_collide(hit, lambda: context.new_obstacle(1, hit.rect.x))
        context.new_enemy()

    # check to see if a enemy's shot hit the player
    hits = pygame.sprite.spritecollide(player, context.enemies_shots, True, pygame.sprite.collide_circle)
    for hit in hits:
        game_over = player_collide(hit, lambda: context.new_enemy())

    # check to see if a player's shot hit the enemy
    hits = pygame.sprite.groupcollide(context.enemies, context.bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        context.playerCanShot = True
        death_explosion = Explosion(hit.rect.center, 'player', resource.explosion_animations)
        context.all_sprites.add(death_explosion)
        hit.kill()
        if len(context.enemies.sprites()) <= MAX_ENEMIES:
            context.new_enemy()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(resource.background, resource.background_rect)
    context.all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH / 2, 20)

    draw_text(screen, "SHIELD", 16, 35, 7)
    draw_shield_bar(screen, GREEN, 70, 10, player.shield)

    draw_text(screen, "FUEL ", 16, 35, 27)
    draw_shield_bar(screen, RED, 70, 31, player.fuel)

    draw_lives(screen, WIDTH - 100, 5, player.lives, resource.player_mini_img)

    if game_over:
        draw_text(screen, "Game over", 50, WIDTH // 2, HEIGHT // 2 - 70)
        draw_text(screen, str(score), 50, WIDTH // 2, HEIGHT // 2)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
