import abc

import pygame


class BaseShooterSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._speedy = None
        self._origin_speedy = None

    @abc.abstractmethod
    def speed_up(self):
        """Base method implemented in derived classes"""
        pass

    @abc.abstractmethod
    def slow_down(self):
        """Base method implemented in derived classes"""
        pass
