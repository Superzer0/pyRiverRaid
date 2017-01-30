import logging

import pygame

from objects.globals.gamecolors import GameColors


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img, context, speedy=-10):
        self.__logger = logging.getLogger(Bullet.__module__)
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(GameColors.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.context = context
        self.__speedy = speedy
        self.context.playerCanShot = False

    def update(self, *args):
        self.rect.y += self.__speedy
        if self.rect.bottom < 0:
            self.context.playerCanShot = True
            self.kill()
