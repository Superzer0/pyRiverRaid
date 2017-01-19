from os import path
import pygame


class SoundResources:
    __SOUND_FOLDER_PREFIX = "snd"

    def __init__(self, game_folder):
        self.__game_folder = game_folder
        self.__snd_dir = path.join(self.__game_folder, SoundResources.__SOUND_FOLDER_PREFIX)
        self.__shoot_sounds = [pygame.mixer.Sound(path.join(self.__snd_dir, snd)) for snd in
                               ['sfx_laser1.ogg', 'sfx_laser2.ogg']]
        self.__explosion_sounds = [pygame.mixer.Sound(path.join(self.__snd_dir, snd)) for snd in
                                   ['expl3.wav', 'expl6.wav']]
        self.__player_die_sound = pygame.mixer.Sound(path.join(self.__snd_dir, 'rumble1.ogg'))

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
        pygame.mixer.music.load(path.join(self.__snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))

    @staticmethod
    def play_default_music():
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)
