import pygame
import random
from objects.enemy import Enemy
from objects.explosion import Explosion
from objects.mobs.randommeteor import RandomMeteor
from objects.mobs.rotatingmeteor import RotatingMeteor
from objects.resource import Resource


class Context:
    def __init__(self):
        self.resource = Resource()

        # sprites collections
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemies_shots = pygame.sprite.Group()

        self.playerCanShot = True
        self.player = None

    def new_mob(self):
        m = RandomMeteor(meteor_mobs_images)
        self.all_sprites.add(m)
        self.mobs.add(m)

    def new_obstacle(self, i, start_x):
        m = RotatingMeteor(self.resource.meteor_obstacles_images, start_x,
                           random.randrange(-300, (15 * i)), 0, random.randrange(1, 2), random.randrange(-2, 2))
        self.all_sprites.add(m)
        self.obstacles.add(m)

    def new_enemy(self):
        enemy = Enemy(self.all_sprites, self.enemies, self.enemies_shots, self.resource.enemy_mini_img,
                      self.resource.bullet_img, self)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)
