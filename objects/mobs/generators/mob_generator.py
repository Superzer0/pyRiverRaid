import random

from objects.globals.gamesettings import GameSettings
from objects.mobs.randommeteor import RandomMeteor


class MobGenerator:
    def __init__(self, spriteContext, imgResources, all_sprites):
        self.imgResources = imgResources
        self.spriteContext = spriteContext
        self.all_sprites = all_sprites

    def generate(self):
        for i in range(GameSettings.MAX_METEORS - len(self.spriteContext.mobs)):
            self.__new_mob()

    def __new_mob(self):
        m = RandomMeteor(self.imgResources.meteor_mobs_img)
        self.all_sprites.add(m)
        self.spriteContext.mobs.add(m)
