import logging

from objects.base_sprite import BaseShooterSprite
from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings


class Bullet(BaseShooterSprite):
    def __init__(self, x, y, bullet_img, context, speedy=-30):
        self.__logger = logging.getLogger(Bullet.__module__)
        BaseShooterSprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(GameColors.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.context = context
        self.__speedy = speedy
        self.__origin_speedy = speedy
        self.context.playerCanShot = False

    def update(self, *args):
        self.rect.y += self.__speedy
        if self.rect.bottom < 0:
            self.context.playerCanShot = True
            self.kill()

    def speed_up(self):
        self.__speedy = self.__origin_speedy * GameSettings.SPEED_FACTOR

    def slow_down(self):
        self.__speedy = self.__origin_speedy
