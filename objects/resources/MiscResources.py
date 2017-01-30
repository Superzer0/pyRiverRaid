import logging
from os import path

import pygame

from objects.resources.ConfigReader import ConfigReader


class MiscResources(ConfigReader):
    __MISC_CONFIG_SECTION_NAME = "MISC"
    __MISC_FOLDER_CONFIG_KEY = "miscFolderName"
    __DEFAULT_FONT_CONFIG_KEY = "defaultFont"

    def __init__(self, game_folder, config):
        self.__logger = logging.getLogger(MiscResources.__module__)

        try:
            ConfigReader.__init__(self, game_folder, config, MiscResources.__MISC_CONFIG_SECTION_NAME)
            self.__misc_dir = path.join(self.resources_folder,
                                        self.get_config_property(MiscResources.__MISC_FOLDER_CONFIG_KEY))
            self.__default_font = path.join(self.__misc_dir,
                                            self.get_config_property(MiscResources.__DEFAULT_FONT_CONFIG_KEY))

            self.__logger.info('loaded miscellaneous resources')
        except Exception:
            self.__logger.error('loading miscellaneous resources failed')
            raise

    def get_font(self, size):
        return pygame.font.Font(self.__default_font, size)
