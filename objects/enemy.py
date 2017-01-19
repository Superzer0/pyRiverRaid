import pygame
import random
from objects.bullet import Bullet
from objects.settings import BLACK
from objects.settings import HEIGHT
from objects.settings import MAX_ENEMIES
from objects.settings import WIDTH


class Enemy(pygame.sprite.Sprite):
    shoot_delay = 750

    def __init__(self, all_sprites, enemies, enemies_shots, imgResources):
        pygame.sprite.Sprite.__init__(self)
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.enemies_shots = enemies_shots
        self.image = imgResources.enemy_img
        self.image.set_colorkey(BLACK)
        self.bullet_img = imgResources.bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randrange(0, 10)
        self.rect.centerx = random.randrange(150, WIDTH - 150)
        self.speedy = 7
        self.radius = 100
        self.last_shot = pygame.time.get_ticks()
        self.hidden_time = pygame.time.get_ticks()
        self.power_time = pygame.time.get_ticks()

    def shot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > Enemy.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.bottom, self.bullet_img)
            bullet.speedy = 15
            self.all_sprites.add(bullet)
            self.enemies_shots.add(bullet)

    def update(self, *args):
        self.rect.y += self.speedy
        self.shot()
        if self.rect.bottom > HEIGHT and len(self.enemies.sprites()) < MAX_ENEMIES:
            self.rect.bottom = random.randrange(0, 10)
            self.rect.centerx = random.randrange(150, WIDTH - 150)
