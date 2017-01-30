from objects.resources.i18n.game_screen_locatization import GameScreenLocalization
from objects.resources.i18n.start_screen_localization import StartScreenLocalization


class LocalizationContext:
    def __init__(self, config, section_name=None):
        self.__game_screen_localization = GameScreenLocalization(config, section_name)
        self.__start_screen_localization = StartScreenLocalization(config, section_name)

    @property
    def GameScreen(self):
        return self.__game_screen_localization

    @property
    def InitialScreen(self):
        return self.__start_screen_localization
