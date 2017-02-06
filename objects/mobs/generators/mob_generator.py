from objects.globals.gamesettings import GameSettings
from objects.mobs.randommeteor import RandomMeteor


class MobGenerator:
    """Generates obstacles for user."""

    def __init__(self, spriteContext, imgResources, all_sprites):
        """Inits new instance of generator with required img resources and sprites context"""
        self.imgResources = imgResources
        self.spriteContext = spriteContext
        self.all_sprites = all_sprites

    def generate(self):
        """Generates new obstacle (mob) initialized with random values."""
        for i in range(GameSettings.MAX_METEORS - len(self.spriteContext.mobs)):
            self.__new_mob()

    def __new_mob(self):
        m = RandomMeteor(self.imgResources.meteor_mobs_img)
        self.all_sprites.add(m)
        self.spriteContext.mobs.add(m)
