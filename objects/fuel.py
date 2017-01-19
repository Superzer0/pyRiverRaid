import pygame


class Fuel(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        # self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -5

    def update(self, *args):
        pass
