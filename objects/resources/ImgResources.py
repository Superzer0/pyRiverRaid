import logging
from os import path

import pygame

from objects.globals.gamecolors import GameColors
from objects.resources.ConfigReader import ResourcesReader


class ImgResources(ResourcesReader):
    EXPLOSION_ANIMATIONS_LG = 'lg'
    EXPLOSION_ANIMATIONS_SM = 'sm'
    EXPLOSION_ANIMATIONS_PLAYER = 'player'

    POWER_UP_SHIELD = 'shield'
    POWER_UP_FUEL = 'fuel'
    POWER_UP_GUN = 'gun'

    __IMG_CONFIG_SECTION_NAME = "IMAGES"
    __IMG_FOLDER_CONFIG_KEY = "imgFolderName"

    __IMG_BULLET_CONFIG_KEY = "bulletImg"
    __IMG_ENEMY_CONFIG_KEY = "enemyImg"
    __IMG_PLAYER_CONFIG_KEY = "playerImg"
    __IMG_POWER_PLAYER_CONFIG_KEY = "powerPlayerImg"
    __IMG_BACKGROUND_CONFIG_KEY = "background"

    __IMG_METEORS_FOLDER_CONFIG_KEY = "meteorsFolder"
    __IMG_METEORS_OBSTACLES_CONFIG_KEY = "meteorsObstacles"
    __IMG_METEORS_MOBS_CONFIG_KEY = "meteorMobs"
    __IMG_METEORS_FILE_NAMES_CONFIG_KEY = "meteorsFilesNames"
    __IMG_EXPLOSIONS_FOLDER_CONFIG_KEY = "explosionsFolderName"
    __IMG_EXPLOSIONS_REGULAR_CONFIG_KEY = "regularExplosionFileNames"
    __IMG_EXPLOSIONS_SONIC_CONFIG_KEY = "sonicExplosionFileNames"
    __IMG_SHIELD_CONFIG_KEY = "shieldPowerUp"
    __IMG_FUEL_CONFIG_KEY = "fuelPowerUp"
    __IMG_BOLT_CONFIG_KEY = "boltPowerUp"
    __IMG_BUTTON_KEY = "buttonImg"
    __IMG_BUTTON_PRESSED_KEY = "buttonPressedImg"
    __IMG_PLAYER_LIFE_IMG = "playerLifeImg"

    def __init__(self, game_folder, config):
        self.__logger = logging.getLogger(ImgResources.__module__)
        try:
            ResourcesReader.__init__(self, game_folder, config, ImgResources.__IMG_CONFIG_SECTION_NAME)
            self.__img_dir = path.join(self.resources_folder,
                                       self.get_config_property(ImgResources.__IMG_FOLDER_CONFIG_KEY))
            self.__bullet_img = self.load_image(ImgResources.__IMG_BULLET_CONFIG_KEY)
            self.__enemy_img = pygame.transform.rotate(self.load_image(ImgResources.__IMG_ENEMY_CONFIG_KEY), 180)
            self.__player_img = self.load_image(ImgResources.__IMG_PLAYER_CONFIG_KEY)
            self.__button_img = self.load_image(ImgResources.__IMG_BUTTON_KEY)
            self.__button_pressed_img = self.load_image(ImgResources.__IMG_BUTTON_PRESSED_KEY)
            self.__power_player_img = self.load_image(ImgResources.__IMG_POWER_PLAYER_CONFIG_KEY)
            self.__player_mini_img = self.load_image(ImgResources.__IMG_PLAYER_LIFE_IMG)
            self.__player_mini_img.set_colorkey(GameColors.BLACK)
            self.__background = self.load_image(ImgResources.__IMG_BACKGROUND_CONFIG_KEY)
            self.__meteors_obstacles = self.__load_meteors_img(
                self.get_config_property(ImgResources.__IMG_METEORS_OBSTACLES_CONFIG_KEY))
            self.__meteors_mobs = self.__load_meteors_img(
                self.get_config_property(ImgResources.__IMG_METEORS_MOBS_CONFIG_KEY))
            self.__explosion_animations = self.__load_explosions_animations()
            self.__power_ups = self.__load_power_ups()
            self.__logger.info('loaded image resources')
        except Exception:
            self.__logger.error('loading image resources failed')
            raise

    @property
    def background(self):
        return self.__background

    @property
    def player_img(self):
        return self.__player_img

    @property
    def button_img(self):
        return self.__button_img

    @property
    def button_pressed_img(self):
        return self.__button_pressed_img

    @property
    def player_mini_img(self):
        return self.__player_mini_img

    @property
    def power_player_img(self):
        return self.__power_player_img

    @property
    def enemy_img(self):
        return self.__enemy_img

    @property
    def bullet_img(self):
        return self.__bullet_img

    @property
    def meteor_obstacles_img(self):
        return self.__meteors_obstacles

    @property
    def meteor_mobs_img(self):
        return self.__meteors_mobs

    @property
    def explosion_animations(self):
        return self.__explosion_animations

    @property
    def power_ups(self):
        return self.__power_ups

    def load_image(self, property_name):
        return pygame.image.load(path.join(self.__img_dir, self.get_config_property(property_name))).convert()

    def __load_power_ups(self):
        return {
            ImgResources.POWER_UP_SHIELD: self.load_image(ImgResources.__IMG_SHIELD_CONFIG_KEY),
            ImgResources.POWER_UP_FUEL: self.load_image(ImgResources.__IMG_FUEL_CONFIG_KEY),
            ImgResources.POWER_UP_GUN: self.load_image(ImgResources.__IMG_BOLT_CONFIG_KEY)}

    @staticmethod
    def __load_explosions_img(image_directory, subfolder, img_filename):
        explosion_image = pygame.image.load(path.join(image_directory, subfolder, img_filename)).convert()
        explosion_image.set_colorkey(GameColors.BLACK)
        return explosion_image

    def __load_meteors_img(self, subfolder):
        meteors_file_names_list = self.get_config_property_value_list(ImgResources.__IMG_METEORS_FILE_NAMES_CONFIG_KEY)
        meteors_folder = self.get_config_property(ImgResources.__IMG_METEORS_FOLDER_CONFIG_KEY)

        return [pygame.image.load(path.join(self.__img_dir, meteors_folder, subfolder, img)).convert()
                for img in
                meteors_file_names_list]

    def __load_explosions_animations(self):

        animations_folder = self.get_config_property(ImgResources.__IMG_EXPLOSIONS_FOLDER_CONFIG_KEY)

        explosion_animations = {ImgResources.EXPLOSION_ANIMATIONS_LG: [], ImgResources.EXPLOSION_ANIMATIONS_SM: [],
                                ImgResources.EXPLOSION_ANIMATIONS_PLAYER: []}

        # regular explosion
        regular_explosions_animations_file_names = self.get_config_property_value_list(
            ImgResources.__IMG_EXPLOSIONS_REGULAR_CONFIG_KEY)

        for file_name in regular_explosions_animations_file_names:
            img = self.__load_explosions_img(self.__img_dir, animations_folder, file_name)
            img_lg = pygame.transform.scale(img, (75, 75))
            explosion_animations[ImgResources.EXPLOSION_ANIMATIONS_LG].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            explosion_animations[ImgResources.EXPLOSION_ANIMATIONS_SM].append(img_sm)

        # player explosion
        sonic_explosions_animations_file_names = self.get_config_property_value_list(
            ImgResources.__IMG_EXPLOSIONS_SONIC_CONFIG_KEY)

        for file_name in sonic_explosions_animations_file_names:
            img = self.__load_explosions_img(self.__img_dir, animations_folder, file_name)
            explosion_animations[ImgResources.EXPLOSION_ANIMATIONS_PLAYER].append(img)

        return explosion_animations
