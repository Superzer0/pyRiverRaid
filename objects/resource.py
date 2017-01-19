import os
import random
from objects.enemy import Enemy
from objects.explosion import Explosion
from objects.mobs.randommeteor import RandomMeteor
from objects.mobs.rotatingmeteor import RotatingMeteor
from objects.player import *
from objects.powerup import Powerup
from objects.settings import *
from os import path


class Resource:
    def __init__(self):
        # set up asset folders
        self.game_folder = path.join(os.path.dirname(__file__), '..', 'resources')
        self.img_dir = path.join(self.game_folder, 'img')
        self.snd_dir = path.join(self.game_folder, 'snd')
        self.misc_dir = path.join(self.game_folder, 'misc')
        self.shoot_sound = pygame.mixer.Sound(
            path.join(self.snd_dir, random.choice(['sfx_laser1.ogg', 'sfx_laser2.ogg'])))
        self.explosion_sounds = [pygame.mixer.Sound(path.join(self.snd_dir, snd)) for snd in ['expl3.wav', 'expl6.wav']]
        self.player_die_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'rumble1.ogg'))
        pygame.mixer.music.load(path.join(self.snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.set_volume(0.4)

        self.background = pygame.image.load(path.join(self.img_dir, 'starfield.png')).convert()
        self.background_rect = self.background.get_rect()
        self.player_img = pygame.image.load(path.join(self.img_dir, "playerShip2_blue.png")).convert()
        self.enemy_img = pygame.image.load(path.join(self.img_dir, "playerShip1_orange.png")).convert()
        self.enemy_mini_img = pygame.transform.rotate(self.enemy_img, 180)
        self.player_power_up_img = pygame.image.load(path.join(self.img_dir, "playerShip3_blue.png")).convert()
        self.bullet_img = pygame.image.load(path.join(self.img_dir, "laserRed16.png")).convert()

        self.meteors_file_names_list = ['meteor_big1.png', 'meteor_big2.png', 'meteor_big3.png', 'meteor_big4.png',
                                        'meteor_med1.png',
                                        'meteor_med2.png', 'meteor_small1.png', 'meteor_small2.png',
                                        'meteor_tiny1.png', 'meteor_tiny2.png']

        self.meteor_mobs_images = [pygame.image.load(path.join(self.img_dir, 'meteors', 'brown', img)).convert() for img
                                   in
                                   self.meteors_file_names_list]

        self.meteor_obstacles_images = [pygame.image.load(path.join(self.img_dir, 'meteors', 'grey', img)).convert() for
                                        img in
                                        self.meteors_file_names_list]

        self.explosion_animations = {'lg': [], 'sm': [], 'player': []}

        self.player_mini_img = pygame.transform.scale(self.player_img, (25, 19))
        self.player_mini_img.set_colorkey(BLACK)

        self.power_up_images = {
            'shield': pygame.image.load(path.join(self.img_dir, 'powerups', 'shield_gold.png')).convert(),
            'gun': pygame.image.load(path.join(self.img_dir, 'powerups', 'bolt_gold.png')).convert(),
            'fuel': pygame.image.load(path.join(self.img_dir, 'powerups', 'fuel_gold.png')).convert()}

        self.font_name = path.join(self.misc_dir, 'kenvector_future_thin.ttf')

    def load_explosions_animations(self, image_directory, filename_prefix, index):
        img_filename = filename_prefix.format(index)
        explosion_image = pygame.image.load(path.join(image_directory, 'Explosions_kenney', img_filename)).convert()
        explosion_image.set_colorkey(BLACK)
        return explosion_image
