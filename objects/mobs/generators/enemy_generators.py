import random

from objects.globals.gamesettings import GameSettings
from objects.mobs.enemy import Enemy
from objects.mobs.straight_enemy import StraightEnemy


class EnemyGenerator:
    def __init__(self, spriteContext, imgResources, all_sprites):
        self.imgResources = imgResources
        self.spriteContext = spriteContext
        self.all_sprites = all_sprites

    def generate_enemy(self):
        if len(self.spriteContext.enemies) < random.randrange(0, GameSettings.MAX_ENEMIES) and random.random() > 0.9:
            enemy = Enemy(self.all_sprites, self.spriteContext.enemies, self.spriteContext.enemies_shots,
                          self.imgResources)
            self.spriteContext.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def generate_straight_enemy(self):
        if len(self.spriteContext.straight_enemies) < \
                random.randrange(0, GameSettings.MAX_STRAIGHT_ENEMIES) and random.random() > 0.6:
            enemy = StraightEnemy(self.all_sprites, self.spriteContext.enemies, self.spriteContext.enemies_shots,
                                  self.imgResources, 2)
            self.spriteContext.straight_enemies.add(enemy)
            self.all_sprites.add(enemy)
