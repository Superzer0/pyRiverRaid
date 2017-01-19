import random

import pygame

from objects.settings import BLACK, HEIGHT


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center, images, type):
        pygame.sprite.Sprite.__init__(self)
        self.__type = type
        self.__speedy = 5
        self.image = images[self.__type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center

    @property
    def type(self):
        return self.__type

    def update(self, *args):
        self.rect.y += self.__speedy

        if self.rect.top > HEIGHT:
            self.kill()
