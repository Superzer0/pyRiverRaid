import logging

import pygame

from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center, images, type):
        pygame.sprite.Sprite.__init__(self)
        self.__logger = logging.getLogger(PowerUp.__module__)
        self.__type = type
        self.__speedy = 5
        self.image = images[self.__type]
        self.image.set_colorkey(GameColors.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center

    @property
    def type(self):
        return self.__type

    def update(self, *args):
        self.rect.y += self.__speedy

        if self.rect.top > GameSettings.HEIGHT:
            self.kill()
