import logging

from objects.base_sprite import BaseShooterSprite
from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings


class PowerUp(BaseShooterSprite):
    def __init__(self, center, images, power_up_type, speedy=5):
        BaseShooterSprite.__init__(self)
        self.__logger = logging.getLogger(PowerUp.__module__)
        self.__type = power_up_type
        self.__speedy = speedy
        self.__origin_speedy = speedy
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

    def speed_up(self):
        """Causes increase in Y speed of the sprite by GameSettings.SPEED_FACTOR"""
        self.__speedy = self.__origin_speedy * GameSettings.SPEED_FACTOR

    def slow_down(self):
        """Causes decrease in Y speed of the sprite."""
        self.__speedy = self.__origin_speedy
