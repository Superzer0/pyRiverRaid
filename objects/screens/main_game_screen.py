from objects.enemy import Enemy
from objects.explosion import Explosion
from objects.mobs.randommeteor import RandomMeteor
from objects.mobs.rotatingmeteor import RotatingMeteor
from objects.player import *
from objects.powerup_generators import *
from objects.resources import ImgResources
from objects.resources.ImgResources import ImgResources
from objects.screens.base_screen import BaseScreen
from objects.spritescontext import SpritesContext


class MainGameScreen(BaseScreen):
    def __init__(self, resourceContext, localizationContext):
        BaseScreen.__init__(self, resourceContext)
        self.__logger = logging.getLogger(MainGameScreen.__module__)
        self.__resourceContext = resourceContext
        self.__localizationContext = localizationContext
        self.__score = 0

    def __init_screen(self):
        self.all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        enemies_shots = pygame.sprite.Group()
        self.spriteContext = SpritesContext(mobs, obstacles, bullets, powerups, enemies, enemies_shots)
        player = Player(self.__resourceContext.imgResources, self.__resourceContext.soundResources, self.all_sprites,
                        bullets, self.spriteContext)
        self.all_sprites.add(player)
        self.spriteContext.player = player

        self.shieldGenerator = ShieldGenerator(player, self.__resourceContext.imgResources, self.all_sprites, powerups)
        self.fuelGenerator = FuelGenerator(player, self.__resourceContext.imgResources, self.all_sprites, powerups)

        # left obstacles
        for i in range(100):
            self.__new_obstacle(i, random.randrange(0, GameSettings.WIDTH_OBSTACLES - 50))

        # right obstacles
        for i in range(100):
            self.__new_obstacle(i, random.randrange(GameSettings.WIDTH - GameSettings.WIDTH_OBSTACLES - 50,
                                                    GameSettings.WIDTH - 10))

        # for i in range(20):
        #     new_mob()

        for i in range(5):
            self.__new_enemy()

    def run(self, clock, screen, args=None):
        self.__init_screen()
        running = True
        score = 0
        player = self.spriteContext.player
        quit_reason = BaseScreen.SCREEN_END_REASON_NORMAL

        while running:
            # keep loop running at the right speed
            clock.tick(GameSettings.FPS)

            self.all_sprites.update(screen)

            score += self.__mob_shot_down()

            self.__player_got_power_up(player)
            self.__player_shoot_down_power_up()
            self.__player_shoot_down_enemy()

            running = self.__player_check_fuel(player)
            running = self.__player_hit_by_mob(player, running)
            running = self.__player_hit_by_obstacle(player, running)
            running = self.__player_hit_enemy(player, running)
            running = self.__enemy_shot_down_player(player, running)

            self.fuelGenerator.generate()

            # Draw / render
            self.draw_sprites(player, score, screen)

            # *after* drawing everything, flip the display
            pygame.display.flip()

            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                    quit_reason = BaseScreen.SCREEN_END_REASON_QUIT

        self.__clean_up_screen(screen)
        return {BaseScreen.SCREEN_END_REASON: quit_reason, 'score': score}

    def draw_sprites(self, player, score, screen):
        screen.fill(GameColors.BLACK)
        screen.blit(self.__resourceContext.imgResources.background,
                    self.__resourceContext.imgResources.background.get_rect())
        self.all_sprites.draw(screen)
        self.draw_text(screen, str(score), 30, GameSettings.WIDTH / 2, 20)
        self.draw_text(screen, self.__localizationContext.GameScreen.shield_label, 16, 35, 7)
        self.__draw_hud_bar(screen, GameColors.GREEN, 70, 10, player.shield)
        self.draw_text(screen, self.__localizationContext.GameScreen.fuel_label, 16, 35, 27)
        self.__draw_hud_bar(screen, GameColors.RED, 70, 31, player.fuel)
        self.__draw_lives(screen, GameSettings.WIDTH - 100, 5, player.lives,
                          self.__resourceContext.imgResources.player_mini_img)

    def __player_check_fuel(self, player):
        if not player.has_fuel():
            self.__resourceContext.soundResources.player_die_sound.play()
            death_explosion = Explosion(self.spriteContext.player.rect.center,
                                        ImgResources.EXPLOSION_ANIMATIONS_PLAYER,
                                        self.__resourceContext.imgResources.explosion_animations)
            self.all_sprites.add(death_explosion)
            player.fuel_is_empty()

            if death_explosion.alive():
                player.hide()

        return player.is_alive()

    def __player_shoot_down_enemy(self):
        hits = pygame.sprite.groupcollide(self.spriteContext.enemies, self.spriteContext.bullets, True,
                                          pygame.sprite.collide_circle)
        for hit in hits:
            self.spriteContext.playerCanShot = True
            death_explosion = Explosion(hit.rect.center,
                                        self.__resourceContext.imgResources.EXPLOSION_ANIMATIONS_PLAYER,
                                        self.__resourceContext.imgResources.explosion_animations)
            self.all_sprites.add(death_explosion)
            hit.kill()
            if len(self.spriteContext.enemies.sprites()) <= GameSettings.MAX_ENEMIES:
                self.__new_enemy()

    def __enemy_shot_down_player(self, player, running):
        # check to see if a enemy's shot hit the player
        hits = pygame.sprite.spritecollide(player, self.spriteContext.enemies_shots, True,
                                           pygame.sprite.collide_circle)
        for hit in hits:
            running = self.__player_collide(hit, lambda: self.__new_enemy())

        return running

    def __player_hit_enemy(self, player, running):
        hits = pygame.sprite.spritecollide(player, self.spriteContext.enemies, True)
        if hits:
            hit = hits[0]
            running = self.__player_collide(hit, lambda: self.__new_obstacle(1, hit.rect.x))
            self.__new_enemy()

        return running

    def __player_shoot_down_power_up(self):
        hits = pygame.sprite.groupcollide(self.spriteContext.powerups, self.spriteContext.bullets, True, True)
        for hit in hits:
            random.choice(self.__resourceContext.soundResources.explosion_sounds).play()
            explosion = Explosion(hit.rect.center, self.__resourceContext.imgResources.EXPLOSION_ANIMATIONS_SM,
                                  self.__resourceContext.imgResources.explosion_animations)
            self.all_sprites.add(explosion)
            self.spriteContext.playerCanShot = True

    def __player_got_power_up(self, player):
        hits = pygame.sprite.spritecollide(player, self.spriteContext.powerups, True)
        for hit in hits:
            player.power_up(hit.type)

    def __player_hit_by_obstacle(self, player, running):
        hits = pygame.sprite.spritecollide(player, self.spriteContext.obstacles, True, pygame.sprite.collide_circle)
        for hit in hits:
            running = self.__player_collide(hit, lambda: self.__new_obstacle(1, hit.rect.x))
        return running

    def __player_hit_by_mob(self, player, running):
        hits = pygame.sprite.spritecollide(player, self.spriteContext.mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            running = self.__player_collide(hit, lambda: self.__new_mob())
        return running

    def __mob_shot_down(self):
        hits = pygame.sprite.groupcollide(self.spriteContext.mobs, self.spriteContext.bullets, True, True)
        score_change = 0
        for hit in hits:
            random.choice(self.__resourceContext.soundResources.explosion_sounds).play()

            explosion = Explosion(hit.rect.center, self.__resourceContext.imgResources.EXPLOSION_ANIMATIONS_LG,
                                  self.__resourceContext.imgResources.explosion_animations)

            self.all_sprites.add(explosion)
            self.shieldGenerator.generate()
            self.__new_mob()
            score_change += 50 - hit.radius

        return score_change

    def __clean_up_screen(self, screen):
        self.all_sprites.empty()
        self.all_sprites.draw(screen)
        pygame.display.flip()

    def __new_mob(self):
        m = RandomMeteor(self.__resourceContext.imgResources.meteor_mobs_img)
        self.all_sprites.add(m)
        self.spriteContext.mobs.add(m)

    def __new_obstacle(self, i, start_x):
        m = RotatingMeteor(self.__resourceContext.imgResources.meteor_obstacles_img, start_x,
                           random.randrange(-300, (15 * i)), 0, random.randrange(1, 2), random.randrange(-2, 2))
        self.all_sprites.add(m)
        self.spriteContext.obstacles.add(m)

    def __new_enemy(self):
        enemy = Enemy(self.all_sprites, self.spriteContext.enemies, self.spriteContext.enemies_shots,
                      self.__resourceContext.imgResources)
        self.spriteContext.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def __draw_lives(self, surf, x, y, lives, player_live_img):
        for live in range(lives):
            img_rect = player_live_img.get_rect()
            img_rect.x = x + 30 * live
            img_rect.y = y
            surf.blit(player_live_img, img_rect)

    def __draw_hud_bar(self, screen, color, x, y, pct):

        if pct < 0:
            pct = 0

        fill = (pct / 100) * GameSettings.BAR_LENGTH
        outline_rect = pygame.Rect(x, y, GameSettings.BAR_LENGTH, GameSettings.BAR_HEIGTH)
        fill_rect = pygame.Rect(x, y, fill, GameSettings.BAR_HEIGTH)
        pygame.draw.rect(screen, color, fill_rect)
        pygame.draw.rect(screen, GameColors.WHITE, outline_rect, 2)

    def __player_collide(self, hit, new_object_fun):
        is_terminal_hit = self.spriteContext.player.was_hit(hit.radius * 2)
        new_object_fun()
        player_explosion = Explosion(hit.rect.center, ImgResources.EXPLOSION_ANIMATIONS_SM,
                                     self.__resourceContext.imgResources.explosion_animations)
        random.choice(self.__resourceContext.soundResources.explosion_sounds).play()
        self.all_sprites.add(player_explosion)
        if is_terminal_hit:
            self.__logger.debug("player terminated by:" + str(hit))
            self.__resourceContext.soundResources.player_die_sound.play()
            death_explosion = Explosion(self.spriteContext.player.rect.center, ImgResources.EXPLOSION_ANIMATIONS_PLAYER,
                                        self.__resourceContext.imgResources.explosion_animations)
            self.all_sprites.add(death_explosion)
            self.spriteContext.player.recharge_fuel()
            self.spriteContext.player.hide()
            if not self.spriteContext.player.is_alive() and death_explosion.alive():
                return True
        return False
