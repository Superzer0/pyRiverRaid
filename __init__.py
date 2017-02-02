import configparser
import os
from logging.config import fileConfig

from objects.leaderboards.leaderboard_service import LeaderBoardService
from objects.player import *
from objects.powerup_generators import *
from objects.resources.ImgResources import ImgResources
from objects.resources.MiscResources import MiscResources
from objects.resources.ResourcesContext import ResourceContext
from objects.resources.SoundResources import SoundResources
from objects.resources.i18n.LocalizationContext import LocalizationContext
from objects.screens.base_screen import BaseScreen
from objects.screens.game_menu_screen import GameMenuScreen
from objects.screens.game_over_screen import GameOverScreen
from objects.screens.main_game_screen import MainGameScreen


def load_resources(folder):
    try:
        context = ResourceContext()
        configReader = configparser.ConfigParser()
        configReader.read(os.path.join('configuration', 'resources.ini'))
        context.soundResources = SoundResources(folder, configReader)
        context.soundResources.load_default_music()
        context.miscResources = MiscResources(folder, configReader)
        context.imgResources = ImgResources(folder, configReader)
        return context
    except IOError:
        logging.error("Cannot load resources.")
        raise


def load_localization():
    try:
        configReader = configparser.ConfigParser()
        configReader.read(os.path.join('configuration', 'translations.ini'))
        return LocalizationContext(configReader)
    except IOError:
        logging.error("Cannot load translations.")
        raise


if __name__ == '__main__':

    logging.info('starting game...')
    game_folder = os.path.dirname(__file__)
    fileConfig(os.path.join('configuration', 'logging.ini'))

    # set up asset folders

    pygame.init()
    pygame.mixer.init()
    py_game_screen = pygame.display.set_mode((GameSettings.WIDTH, GameSettings.HEIGHT))
    py_game_clock = pygame.time.Clock()

    resource_context = load_resources(game_folder)
    localization_context = load_localization()

    pygame.display.set_caption(localization_context.initial_screen.title_label)

    leader_board_service = LeaderBoardService(os.path.join(game_folder, 'logs', 'leader_board.csv'))

    gameMenuScreen = GameMenuScreen(resource_context, localization_context)
    mainScreen = MainGameScreen(resource_context, localization_context)
    gameOverScreen = GameOverScreen(resource_context, localization_context, leader_board_service)
    gameScreenResult = None

    # play the music
    pygame.mixer.music.play(loops=-1)
    for gameScreen in [gameMenuScreen, mainScreen, gameOverScreen]:
        gameScreenResult = gameScreen.run(py_game_clock, py_game_screen, gameScreenResult)
        if not BaseScreen.screen_finished_normally(gameScreenResult):
            pygame.quit()
            break

    pygame.quit()
