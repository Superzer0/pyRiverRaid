import pygame
from objects.bullet import Bullet
from objects.explosion import Explosion
from objects.resource import Resource
from objects.settings import *


class Player(pygame.sprite.Sprite):
    shield_max_value = 100
    fuel_max_value = 100
    shoot_delay = 250
    max_hidden_time = 1000

    def __init__(self, resource, context):
        pygame.sprite.Sprite.__init__(self)
        self.player_power_up_img = resource.player_power_up_img
        self.explosion_animations = resource.explosion_animations
        self.player_org_img = resource.player_img
        self.bullets = context.bullets
        self.all_sprites = context.all_sprites
        self.shoot_sound = resource.shoot_sound
        self.bullet_img = resource.bullet_img
        self.set_player_img(resource.player_img, WIDTH / 2, HEIGHT - 10)
        self.speedx = 0
        self.lives = 3
        self.power = 1
        self.fuel = Player.fuel_max_value
        self.hidden = False
        self.shield = Player.shield_max_value
        self.last_shot = pygame.time.get_ticks()
        self.hidden_time = pygame.time.get_ticks()
        self.power_time = pygame.time.get_ticks()
        self.context = context

    def set_player_img(self, player_img, x, y):
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self, *args):

        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            if self.power == 1:
                self.set_player_img(self.player_org_img, self.rect.centerx, self.rect.bottom)

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hidden_time > Player.max_hidden_time:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
        if self.rect.right > WIDTH - WIDTH_OBSTACLES:
            self.rect.right = WIDTH - WIDTH_OBSTACLES
        if self.rect.left < WIDTH_OBSTACLES:
            self.rect.left = WIDTH_OBSTACLES

        self.fuel -= 0.2
        if self.fuel < 0:
            # destroy yourself
            # self.player_die_sound.play()
            self.fuel = 100
            death_explosion = Explosion(self.rect.center, 'player', self.explosion_animations)
            self.context.all_sprites.add(death_explosion)
            self.hide()

    def hide(self):
        self.hidden = True
        self.hidden_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH, HEIGHT + 200)

    def power_up(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        self.set_player_img(self.player_power_up_img, self.rect.centerx, self.rect.bottom)

    def shoot(self):
        if self.context.playerCanShot:
            self.context.playerCanShot = False
            if self.hidden:
                return

            now = pygame.time.get_ticks()
            if now - self.last_shot > Player.shoot_delay:
                self.last_shot = now
                if self.power == 1:
                    bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_img, self.context)
                    self.context.all_sprites.add(bullet)
                    self.context.bullets.add(bullet)
                    self.shoot_sound.play()
                if self.power >= 2:
                    bullet1 = Bullet(self.rect.left, self.rect.centery, self.bullet_img)
                    bullet2 = Bullet(self.rect.right, self.rect.centery, self.bullet_img)
                    self.context.all_sprites.add(bullet1)
                    self.context.all_sprites.add(bullet2)
                    self.context.bullets.add(bullet1)
                    self.context.bullets.add(bullet2)
                    self.shoot_sound.play()

    def was_hit(self, impact):
        """
        Changes player internal state after being hit.
        @returns information if player live was lost
        """
        self.shield -= impact
        if self.shield < 0:
            self.lives -= 1
            if self.lives > 0:
                self.shield = 100
            return True
        else:
            return False

    def is_alive(self):
        """ Returns information if player have enough lives to continue game. """
        if self.lives < 1:
            return False
        else:
            return True

    def recharge_fuel(self):
        self.fuel = Player.fuel_max_value

    def recover(self):
        self.shield = Player.shield_max_value

    def destroy(self):
        pass
