import random

from objects.globals.gamesettings import GameSettings
from objects.mobs.rotatingmeteor import RotatingMeteor


class RandomMeteor(RotatingMeteor):
    """Randomly showing obstacle/meteor for the user"""
    def __init__(self, meteor_images):
        RotatingMeteor.__init__(self, meteor_images,
                                random.randrange(GameSettings.WIDTH - GameSettings.WIDTH_OBSTACLES),
                                random.randrange(-150, -100), random.randrange(-2, 2),
                                random.randrange(1, 8), random.randrange(-8, 8))

    def update(self, *args):
        """Updates state for the meteor on frame basis"""
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > GameSettings.HEIGHT + 10 or self.rect.left < -25 \
                or self.rect.right > GameSettings.WIDTH + 20:
            self.rect.x = random.randrange(GameSettings.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def is_on_the_border(self):
        """Returns information if obstacle/meteor is on the edge of the user screen

        :return: True/False
        """
        return self.rect.top > GameSettings.HEIGHT + 10 or self.rect.left < -25 or self.rect.right \
                                                                                   > GameSettings.WIDTH + 20
