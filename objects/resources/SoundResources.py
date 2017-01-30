import logging
from os import path

import pygame

from objects.resources.ConfigReader import ConfigReader


class SoundResources(ConfigReader):
    __SOUND_SECTION_CONFIG_NAME = 'SOUNDS'
    __SOUND_FOLDER_CONFIG_NAME = 'soundFolderName'
    __DEFAULT_MUSIC_CONFIG_KEY = 'defaultMusic'
    __SHOOTS_SOUNDS_CONFIG_KEY = 'shootSounds'
    __EXPLOSION_SOUNDS_CONFIG_KEY = 'expolosionSounds'
    __PLAYER_DIE_SOUND_CONFIG_KEY = 'playerDieSound'

    def __init__(self, game_folder, config):
        self.__logger = logging.getLogger(SoundResources.__module__)
        try:
            ConfigReader.__init__(self, game_folder, config, SoundResources.__SOUND_SECTION_CONFIG_NAME)
            self.__snd_dir = path.join(self.resources_folder,
                                       self.get_config_property(SoundResources.__SOUND_FOLDER_CONFIG_NAME))
            self.__shoot_sounds = self.get_sound_resources(SoundResources.__SHOOTS_SOUNDS_CONFIG_KEY)
            self.__explosion_sounds = self.get_sound_resources(SoundResources.__EXPLOSION_SOUNDS_CONFIG_KEY)
            self.__player_die_sound = self.get_sound_resources(SoundResources.__PLAYER_DIE_SOUND_CONFIG_KEY)[0]
            self.__default_music_path = path.join(self.__snd_dir,
                                                  self.get_config_property(SoundResources.__DEFAULT_MUSIC_CONFIG_KEY))
            self.__logger.info('loaded sound resources')
        except Exception:
            self.__logger.info('loading sound resources failed.')
            raise

    def get_sound_resources(self, prop):
        return [pygame.mixer.Sound(path.join(self.__snd_dir, snd)) for snd in self.get_config_property_value_list(prop)]

    @property
    def shoot_sounds(self):
        return self.__shoot_sounds

    @property
    def explosion_sounds(self):
        return self.__explosion_sounds

    @property
    def player_die_sound(self):
        return self.__player_die_sound

    def load_default_music(self):
        pygame.mixer.music.load(self.__default_music_path)
        self.__logger.info('loaded game music')

    @staticmethod
    def play_default_music():
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)
