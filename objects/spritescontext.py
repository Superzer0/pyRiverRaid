class SpritesContext:
    def __init__(self, mobs, obstacles, bullets, powerups, enemies, enemies_shots):
        self._player = None
        self._mobs = mobs
        self._obstacles = obstacles
        self._bullets = bullets
        self._powerups = powerups
        self._enemies = enemies
        self._enemies_shots = enemies_shots

        # player's properties
        self.playerCanShot = True

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        self._player = player
