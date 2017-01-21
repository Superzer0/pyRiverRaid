import pygame
import random
from objects.bullet import Bullet
from objects.resources.ImgResources import ImgResources
from objects.settings import *


class Player(pygame.sprite.Sprite):
    shield_max_value = 100
    fuel_max_value = 100
    fuel_consumption = 0.2
    shoot_delay = 250
    max_hidden_time = 1000

    def __init__(self, imgResources, soundResources, all_sprites, bullets):
        pygame.sprite.Sprite.__init__(self)
        self.__player_power_up_img = imgResources.power_player_img
        self.__player_org_img = imgResources.player_img
        self.__bullets = bullets
        self.__all_sprites = all_sprites
        self.__soundResources = soundResources
        self.__bullet_img = imgResources.bullet_img
        self.set_player_img(self.__player_org_img, WIDTH / 2, HEIGHT - 10)
        self.__speedx = 0
        self.__lives = 3
        self.__power = 1
        self.__hidden = False
        self.__shield = Player.shield_max_value
        self.__fuel = Player.fuel_max_value
        self.__last_shot = pygame.time.get_ticks()
        self.__hidden_time = pygame.time.get_ticks()
        self.__power_time = pygame.time.get_ticks()

    def set_player_img(self, player_img, x, y):
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = x
        self.rect.bottom = y

    @property
    def shield(self):
        return self.__shield

    @property
    def fuel(self):
        return self.__fuel

    @property
    def lives(self):
        return self.__lives

    @property
    def power(self):
        return self.__power

    @lives.setter
    def lives(self, value):
        self.__lives = value

    @shield.setter
    def shield(self, value):
        self.__shield = value

    @fuel.setter
    def fuel(self, value):
        self.__fuel = value

    def update(self, *args):

        if self.__power >= 2 and pygame.time.get_ticks() - self.__power_time > POWERUP_TIME:
            self.__power -= 1
            self.__power_time = pygame.time.get_ticks()
            if self.__power == 1:
                self.set_player_img(self.__player_org_img, self.rect.centerx, self.rect.bottom)

        # unhide if hidden
        if self.__hidden and pygame.time.get_ticks() - self.__hidden_time > Player.max_hidden_time:
            self.__hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.__speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.__speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.__speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.__speedx
        if self.rect.right > WIDTH - WIDTH_OBSTACLES:
            self.rect.right = WIDTH - WIDTH_OBSTACLES
        if self.rect.left < WIDTH_OBSTACLES:
            self.rect.left = WIDTH_OBSTACLES

        if not self.__hidden:
            self.fuel -= Player.fuel_consumption

    def hide(self):
        self.__hidden = True
        self.__hidden_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH, HEIGHT + 200)

    def power_up(self, power_up_type):
        if power_up_type == ImgResources.POWER_UP_SHIELD:
            self.__shield += random.randrange(10, 30)
            if self.__shield >= 100:
                self.__shield = 100
        if power_up_type == ImgResources.POWER_UP_FUEL:
            self.fuel = Player.fuel_max_value
        if power_up_type == ImgResources.POWER_UP_GUN:
            self.__power += 1
            self.__power_time = pygame.time.get_ticks()
            self.set_player_img(self.__player_power_up_img, self.rect.centerx, self.rect.bottom)

    def shoot(self):
        if self.__hidden:
            return

        now = pygame.time.get_ticks()
        if now - self.__last_shot > Player.shoot_delay:
            self.__last_shot = now
            if self.__power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top, self.__bullet_img)
                self.__all_sprites.add(bullet)
                self.__bullets.add(bullet)
                random.choice(self.__soundResources.shoot_sounds).play()
            if self.__power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery, self.__bullet_img)
                bullet2 = Bullet(self.rect.right, self.rect.centery, self.__bullet_img)
                self.__all_sprites.add(bullet1)
                self.__all_sprites.add(bullet2)
                self.__bullets.add(bullet1)
                self.__bullets.add(bullet2)
                random.choice(self.__soundResources.shoot_sounds).play()

    def was_hit(self, impact):
        """
        Changes player internal state after being hit.
        @returns information if player live was lost
        """
        self.__shield -= impact
        if self.__shield < 0:
            self.__lives -= 1
            if self.__lives > 0:
                self.__shield = 100
            return True
        else:
            return False

    def is_alive(self):
        """ Returns information if player have enough lives to continue game. """
        if self.__lives < 1:
            return False
        else:
            return True

    def recharge_fuel(self):
        self.__fuel = Player.fuel_max_value

    def recover(self):
        self.__shield = Player.shield_max_value
