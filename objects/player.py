import logging
import random

import pygame

from objects.bullet import Bullet
from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings
from objects.resources.ImgResources import ImgResources


class Player(pygame.sprite.Sprite):
    SHIELD_MAX_VALUE = 100
    FUEL_MAX_VALUE = 100
    FUEL_CONSUMPTION = 0.2
    SHOOT_DELAY = 25
    MAX_HIDDEN_TIME = 1000

    def __init__(self, imgResources, soundResources, all_sprites, bullets, context):
        pygame.sprite.Sprite.__init__(self)
        self.__logger = logging.getLogger(Player.__module__)
        self.__player_power_up_img = imgResources.power_player_img
        self.__player_org_img = imgResources.player_img
        self.__bullets = bullets
        self.__all_sprites = all_sprites
        self.__soundResources = soundResources
        self.__bullet_img = imgResources.bullet_img
        self.set_player_img(self.__player_org_img, GameSettings.WIDTH / 2, GameSettings.HEIGHT - 10)
        self.__speedx = 0
        self.__lives = 3
        self.__power = 1
        self.__hidden = False
        self.__shield = Player.SHIELD_MAX_VALUE
        self.__fuel = Player.FUEL_MAX_VALUE
        self.__last_shot = pygame.time.get_ticks()
        self.__hidden_time = pygame.time.get_ticks()
        self.__power_time = pygame.time.get_ticks()
        self.context = context

    def set_player_img(self, player_img, x, y):
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(GameColors.BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
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

    def update(self, *args):

        if self.__power >= 2 and pygame.time.get_ticks() - self.__power_time > GameSettings.POWERUP_TIME:
            self.__power -= 1
            self.__power_time = pygame.time.get_ticks()
            if self.__power == 1:
                self.set_player_img(self.__player_org_img, self.rect.centerx, self.rect.bottom)

        # unhide if hidden
        if self.__hidden and pygame.time.get_ticks() - self.__hidden_time > Player.MAX_HIDDEN_TIME:
            self.__hidden = False
            self.rect.centerx = GameSettings.WIDTH / 2
            self.rect.bottom = GameSettings.HEIGHT - 10

        self.__speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.__speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.__speedx = 8
        if keystate[pygame.K_SPACE]:
                self.shoot()
        if keystate[pygame.K_UP]:
            if not self.context.speedGameHasChanged:
                self.rect.centery = GameSettings.HEIGHT - 50
                self.context.gameSpeedUp = True
                self.context.speedGameHasChanged = True

            self.context.speed_up_sprites()
            self.context.gameSpeedUp = True
        else:
            self.context.gameSpeedUp = False

        if self.context.speedGameHasChanged and not self.context.gameSpeedUp:
            self.context.slow_down_sprites()
            self.rect.centery = GameSettings.HEIGHT - 30
            self.context.speedGameHasChanged = False
            self.context.gameSpeedUp = False

        self.rect.x += self.__speedx
        if self.rect.right > GameSettings.WIDTH - GameSettings.WIDTH_OBSTACLES:
            self.rect.right = GameSettings.WIDTH - GameSettings.WIDTH_OBSTACLES
        if self.rect.left < GameSettings.WIDTH_OBSTACLES:
            self.rect.left = GameSettings.WIDTH_OBSTACLES

        if not self.__hidden:
            self.__fuel -= Player.FUEL_CONSUMPTION

    def hide(self):
        self.__hidden = True
        self.__hidden_time = pygame.time.get_ticks()
        self.rect.center = (GameSettings.WIDTH, GameSettings.HEIGHT + 200)

    def power_up(self, power_up_type):
        if power_up_type == ImgResources.POWER_UP_SHIELD:
            self.__shield += random.randrange(10, 30)
            if self.__shield >= 100:
                self.recover_shield()
        if power_up_type == ImgResources.POWER_UP_FUEL:
            self.recharge_fuel()
        if power_up_type == ImgResources.POWER_UP_GUN:
            self.__power += 1
            self.__power_time = pygame.time.get_ticks()
            self.set_player_img(self.__player_power_up_img, self.rect.centerx, self.rect.bottom)

    def shoot(self):
        """Allows player to shoot down the enemy. Issues one bullet and adds it to underlying sprite context."""
        if self.__hidden:
            return

        if self.context.playerCanShot:
            now = pygame.time.get_ticks()
            if now - self.__last_shot > Player.SHOOT_DELAY:
                self.__last_shot = now
                if self.__power == 1:
                    bullet = Bullet(self.rect.centerx, self.rect.top, self.__bullet_img, self.context)
                    self.__all_sprites.add(bullet)
                    self.__bullets.add(bullet)
                    random.choice(self.__soundResources.shoot_sounds).play()
                if self.__power >= 2:
                    bullet1 = Bullet(self.rect.left, self.rect.centery, self.__bullet_img, self.context)
                    bullet2 = Bullet(self.rect.right, self.rect.centery, self.__bullet_img, self.context)
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
                self.recover_shield()
                self.recharge_fuel()
            return True
        else:
            return False

    def is_alive(self):
        """ Returns information if player have enough lives to continue game. """
        return self.__lives > 0

    def recharge_fuel(self):
        """Fills fuel to max value"""
        self.__fuel = Player.FUEL_MAX_VALUE

    def has_fuel(self):
        """Returns true/false if player has gas"""
        return self.__fuel > 0

    def fuel_is_empty(self):
        """Triggers actions for fuel empty. Player loses live"""
        self.__lives -= 1
        if self.__lives > 0:
            self.recover_shield()
            self.recharge_fuel()

    def recover_shield(self):
        """Fills shield to max value"""
        self.__shield = Player.SHIELD_MAX_VALUE
