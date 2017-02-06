import logging
import random

import pygame

from objects.base_sprite import BaseShooterSprite
from objects.bullet import Bullet
from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings


class EnemyMoveDirection:
    """Defines direction for move"""
    LEFT = -1
    RIGHT = 1


class Enemy(BaseShooterSprite):
    """Base sprite for enemy"""
    SHOOT_DELAY = 750
    AREA_LENGTH = 150
    MOVE_SPEED = 5

    def __init__(self, all_sprites, enemies, enemies_shots, imgResources, speedy=2):
        """Inits Enemy sprite with all required img resources and sprite context"""
        BaseShooterSprite.__init__(self)
        self.__logger = logging.getLogger(Enemy.__module__)
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.enemies_shots = enemies_shots
        self.imgResource = imgResources
        self.image = imgResources.enemy_img
        self.image.set_colorkey(GameColors.BLACK)
        self.__bullet_img = imgResources.bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randrange(0, 10)
        self.origin_x = random.randrange(150, GameSettings.WIDTH - 150)
        self.rect.centerx = self.origin_x
        self.direction_of_flight = self.get_direction()
        self.__rotate()
        self.__speedy = speedy
        self.__origin_speedy = speedy
        self.__twisting_speedy = Enemy.MOVE_SPEED
        self.radius = 100
        self.__last_shot = pygame.time.get_ticks()
        self.__hidden_time = pygame.time.get_ticks()
        self.__power_time = pygame.time.get_ticks()

    def get_direction(self):
        """
        Returns current move direction
        :return: Direction
        """
        if 150 < self.origin_x < GameSettings.WIDTH / 2:
            return EnemyMoveDirection.LEFT
        if GameSettings.WIDTH / 2 < self.origin_x < GameSettings.WIDTH - 150:
            return EnemyMoveDirection.RIGHT

    def shot(self):
        """Triggers enemy shot. Adds new bullet sprite in sprite context

        :return: None
        """
        now = pygame.time.get_ticks()
        if now - self.__last_shot > Enemy.SHOOT_DELAY:
            self.__last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.bottom, self.__bullet_img, 15)
            self.all_sprites.add(bullet)
            self.enemies_shots.add(bullet)

    def update(self, *args):
        """Updates state for the enemy on frame basis"""
        self.rect.y += self.__speedy
        distance = abs(self.origin_x - self.rect.centerx)
        if distance > Enemy.AREA_LENGTH:
            # switch direction of flight and rotate enemy's image
            self.__rotate()

        # move enemy to left or right
        if self.direction_of_flight == EnemyMoveDirection.RIGHT:
            self.rect.centerx += self.__twisting_speedy
        else:
            self.rect.centerx -= self.__twisting_speedy

    def __rotate(self):
        if self.direction_of_flight == EnemyMoveDirection.LEFT:
            self.direction_of_flight = EnemyMoveDirection.RIGHT
            self.image = pygame.transform.rotate(self.imgResource.enemy_img, 90)

        else:
            self.direction_of_flight = EnemyMoveDirection.LEFT
            self.image = pygame.transform.rotate(self.imgResource.enemy_img, -90)

    def speed_up(self):
        """Causes increase in Y speed of the sprite by GameSettings.SPEED_FACTOR"""
        self.__speedy = self.__origin_speedy * GameSettings.SPEED_FACTOR

    def slow_down(self):
        self.__speedy = self.__origin_speedy
