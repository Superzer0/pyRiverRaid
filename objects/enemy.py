import logging
import random

import pygame

from objects.bullet import Bullet
from objects.settings import BLACK
from objects.settings import WIDTH


class Direction:
    LEFT = -1
    RIGHT = 1


class Enemy(pygame.sprite.Sprite):
    shoot_delay = 750
    area_length = 150
    move_speed = 5

    def __init__(self, all_sprites, enemies, enemies_shots, imgResources):
        pygame.sprite.Sprite.__init__(self)
        self.__logger = logging.getLogger(Enemy.__module__)
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.enemies_shots = enemies_shots
        self.imgResource = imgResources
        self.image = imgResources.enemy_img
        self.image.set_colorkey(BLACK)
        self.__bullet_img = imgResources.bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randrange(0, 10)
        self.origin_x = random.randrange(150, WIDTH - 150);
        self.rect.centerx = self.origin_x
        self.direction_of_flight = self.getDirection()
        self.rotate()
        self.__speedy = 2
        self.radius = 100
        self.__last_shot = pygame.time.get_ticks()
        self.__hidden_time = pygame.time.get_ticks()
        self.__power_time = pygame.time.get_ticks()

    def getDirection(self):
        if 150 < self.origin_x < WIDTH / 2:
            return Direction.LEFT
        if WIDTH / 2 < self.origin_x < WIDTH - 150:
            return Direction.RIGHT

    def shot(self):
        now = pygame.time.get_ticks()
        if now - self.__last_shot > Enemy.shoot_delay:
            self.__last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.bottom, self.__bullet_img, 15)
            self.all_sprites.add(bullet)
            self.enemies_shots.add(bullet)

    def update(self, *args):
        self.rect.y += self.__speedy
        # self.shot()

        distance = abs(self.origin_x - self.rect.centerx)
        if distance > Enemy.area_length:
            # switch direction of flight and rotate enemy's image
            self.rotate()

        # move enemy to left or right
        if self.direction_of_flight == Direction.RIGHT:
            self.rect.centerx += Enemy.move_speed
        else:
            self.rect.centerx -= Enemy.move_speed

    def rotate(self):
        if self.direction_of_flight == Direction.LEFT:
            self.direction_of_flight = Direction.RIGHT
            self.image = pygame.transform.rotate(self.imgResource.enemy_img, 90)

        else:
            self.direction_of_flight = Direction.LEFT
            self.image = pygame.transform.rotate(self.imgResource.enemy_img, -90)
