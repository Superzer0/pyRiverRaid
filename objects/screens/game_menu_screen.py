import logging

import pygame

from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings
from objects.screens.base_screen import BaseScreen
from objects.screens.game_screens import GameScreens
from objects.ui.button import Button


class GameMenuScreen(BaseScreen):

    def __init__(self, resourceContext, localizationContext):
        BaseScreen.__init__(self, resourceContext)
        self.__logger = logging.getLogger(GameMenuScreen.__module__)
        self.__resourceContext = resourceContext
        self.__localizationContext = localizationContext

    def run(self, clock, screen, args=None):
        buttons_sprites = pygame.sprite.Group()
        start_game_button = Button(GameSettings.WIDTH / 2, GameSettings.HEIGHT * 0.5 + 50,
                                   self.__resourceContext,
                                   self.__localizationContext.initial_screen.start_button_label,
                                   GameScreens.GAME_SCREEN,
                                   True)

        buttons_sprites.add(start_game_button)

        leader_board_button = Button(GameSettings.WIDTH / 2, GameSettings.HEIGHT * 0.5 + 100,
                                     self.__resourceContext,
                                     self.__localizationContext.initial_screen.board_button_label,
                                     GameScreens.LEADER_BOARD_SCREEN)

        buttons_sprites.add(leader_board_button)

        exit_button = Button(GameSettings.WIDTH / 2, GameSettings.HEIGHT * 0.5 + 150,
                             self.__resourceContext,
                             self.__localizationContext.initial_screen.exit_button_label,
                             GameScreens.QUIT_GAME)

        buttons_sprites.add(exit_button)
        buttons_list = [start_game_button, leader_board_button, exit_button]

        running = True
        focused_button_index = 0
        next_screen = GameScreens.GAME_SCREEN
        while running:
            clock.tick(GameSettings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_screen = GameScreens.QUIT_GAME
                    running = False
                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_SPACE:
                        next_screen = buttons_list[focused_button_index].id
                        running = False

                    if event.key == pygame.K_UP:
                        focused_button_index = (focused_button_index - 1) % 3
                    if event.key == pygame.K_DOWN:
                        focused_button_index = (focused_button_index + 1) % 3

                    [button.focus(False) for button in buttons_list]
                    buttons_list[focused_button_index].focus(True)

            buttons_sprites.update(screen)

            screen.fill(GameColors.BLACK)
            screen.blit(self.__resourceContext.imgResources.background,
                        self.__resourceContext.imgResources.background.get_rect())

            buttons_sprites.draw(screen)

            self.draw_text(screen, self.__localizationContext.initial_screen.title_label, 64, GameSettings.WIDTH / 2,
                           GameSettings.HEIGHT / 4)

            self.draw_text(screen, self.__localizationContext.initial_screen.instructions_1_label, 22,
                           GameSettings.WIDTH / 2, GameSettings.HEIGHT - 100)

            pygame.display.flip()

        return {BaseScreen.SCREEN_NEXT: next_screen}
