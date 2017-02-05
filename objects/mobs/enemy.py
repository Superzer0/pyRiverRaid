import logging
import random

import pygame

from objects.base_sprite import BaseShooterSprite
from objects.bullet import Bullet
from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings


class Direction:
    LEFT = -1
    RIGHT = 1


class Enemy(BaseShooterSprite):
    SHOOT_DELAY = 750
    AREA_LENGTH = 150
    MOVE_SPEED = 5

    def __init__(self, all_sprites, enemies, enemies_shots, imgResources, speedy=2):
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
        self.origin_x = random.randrange(150, GameSettings.WIDTH - 150);
        self.rect.centerx = self.origin_x
        self.direction_of_flight = self.get_direction()
        self.rotate()
        self.__speedy = speedy
        self.__origin_speedy = speedy
        self.__twisting_speedy = Enemy.MOVE_SPEED
        self.radius = 100
        self.__last_shot = pygame.time.get_ticks()
        self.__hidden_time = pygame.time.get_ticks()
        self.__power_time = pygame.time.get_ticks()

    def get_direction(self):
        if 150 < self.origin_x < GameSettings.WIDTH / 2:
            return Direction.LEFT
        if GameSettings.WIDTH / 2 < self.origin_x < GameSettings.WIDTH - 150:
            return Direction.RIGHT

    def shot(self):
        now = pygame.time.get_ticks()
        if now - self.__last_shot > Enemy.SHOOT_DELAY:
            self.__last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.bottom, self.__bullet_img, 15)
            self.all_sprites.add(bullet)
            self.enemies_shots.add(bullet)

    def update(self, *args):
        self.rect.y += self.__speedy
        # self.shot()

        distance = abs(self.origin_x - self.rect.centerx)
        if distance > Enemy.AREA_LENGTH:
            # switch direction of flight and rotate enemy's image
            self.rotate()

        # move enemy to left or right
        if self.direction_of_flight == Direction.RIGHT:
            self.rect.centerx += self.__twisting_speedy
        else:
            self.rect.centerx -= self.__twisting_speedy

    def rotate(self):
        if self.direction_of_flight == Direction.LEFT:
            self.direction_of_flight = Direction.RIGHT
            self.image = pygame.transform.rotate(self.imgResource.enemy_img, 90)

        else:
            self.direction_of_flight = Direction.LEFT
            self.image = pygame.transform.rotate(self.imgResource.enemy_img, -90)

    def speed_up(self):
        self.__speedy = self.__origin_speedy * GameSettings.SPEED_FACTOR

    def slow_down(self):
        self.__speedy = self.__origin_speedy
