import logging
import pygame
import random
from objects.bullet import Bullet
from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings


class Direction:
    LEFT = -1
    RIGHT = 1


class StraightEnemy(pygame.sprite.Sprite):
    shoot_delay = 750
    area_length = 150
    move_speed = 5

    def __init__(self, all_sprites, enemies, enemies_shots, imgResources):
        pygame.sprite.Sprite.__init__(self)
        self.__logger = logging.getLogger(StraightEnemy.__module__)
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.enemies_shots = enemies_shots
        self.imgResource = imgResources
        self.image = imgResources.straight_enemy_img
        self.image.set_colorkey(GameColors.BLACK)
        self.__bullet_img = imgResources.bullet_img
        self.rect = self.image.get_rect()
        self.setPosition()
        self.__speedy = 10
        self.radius = 100
        self.__last_shot = pygame.time.get_ticks()
        self.__hidden_time = pygame.time.get_ticks()
        self.__power_time = pygame.time.get_ticks()

    def setPosition(self):
        self.direction_of_flight = self.getDirection()
        if self.direction_of_flight == Direction.RIGHT:
            self.rect.centerx = 50
        else:
            self.rect.centerx = GameSettings.WIDTH - 50

        self.rect.y = random.randrange(50, 350)
        self.rotate()

    def getDirection(self):
        return random.choice([Direction.LEFT, Direction.RIGHT])

    def update(self, *args):
        if 0 < self.rect.centerx and self.rect.centerx < GameSettings.WIDTH:
            self.rect.y += 2
            if self.direction_of_flight == Direction.LEFT:
                self.rect.centerx -= self.__speedy
            else:
                self.rect.centerx += self.__speedy
        else:
            self.kill()

    def rotate(self):
        if self.direction_of_flight == Direction.LEFT:
            self.image = pygame.transform.rotate(self.imgResource.straight_enemy_img, -90)
        else:
            self.image = pygame.transform.rotate(self.imgResource.straight_enemy_img, 90)
