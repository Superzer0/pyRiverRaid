import random

from objects.mobs.rotatingmeteor import RotatingMeteor
from objects.settings import *


class RandomMeteor(RotatingMeteor):
    def __init__(self, meteor_images):
        RotatingMeteor.__init__(self, meteor_images, random.randrange(WIDTH - WIDTH_OBSTACLES),
                                random.randrange(-150, -100), random.randrange(-2, 2),
                                random.randrange(1, 8), random.randrange(-8, 8))

    def update(self, *args):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def is_on_the_border(self):
        return self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20