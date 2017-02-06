import logging
import random

import pygame

from objects.base_sprite import BaseShooterSprite
from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings
from objects.mobs.enemy import EnemyMoveDirection


class StraightEnemy(BaseShooterSprite):
    def __init__(self, all_sprites, enemies, enemies_shots, imgResources, speedy=10):
        BaseShooterSprite.__init__(self)
        self.__logger = logging.getLogger(StraightEnemy.__module__)
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.enemies_shots = enemies_shots
        self.imgResource = imgResources
        self.image = imgResources.straight_enemy_img
        self.image.set_colorkey(GameColors.BLACK)
        self.__bullet_img = imgResources.bullet_img
        self.rect = self.image.get_rect()
        self.set_position()
        self.__speedy = speedy
        self.__speedx = 15
        self.__origin_speedy = speedy
        self.radius = 100
        self.__last_shot = pygame.time.get_ticks()
        self.__hidden_time = pygame.time.get_ticks()
        self.__power_time = pygame.time.get_ticks()

    def set_position(self):
        self.direction_of_flight = self.get_direction()
        if self.direction_of_flight == EnemyMoveDirection.RIGHT:
            self.rect.centerx = 50
        else:
            self.rect.centerx = GameSettings.WIDTH - 50

        self.rect.y = random.randrange(50, 350)
        self.__rotate()

    @staticmethod
    def get_direction():
        return random.choice([EnemyMoveDirection.LEFT, EnemyMoveDirection.RIGHT])

    def update(self, *args):
        if 0 < self.rect.centerx < GameSettings.WIDTH:
            self.rect.y += self.__speedy
            if self.direction_of_flight == EnemyMoveDirection.LEFT:
                self.rect.centerx -= self.__speedx
            else:
                self.rect.centerx += self.__speedx
        else:
            self.kill()

    def __rotate(self):
        if self.direction_of_flight == EnemyMoveDirection.LEFT:
            self.image = pygame.transform.rotate(self.imgResource.straight_enemy_img, -90)
        else:
            self.image = pygame.transform.rotate(self.imgResource.straight_enemy_img, 90)

    def speed_up(self):
        """Causes increase in Y speed of the sprite by GameSettings.SPEED_FACTOR"""
        self.__speedy = self.__origin_speedy * GameSettings.SPEED_FACTOR

    def slow_down(self):
        """Causes decrease in Y speed of the sprite."""
        self.__speedy = self.__origin_speedy
