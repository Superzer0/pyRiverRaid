from objects.resources.i18n.game_over_screen_localization import GameOverLocalization
from objects.resources.i18n.game_screen_localization import GameScreenLocalization
from objects.resources.i18n.leader_boards_localization import LeaderBoardLocalization
from objects.resources.i18n.start_screen_localization import StartScreenLocalization


class LocalizationContext:
    """Holds references for all localization related classes"""
    def __init__(self, config, section_name=None):
        self.__game_screen_localization = GameScreenLocalization(config, section_name)
        self.__start_screen_localization = StartScreenLocalization(config, section_name)
        self.__game_over_screen_localization = GameOverLocalization(config, section_name)
        self.__leader_board_localization = LeaderBoardLocalization(config, section_name)

    @property
    def game_over_screen(self):
        """game over screen related labels"""
        return self.__game_over_screen_localization

    @property
    def main_game_screen(self):
        """main game screen related labels"""
        return self.__game_screen_localization

    @property
    def initial_screen(self):
        """game menu screen related labels"""
        return self.__start_screen_localization

    @property
    def leader_board_screen(self):
        """leader board screen related labels"""
        return self.__leader_board_localization
