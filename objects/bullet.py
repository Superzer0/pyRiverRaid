import pygame

from objects.settings import BLACK


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img, speedy=-10):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.__speedy = speedy

    def update(self, *args):
        self.rect.y += self.__speedy
        if self.rect.bottom < 0:
            self.kill()
