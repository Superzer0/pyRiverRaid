import pygame

from objects.settings import BLACK


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img, context):
        pygame.sprite.Sprite.__init__(self)
        self.context = context
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self, *args):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.context.playerCanShot = True
            self.kill()
