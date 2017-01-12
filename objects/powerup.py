import random

import pygame

from objects.settings import BLACK, HEIGHT


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center, images):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self, *args):
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            self.kill()
