import itertools

from objects.globals.gamesettings import GameSettings


class SpritesContext:
    def __init__(self, mobs, obstacles, bullets, power_ups, enemies, straight_enemies, enemies_shots):
        self.__player = None
        self.__bridge = None
        self.__mobs = mobs
        self.__obstacles = obstacles
        self.__bullets = bullets
        self.__power_ups = power_ups
        self.__enemies = enemies
        self.__straight_enemies = straight_enemies
        self.__enemies_shots = enemies_shots

        # player's properties
        self.playerCanShot = True

        # game speed's properties
        self.gameSpeedUp = False
        self.speedGameHasChanged = False

        self.enable_sprites = True
        self.bridgeWasDestroyed = False
        self.__level_threshold = GameSettings.LEVEL_INITIAL_THRESHOLD

    def set_level_threshold(self, level):
        self.__level_threshold = level * GameSettings.LEVEL_INITIAL_THRESHOLD

    def speed_up_sprites(self):
        for sprite in self.__get_all_sprites():
            sprite.speed_up()

    def slow_down_sprites(self):
        for sprite in self.__get_all_sprites():
            sprite.slow_down()

    def __get_all_sprites(self):
        return list(itertools.chain(self.__mobs, self.__obstacles, self.__bullets,
                                    self.__power_ups, self.__enemies, self.__straight_enemies,
                                    self.__enemies_shots))

    @property
    def player(self):
        return self.__player

    @property
    def bridge(self):
        return self.__bridge

    @property
    def level_threshold(self):
        return self.__level_threshold

    @property
    def obstacles(self):
        return self.__obstacles

    @property
    def bullets(self):
        return self.__bullets

    @property
    def mobs(self):
        return self.__mobs

    @property
    def power_ups(self):
        return self.__power_ups

    @property
    def enemies_shots(self):
        return self.__enemies_shots

    @property
    def enemies(self):
        return self.__enemies

    @property
    def straight_enemies(self):
        return self.__straight_enemies

    @player.setter
    def player(self, player):
        self.__player = player

    @bridge.setter
    def bridge(self, bridge):
        self.__bridge = bridge

    @level_threshold.setter
    def level_threshold(self, level):
        self.__level_threshold = level
