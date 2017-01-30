import logging

import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, explosion_anim):
        pygame.sprite.Sprite.__init__(self)
        self.__logger = logging.getLogger(Explosion.__module__)
        self.__size = size
        self.__explosion_anim = explosion_anim
        self.image = explosion_anim[self.__size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.__frame = 0
        self.__last_update = pygame.time.get_ticks()
        self.__frame_rate = 50

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.__last_update > self.__frame_rate:
            self.__last_update = now
            self.__frame += 1
            if self.__frame == len(self.__explosion_anim[self.__size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.__explosion_anim[self.__size][self.__frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
