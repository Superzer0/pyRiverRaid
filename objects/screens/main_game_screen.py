import datetime
from objects.bridge import Bridge
from objects.explosion import Explosion
from objects.globals.gamesettings import GameSettings
from objects.leaderboards.leaderboard_entry import LeaderboardEntry
from objects.mobs.enemy import Enemy
from objects.mobs.generators.enemy_generators import EnemyGenerator
from objects.mobs.generators.mob_generator import MobGenerator
from objects.mobs.generators.powerup_generators import *
from objects.mobs.randommeteor import RandomMeteor
from objects.mobs.rotatingmeteor import RotatingMeteor
from objects.mobs.straight_enemy import StraightEnemy
from objects.player import *
from objects.resources import ImgResources
from objects.resources.ImgResources import ImgResources
from objects.screens.base_screen import BaseScreen
from objects.screens.game_screens import GameScreens
from objects.spritescontext import SpritesContext


class MainGameScreen(BaseScreen):
    def __init__(self, resourceContext, localizationContext):
        BaseScreen.__init__(self, resourceContext)
        self.__logger = logging.getLogger(MainGameScreen.__module__)
        self.__resourceContext = resourceContext
        self.__localizationContext = localizationContext
        self.__hits = 0
        self.__power_ups = 0
        self.__level = 1

    def __init_screen(self):
        self.all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        straight_enemies = pygame.sprite.Group()
        enemies_shots = pygame.sprite.Group()
        self.spriteContext = SpritesContext(mobs, obstacles, bullets, powerups, enemies, straight_enemies,
                                            enemies_shots)
        player = Player(self.__resourceContext.imgResources, self.__resourceContext.soundResources, self.all_sprites,
                        bullets, self.spriteContext)
        self.all_sprites.add(player)
        self.spriteContext.player = player

        self.gunGenerator = GunGenerator(player, self.__resourceContext.imgResources, self.all_sprites, powerups)
        self.shieldGenerator = ShieldGenerator(player, self.__resourceContext.imgResources, self.all_sprites, powerups)
        self.fuelGenerator = FuelGenerator(player, self.__resourceContext.imgResources, self.all_sprites, powerups)
        self.enemyGenerator = EnemyGenerator(self.spriteContext, self.__resourceContext.imgResources, self.all_sprites)
        self.mobGenerator = MobGenerator(self.spriteContext, self.__resourceContext.imgResources, self.all_sprites)

        self.levels = [GameSettings.LEVEL_1, GameSettings.LEVEL_2, GameSettings.LEVEL_3, GameSettings.LEVEL_4,
                       GameSettings.LEVEL_5]
        self.spriteContext.currentLevel = self.levels[0]

        # left obstacles
        for i in range(GameSettings.MAX_OBSTACLES):
            self.__new_obstacle(i, random.randrange(0, GameSettings.WIDTH_OBSTACLES - 50))

        # right obstacles
        for i in range(GameSettings.MAX_OBSTACLES):
            self.__new_obstacle(i, random.randrange(GameSettings.WIDTH - GameSettings.WIDTH_OBSTACLES - 50,
                                                    GameSettings.WIDTH - 10))


    def run(self, clock, screen, args=None):
        self.__init_screen()
        running = True
        score = 0
        player = self.spriteContext.player
        next_screen = GameScreens.GAME_OVER_SCREEN
        while running:
            # keep loop running at the right speed
            clock.tick(GameSettings.FPS)

            self.all_sprites.update(screen)

            score += self.__mob_shot_down()
            score += self.__player_shoot_down_enemy()

            self.__player_got_power_up(player)
            self.__player_shoot_down_power_up()

            running = self.__player_check_fuel(player)
            running = self.__player_hit_by_mob(player, running)
            running = self.__player_hit_by_obstacle(player, running)
            running = self.__player_hit_enemy(player, running)
            running = self.__player_hit_straight_enemy(player, running)
            running = self.__enemy_shot_down_player(player, running)

            if score > self.spriteContext.currentLevel and self.spriteContext.enableSprites:
                self.spriteContext.enableSprites = False
                bridge = Bridge(self.spriteContext, self.__resourceContext.imgResources)
                self.spriteContext.bridge = bridge
                self.all_sprites.add(bridge)

            if score > self.spriteContext.currentLevel:
                running = self.__enemy_shot_down_bridge(running)

            if self.spriteContext.enableSprites:
                self.fuelGenerator.generate()
                self.enemyGenerator.generate_straight_enemy()
                self.enemyGenerator.generate_enemy()
                self.mobGenerator.generate()

            # Draw / render
            self.draw_sprites(player, score, screen)

            # *after* drawing everything, flip the display
            pygame.display.flip()

            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                    next_screen = GameScreens.QUIT_GAME

        self.__clean_up_screen(screen)

        return {BaseScreen.SCREEN_NEXT: next_screen,
                LeaderboardEntry.LEVEL: self.__level,
                LeaderboardEntry.POWER_UPS: self.__power_ups,
                LeaderboardEntry.HITS: self.__hits,
                LeaderboardEntry.SCORE: score,
                LeaderboardEntry.DATE: datetime.datetime.now(),
                LeaderboardEntry.PLAYER_NAME: 'anonymous player ' + str(random.randint(1, 20))}

    def draw_sprites(self, player, score, screen):
        screen.fill(GameColors.BLACK)
        screen.blit(self.__resourceContext.imgResources.background,
                    self.__resourceContext.imgResources.background.get_rect())
        self.all_sprites.draw(screen)
        self.draw_text(screen, str(score), 30, GameSettings.WIDTH / 2, 20)
        self.draw_text(screen, self.__localizationContext.main_game_screen.shield_label, 16, 35, 7)
        self.__draw_hud_bar(screen, GameColors.GREEN, 70, 10, player.shield)
        self.draw_text(screen, self.__localizationContext.main_game_screen.fuel_label, 16, 35, 27)
        self.__draw_hud_bar(screen, GameColors.RED, 70, 31, player.fuel)
        self.__draw_lives(screen, GameSettings.WIDTH - 150, 5, player.lives,
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
        enemy_hits = pygame.sprite.groupcollide(self.spriteContext.enemies, self.spriteContext.bullets, True,
                                                pygame.sprite.collide_circle)

        straight_enemy_hits = pygame.sprite.groupcollide(self.spriteContext.straight_enemies,
                                                         self.spriteContext.bullets, True,
                                                         pygame.sprite.collide_circle)

        hits = []
        hits.extend(enemy_hits)
        hits.extend(straight_enemy_hits)

        score_change = 0
        for hit in hits:
            self.spriteContext.playerCanShot = True
            random.choice(self.__resourceContext.soundResources.explosion_sounds).play()
            death_explosion = Explosion(hit.rect.center,
                                        self.__resourceContext.imgResources.EXPLOSION_ANIMATIONS_PLAYER,
                                        self.__resourceContext.imgResources.explosion_animations)
            self.all_sprites.add(death_explosion)
            hit.kill()
            self.__hits += 1
            score_change += abs(GameSettings.BASE_SCORE_FOR_ENEMY - hit.radius)
            random.choice([self.shieldGenerator, self.gunGenerator]).generate()
        return score_change

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

    def __player_hit_straight_enemy(self, player, running):
        hits = pygame.sprite.spritecollide(player, self.spriteContext.straight_enemies, True)

        if hits:
            hit = hits[0]
            running = self.__player_collide(hit, lambda: self.__new_obstacle(1, hit.rect.x))
            self.__new_straight_enemy()

        return running

    def __player_shoot_down_power_up(self):
        hits = pygame.sprite.groupcollide(self.spriteContext.power_ups, self.spriteContext.bullets, True, True)
        for hit in hits:
            random.choice(self.__resourceContext.soundResources.explosion_sounds).play()
            explosion = Explosion(hit.rect.center, self.__resourceContext.imgResources.EXPLOSION_ANIMATIONS_SM,
                                  self.__resourceContext.imgResources.explosion_animations)
            self.all_sprites.add(explosion)
            self.spriteContext.playerCanShot = True

    def __player_got_power_up(self, player):
        hits = pygame.sprite.spritecollide(player, self.spriteContext.power_ups, True)
        for hit in hits:
            player.power_up(hit.type)
            self.__power_ups += 1

    def __player_hit_by_obstacle(self, player, running):
        hits = pygame.sprite.spritecollide(player, self.spriteContext.obstacles, True, pygame.sprite.collide_circle)
        for hit in hits:
            running = self.__player_collide(hit, lambda: self.__new_obstacle(1, hit.rect.x))
        return running

    def __player_hit_by_mob(self, player, running):
        hits = pygame.sprite.spritecollide(player, self.spriteContext.mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            running = self.__player_collide(hit, lambda: None)
        return running

    def __enemy_shot_down_bridge(self, running):
        hits = pygame.sprite.spritecollide(self.spriteContext.bridge, self.spriteContext.bullets,
                                           pygame.sprite.collide_circle)
        for hit in hits:
            self.spriteContext.bridge.take_hit();
            self.spriteContext.playerCanShot = True
            print("bridge: " + str(self.spriteContext.bridge.shield))
            if not self.spriteContext.bridge.is_alive():
                self.spriteContext.bridge = None
                self.spriteContext.enableSprites = True
                self.bridgeWasDestroyed = True
                index = self.levels.index(self.spriteContext.currentLevel)
                self.spriteContext.currentLevel = self.levels[index + 1]
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
            score_change += GameSettings.BASE_SCORE_FOR_ENEMY - hit.radius
            self.__hits += 1
            self.spriteContext.playerCanShot = True

        return score_change

    def __clean_up_screen(self, screen):
        self.all_sprites.empty()
        self.all_sprites.draw(screen)
        screen.fill(GameColors.BLACK)
        pygame.display.flip()

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

    def __new_straight_enemy(self):
        enemy = StraightEnemy(self.all_sprites, self.spriteContext.enemies, self.spriteContext.enemies_shots,
                              self.__resourceContext.imgResources)
        self.spriteContext.straight_enemies.add(enemy)
        self.all_sprites.add(enemy)

    def __draw_lives(self, surf, x, y, lives, player_live_img):
        for live in range(lives):
            img_rect = player_live_img.get_rect()
            img_rect.x = x + 40 * live
            img_rect.y = y
            surf.blit(player_live_img, img_rect)

    def __draw_hud_bar(self, screen, color, x, y, pct):

        if pct < 0:
            pct = 0

        fill = (pct / 100) * GameSettings.BAR_LENGTH
        outline_rect = pygame.Rect(x, y, GameSettings.BAR_LENGTH, GameSettings.BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, GameSettings.BAR_HEIGHT)
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
                return False
        return True
