import random

import pygame

from objects.base_sprite import BaseShooterSprite
from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings


class RotatingMeteor(BaseShooterSprite):
    def slow_down(self):
        self.speedy = self.__origin_speedy

    def speed_up(self):
        self.speedy = self.__origin_speedy * GameSettings.SPEED_FACTOR

    def __init__(self, meteor_images, start_x, start_y, speed_x, speed_y, rot_speed):
        BaseShooterSprite.__init__(self)
        self.__image_orig = random.choice(meteor_images)
        self.__image_orig.set_colorkey(GameColors.BLACK)
        self.image = self.__image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)

        self.rect.x = start_x - self.rect.x
        self.rect.y = start_y
        self.speedx = speed_x
        self.speedy = speed_y
        self.__origin_speedy = self.speedy

        self.rot = 0
        self.rot_speed = rot_speed
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.__image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self, *args):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.is_on_the_border():
            self.rect.y = random.randrange(-200, -80)

    def is_on_the_border(self):
        return self.rect.top > GameSettings.HEIGHT + 50 \
               or self.rect.left < -50 or self.rect.right > GameSettings.WIDTH + 100
