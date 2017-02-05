class SpritesContext:
    def __init__(self, mobs, obstacles, bullets, powerups, enemies, straight_enemies, enemies_shots):
        self._player = None
        self._mobs = mobs
        self._obstacles = obstacles
        self._bullets = bullets
        self._powerups = powerups
        self._enemies = enemies
        self._straight_enemies = straight_enemies
        self._enemies_shots = enemies_shots

        # player's properties
        self.playerCanShot = True

        # game speed's properties
        self.gameSpeedUp = False
        self.speedGameHasChanged = False

    def speedUpSprites(self):
        for bullet in self.bullets:
            bullet.speedUp()

        for straight_enemy in self.straight_enemies:
            straight_enemy.speedUp()

        for enemy in self.enemies:
            enemy.speedUp()

        for powerup in self.powerups:
            powerup.speedUp()

    def slowDownSprites(self):
        for bullet in self.bullets:
            bullet.speedy = bullet.slowDown()

        for straight_enemy in self.straight_enemies:
            straight_enemy.slowDown()

        for enemy in self.enemies:
            enemy.slowDown()

        for powerup in self.powerups:
            powerup.slowDown()

    @property
    def player(self):
        return self._player

    @property
    def obstacles(self):
        return self._obstacles

    @property
    def bullets(self):
        return self._bullets

    @property
    def mobs(self):
        return self._mobs

    @property
    def powerups(self):
        return self._powerups

    @property
    def enemies_shots(self):
        return self._enemies_shots

    @property
    def enemies(self):
        return self._enemies

    @property
    def straight_enemies(self):
        return self._straight_enemies

    @player.setter
    def player(self, player):
        self._player = player
