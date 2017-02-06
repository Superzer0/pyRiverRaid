import random

from objects.globals.gamesettings import GameSettings
from objects.powerup import PowerUp


class PowerUpGenerator:
    """Base class for power ups generators"""
    def __init__(self, player, imgResources, all_sprites, powerups):
        self.player = player
        self.imgResources = imgResources
        self.all_sprites = all_sprites
        self.power_ups = powerups

    def generate(self):
        """base dummy implementation for genrating power up"""
        pass


class ShieldGenerator(PowerUpGenerator):
    """Generates random shield"""

    def generate(self):
        """Method used for generating shield, if created shield added to sprite context"""
        if self.player.shield < 50 and random.random() > GameSettings.SHIELD_PROP:
            shield = PowerUp((random.randint(200, GameSettings.WIDTH - 200), 0), self.imgResources.power_ups,
                             self.imgResources.POWER_UP_SHIELD)
            self.power_ups.add(shield)
            self.all_sprites.add(shield)


class GunGenerator(PowerUpGenerator):
    """Generates random gun"""
    def generate(self):
        """Method used for generating gun, if created gun added to sprite context"""
        if random.random() > GameSettings.GUN_PROP:
            gun = PowerUp((random.randint(200, GameSettings.WIDTH - 200), 0), self.imgResources.power_ups,
                          self.imgResources.POWER_UP_GUN)
            self.power_ups.add(gun)
            self.all_sprites.add(gun)


class FuelGenerator(PowerUpGenerator):
    """Generates random fuel pack"""
    def generate(self):
        """Method used for generating fuel, if created fuel added to sprite context"""
        count = len(list(filter(lambda x: x.type == self.imgResources.POWER_UP_FUEL, self.power_ups)))
        if count < 2 and self.player.fuel < 80 and random.random() > GameSettings.FUEL_PROP:
            fuel = PowerUp((random.randint(200, GameSettings.WIDTH - 200), 0), self.imgResources.power_ups,
                           self.imgResources.POWER_UP_FUEL)
            self.power_ups.add(fuel)
            self.all_sprites.add(fuel)
