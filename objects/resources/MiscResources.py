from os import path
import pygame


class MiscResources:
    __MISC_FOLDER_PREFIX = "misc"

    def __init__(self, game_folder):
        self.__game_folder = game_folder
        self.__misc_dir = path.join(game_folder, MiscResources.__MISC_FOLDER_PREFIX)
        self.__default_font = path.join(self.__misc_dir, 'kenvector_future_thin.ttf')

    def get_font(self, size):
        return pygame.font.Font(self.__default_font, size)
