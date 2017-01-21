import random
from objects.powerup import PowerUp
from objects.settings import *


class PowerUpGenerator:
    def __init__(self, player, imgResources, all_sprites, powerups):
        self.player = player
        self.imgResources = imgResources
        self.all_sprites = all_sprites
        self.powerups = powerups

    def generate(self):
        pass


class ShieldGenerator(PowerUpGenerator):
    # generate random shield
    def generate(self):
        if self.player.shield < 50 and random.random() > 0.5:
            shield = PowerUp((random.randint(200, WIDTH - 200), 0), self.imgResources.power_ups,
                             self.imgResources.POWER_UP_SHIELD)
            self.powerups.add(shield)
            self.all_sprites.add(shield)


class FuelGenerator(PowerUpGenerator):
    # generate random fuel
    def generate(self):
        count = len(list(filter(lambda x: x.type == self.imgResources.POWER_UP_FUEL, self.powerups)))
        if count < 2 and self.player.fuel < 80 and random.random() > 0.7:
            fuel = PowerUp((random.randint(200, WIDTH - 200), 0), self.imgResources.power_ups,
                           self.imgResources.POWER_UP_FUEL)
            self.powerups.add(fuel)
            self.all_sprites.add(fuel)

            # class GunGenerator(PowerupGenerator):
            #
            #     # generate random gun
            #     def generate(self):
            #         if random.random() > 0.00000001:
            #             gun = Powerup((random.randint(200, WIDTH - 200), 0), 'gun', self.context.resource.power_up_images)
            #             self.context.powerups.add(gun)
            #             self.context.all_sprites.add(gun)
