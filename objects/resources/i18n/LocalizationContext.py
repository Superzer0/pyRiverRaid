from objects.resources.i18n.game_over_screen_localization import GameOverLocalization
from objects.resources.i18n.game_screen_localization import GameScreenLocalization
from objects.resources.i18n.start_screen_localization import StartScreenLocalization


class LocalizationContext:
    def __init__(self, config, section_name=None):
        self.__game_screen_localization = GameScreenLocalization(config, section_name)
        self.__start_screen_localization = StartScreenLocalization(config, section_name)
        self.__game_over_screen_localization = GameOverLocalization(config, section_name)

    @property
    def game_over_screen(self):
        return self.__game_over_screen_localization

    @property
    def main_game_screen(self):
        return self.__game_screen_localization

    @property
    def initial_screen(self):
        return self.__start_screen_localization
