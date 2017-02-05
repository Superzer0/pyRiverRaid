import configparser
import os
from logging.config import fileConfig

from objects.leaderboards.leaderboard_service import LeaderBoardService
from objects.player import *
from objects.resources.ImgResources import ImgResources
from objects.resources.MiscResources import MiscResources
from objects.resources.ResourcesContext import ResourceContext
from objects.resources.SoundResources import SoundResources
from objects.resources.i18n.LocalizationContext import LocalizationContext
from objects.screens.base_screen import BaseScreen
from objects.screens.game_menu_screen import GameMenuScreen
from objects.screens.game_over_screen import GameOverScreen
from objects.screens.game_screens import GameScreens
from objects.screens.leader_board_screen import LeaderBoardScreen
from objects.screens.main_game_screen import MainGameScreen


def load_resources(folder):
    try:
        context = ResourceContext()
        config_reader = configparser.ConfigParser()
        config_reader.read(os.path.join('configuration', 'resources.ini'))
        context.soundResources = SoundResources(folder, config_reader)
        context.soundResources.load_default_music()
        context.miscResources = MiscResources(folder, config_reader)
        context.imgResources = ImgResources(folder, config_reader)
        return context
    except IOError:
        logging.error("Cannot load resources.")
        raise


def load_localization():
    try:
        config_reader = configparser.ConfigParser()
        config_reader.read(os.path.join('configuration', 'translations.ini'))
        return LocalizationContext(config_reader)
    except IOError:
        logging.error("Cannot load translations.")
        raise


if __name__ == '__main__':

    logging.info('starting game...')
    game_folder = os.path.dirname(__file__)
    fileConfig(os.path.join('configuration', 'logging.ini'))

    # set up asset folders

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mixer.init()
    py_game_screen = pygame.display.set_mode((GameSettings.WIDTH, GameSettings.HEIGHT))
    py_game_clock = pygame.time.Clock()
    # Ignore mouse motion (greatly reduces resources when not needed)
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    resource_context = load_resources(game_folder)
    localization_context = load_localization()

    pygame.display.set_caption(localization_context.initial_screen.title_label)

    leader_board_service = LeaderBoardService(os.path.join(game_folder, 'logs', 'leader_board.csv'))

    gameMenuScreen = GameMenuScreen(resource_context, localization_context)
    mainScreen = MainGameScreen(resource_context, localization_context)
    gameOverScreen = GameOverScreen(resource_context, localization_context, leader_board_service)
    leaderBoardScreen = LeaderBoardScreen(resource_context, localization_context, leader_board_service)
    gameScreenResult = None

    # play the music
    pygame.mixer.music.play(loops=-1)

    screens_flow = {
        GameScreens.START_SCREEN: lambda state: gameMenuScreen.run(py_game_clock, py_game_screen, state),
        GameScreens.GAME_SCREEN: lambda state: mainScreen.run(py_game_clock, py_game_screen, state),
        GameScreens.GAME_OVER_SCREEN: lambda state: gameOverScreen.run(py_game_clock, py_game_screen, state),
        GameScreens.LEADER_BOARD_SCREEN: lambda state: leaderBoardScreen.run(py_game_clock, py_game_screen, state),
        GameScreens.QUIT_GAME: lambda state: pygame.quit()
    }

    screen_result = gameMenuScreen.run(py_game_clock, py_game_screen)

    while True:
        next_action = screens_flow[screen_result[BaseScreen.SCREEN_NEXT]]
        screen_result = next_action(screen_result)
        if not screen_result:
            break
