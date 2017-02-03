import logging

import pygame

from objects.globals.gamecolors import GameColors


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, resourcesContext, text, id, has_focus=False):
        pygame.sprite.Sprite.__init__(self)
        self.__id = id
        self.__resourceContext = resourcesContext
        self.__text = text
        self.__logger = logging.getLogger(Button.__module__)

        self.__x = x
        self.__y = y
        self.has_focus = has_focus
        self.button_pressed_img = self.__resourceContext.imgResources.button_pressed_img
        self.button_img = self.__resourceContext.imgResources.button_img
        self.set_button_image(x, y)

    @property
    def id(self):
        return self.__id

    def set_button_image(self, x, y):
        self.image = self.__get_button_image()
        self.image.set_colorkey(GameColors.BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.draw_text(self.image, self.__text, 20, (self.rect.width // 2, self.rect.height * 0.25), GameColors.BLACK)

    def focus(self, value=True):
        self.has_focus = value

    def update(self, *args):
        self.set_button_image(self.__x, self.__y)

    def __get_button_image(self):
        return (self.button_pressed_img if self.has_focus else self.button_img).copy()

    def draw_text(self, surf, text, size, position, color=GameColors.WHITE):
        font = self.__resourceContext.miscResources.get_font(size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = position
        surf.blit(text_surface, text_rect)
