from os import path
import pygame

from objects.settings import BLACK


class ImgResources:
    EXPLOSION_ANIMATIONS_LG = 'lg'
    EXPLOSION_ANIMATIONS_SM = 'sm'
    EXPLOSION_ANIMATIONS_PLAYER = 'player'

    POWER_UP_SHIELD = 'shield'
    POWER_UP_GUN = 'gun'
    __IMG_FOLDER_PREFIX = "img"

    def __init__(self, game_folder):
        self.__game_folder = game_folder
        self.__img_dir = path.join(game_folder, ImgResources.__IMG_FOLDER_PREFIX)
        self.__bullet_img = pygame.image.load(path.join(self.__img_dir, "laserRed16.png")).convert()
        self.__enemy_img = pygame.transform.rotate(pygame.image.load(path.join(self.__img_dir, "playerShip1_orange.png")).convert(), 180)
        self.__power_player_img = pygame.image.load(path.join(self.__img_dir, "playerShip3_blue.png")).convert()
        self.__player_img = pygame.image.load(path.join(self.__img_dir, "playerShip2_blue.png")).convert()
        self.__player_mini_img = pygame.transform.scale(self.__player_img, (25, 19))
        self.__player_mini_img.set_colorkey(BLACK)
        self.__background = pygame.image.load(path.join(self.__img_dir, 'starfield.png')).convert()
        self.__meteors_obstacles = self.__load_meteors_img('meteors', 'grey')
        self.__meteors_mobs = self.__load_meteors_img('meteors', 'brown')
        self.__explosion_animations = self.__load_explosions_animations('Explosions_kenney')
        self.__power_ups = self.__load_power_ups('powerups', 'shield_gold.png', 'bolt_gold.png')

    @property
    def background(self):
        return self.__background

    @property
    def player_img(self):
        return self.__player_img

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

    def __load_power_ups(self, folder, shield_file_name, bolt_file_name):
        return {ImgResources.POWER_UP_SHIELD: pygame.image.load(
            path.join(self.__img_dir, folder, shield_file_name)).convert(),
                ImgResources.POWER_UP_GUN: pygame.image.load(path.join(self.__img_dir, folder, bolt_file_name)).convert()}

    @staticmethod
    def __load_explosions_img(image_directory, subfolder, img_filename):
        explosion_image = pygame.image.load(path.join(image_directory, subfolder, img_filename)).convert()
        explosion_image.set_colorkey(BLACK)
        return explosion_image

    def __load_meteors_img(self, folder, subfolder):
        meteors_file_names_list = ['meteor_big1.png', 'meteor_big2.png', 'meteor_big3.png', 'meteor_big4.png',
                                   'meteor_med1.png',
                                   'meteor_med2.png', 'meteor_small1.png', 'meteor_small2.png',
                                   'meteor_tiny1.png', 'meteor_tiny2.png']
        return [pygame.image.load(path.join(self.__img_dir, folder, subfolder, img)).convert()
                for img in
                meteors_file_names_list]

    def __load_explosions_animations(self, animationsFolder):
        explosion_animations = {ImgResources.EXPLOSION_ANIMATIONS_LG: [], ImgResources.EXPLOSION_ANIMATIONS_SM: [],
                                ImgResources.EXPLOSION_ANIMATIONS_PLAYER: []}

        # regular explosion
        regular_explosions_animations_file_names = ['regularExplosion0{}.png'.format(i) for i in range(9)]
        for file_name in regular_explosions_animations_file_names:
            img = self.__load_explosions_img(self.__img_dir, animationsFolder, file_name)
            img_lg = pygame.transform.scale(img, (75, 75))
            explosion_animations[ImgResources.EXPLOSION_ANIMATIONS_LG].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            explosion_animations[ImgResources.EXPLOSION_ANIMATIONS_SM].append(img_sm)

        # player explosion
        sonic_explosions_animations_file_names = ['sonicExplosion0{}.png'.format(i) for i in range(9)]
        for file_name in sonic_explosions_animations_file_names:
            img = self.__load_explosions_img(self.__img_dir, animationsFolder, file_name)
            explosion_animations[ImgResources.EXPLOSION_ANIMATIONS_PLAYER].append(img)

        return explosion_animations
