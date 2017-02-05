import random

from objects.globals.gamesettings import GameSettings
from objects.powerup import PowerUp


class PowerUpGenerator:
    def __init__(self, player, imgResources, all_sprites, powerups):
        self.player = player
        self.imgResources = imgResources
        self.all_sprites = all_sprites
        self.power_ups = powerups

    def generate(self):
        pass


class ShieldGenerator(PowerUpGenerator):
    # generate random shield
    def generate(self):
        if self.player.shield < 50 and random.random() > GameSettings.SHIELD_PROP:
            shield = PowerUp((random.randint(200, GameSettings.WIDTH - 200), 0), self.imgResources.power_ups,
                             self.imgResources.POWER_UP_SHIELD)
            self.power_ups.add(shield)
            self.all_sprites.add(shield)


class GunGenerator(PowerUpGenerator):
    def generate(self):
        if random.random() > GameSettings.GUN_PROP:
            gun = PowerUp((random.randint(200, GameSettings.WIDTH - 200), 0), self.imgResources.power_ups,
                          self.imgResources.POWER_UP_GUN)
            self.power_ups.add(gun)
            self.all_sprites.add(gun)


class FuelGenerator(PowerUpGenerator):
    # generate random fuel
    def generate(self):
        count = len(list(filter(lambda x: x.type == self.imgResources.POWER_UP_FUEL, self.power_ups)))
        if count < 2 and self.player.fuel < 80 and random.random() > GameSettings.FUEL_PROP:
            fuel = PowerUp((random.randint(200, GameSettings.WIDTH - 200), 0), self.imgResources.power_ups,
                           self.imgResources.POWER_UP_FUEL)
            self.power_ups.add(fuel)
            self.all_sprites.add(fuel)
