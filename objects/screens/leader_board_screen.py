import logging

import pygame

from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings
from objects.screens.base_screen import BaseScreen
from objects.screens.game_screens import GameScreens
from objects.ui.button import Button


class LeaderBoardScreen(BaseScreen):
    COLUMN_WIDTH = 20
    PAGE_SIZE = 10

    def __init__(self, resourceContext, localizationContext, leaderBoardService):
        BaseScreen.__init__(self, resourceContext)
        self.__leaderBoardService = leaderBoardService
        self.__logger = logging.getLogger(LeaderBoardScreen.__module__)
        self.__resourceContext = resourceContext
        self.__localizationContext = localizationContext

    def run(self, clock, screen, args=None):

        page = 0
        focused_button_index = 0
        running = True

        self.__leaderBoardService.load_leader_board()
        leader_board = list(self.__leaderBoardService.leader_board)
        buttons_sprites = pygame.sprite.Group()
        next_page_button = Button(400, GameSettings.HEIGHT - 50,
                                  self.__resourceContext,
                                  self.__localizationContext.leader_board_screen.next_label,
                                  GameScreens.START_SCREEN,
                                  True)

        next_page_button.hit_action = lambda p: p + 1 if (p + 1) * LeaderBoardScreen.PAGE_SIZE <= len(
            leader_board) else p

        buttons_sprites.add(next_page_button)

        previous_page_button = Button(150, GameSettings.HEIGHT - 50,
                                      self.__resourceContext,
                                      self.__localizationContext.leader_board_screen.prev_label,
                                      GameScreens.START_SCREEN)

        previous_page_button.hit_action = lambda p: p - 1 if p - 1 >= 0 else p

        buttons_sprites.add(previous_page_button)

        exit_button = Button(GameSettings.WIDTH - 200, GameSettings.HEIGHT - 50,
                             self.__resourceContext,
                             self.__localizationContext.leader_board_screen.exit_label,
                             GameScreens.QUIT_GAME)

        exit_button.hit_action = lambda p: p

        buttons_sprites.add(exit_button)
        buttons_list = [next_page_button, previous_page_button, exit_button]

        next_screen = GameScreens.START_SCREEN
        while running:
            clock.tick(GameSettings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_screen = GameScreens.QUIT_GAME
                    running = False
                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_SPACE:
                        if buttons_list[focused_button_index].hit_action:
                            page = buttons_list[focused_button_index].hit_action(page)

                        if buttons_list[focused_button_index].id == GameScreens.QUIT_GAME:
                            running = False

                    if event.key == pygame.K_LEFT:
                        focused_button_index = (focused_button_index + 1) % 3

                    if event.key == pygame.K_RIGHT:
                        focused_button_index = (focused_button_index - 1) % 3

                    [button.focus(False) for button in buttons_list]
                    buttons_list[focused_button_index].focus(True)

            buttons_sprites.update(screen)

            screen.fill(GameColors.BLACK)
            screen.blit(self.__resourceContext.imgResources.background,
                        self.__resourceContext.imgResources.background.get_rect())

            buttons_sprites.draw(screen)

            self.draw_text(screen, self.__localizationContext.leader_board_screen.title_label, 64,
                           GameSettings.WIDTH // 2, 20)

            self.draw_text(screen, self.get_header_line(), 18, 100, 120, GameColors.WHITE, False)

            for i, entry in enumerate(leader_board[
                                      LeaderBoardScreen.PAGE_SIZE * page:
                                                      LeaderBoardScreen.PAGE_SIZE * page + LeaderBoardScreen.PAGE_SIZE]):
                self.draw_text(screen, self.get_data_line(i + LeaderBoardScreen.PAGE_SIZE * page, entry), 18, 100, 180
                               + i * 20, GameColors.WHITE, False)

            pygame.display.flip()

        return {BaseScreen.SCREEN_NEXT: next_screen}

    def get_data_line(self, i, entry):
        data_str = self.get_adjusted_column(i + 1)
        data_str += self.get_adjusted_column(entry.level)
        data_str += self.get_adjusted_column(entry.power_ups)
        data_str += self.get_adjusted_column(entry.hits)
        data_str += self.get_adjusted_column(entry.score)
        data_str += self.get_adjusted_column(entry.player_name)
        return data_str

    def get_header_line(self):
        header_str = self.get_adjusted_column(self.__localizationContext.leader_board_screen.header_lvl_label)
        header_str += self.get_adjusted_column(self.__localizationContext.leader_board_screen.header_lvl_label)
        header_str += self.get_adjusted_column(self.__localizationContext.leader_board_screen.header_power_label)
        header_str += self.get_adjusted_column(self.__localizationContext.leader_board_screen.header_hits_label)
        header_str += self.get_adjusted_column(self.__localizationContext.leader_board_screen.header_score_label)
        header_str += self.get_adjusted_column(self.__localizationContext.leader_board_screen.header_player_label)
        return header_str

    @staticmethod
    def get_adjusted_column(txt):
        return str(txt)[:LeaderBoardScreen.COLUMN_WIDTH].ljust(
            LeaderBoardScreen.COLUMN_WIDTH)
