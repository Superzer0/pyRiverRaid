import random
from objects.base_sprite import BaseShooterSprite
from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings


class Bridge(BaseShooterSprite):
    SHIELD_MAX_VALUE = 100

    def __init__(self, context, imgResources):
        BaseShooterSprite.__init__(self)
        self.context = context
        self.shield = Bridge.SHIELD_MAX_VALUE
        self.imgResorces = imgResources
        self.image = imgResources.bridge_img
        self.image.set_colorkey(GameColors.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = 100
        self.rect.centerx = GameSettings.WIDTH / 2

    def update(self, *args):
        if self.shield < 0:
            self.kill();

    def is_alive(self):
        return self.shield >= 0

    def take_hit(self):
        self.shield -= 5
