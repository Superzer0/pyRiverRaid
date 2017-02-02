import logging

import pygame

from objects.globals.gamesettings import GameSettings
from objects.screens.base_screen import BaseScreen


class GameOverScreen(BaseScreen):
    def __init__(self, resourceContext, localizationContext):
        BaseScreen.__init__(self, resourceContext)
        self.__logger = logging.getLogger(GameOverScreen.__module__)
        self.__resourceContext = resourceContext
        self.__localizationContext = localizationContext

    def run(self, clock, screen, args=None):

        score = args.get('score', 0)

        self.draw_text(screen, self.__localizationContext.InitialScreen.game_over_label, 50,
                       GameSettings.WIDTH // 2,
                       GameSettings.HEIGHT // 2 - 70)
        self.draw_text(screen, str(score), 50, GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2)

        running = True
        quit_reason = BaseScreen.SCREEN_END_REASON_NORMAL
        while running:
            clock.tick(GameSettings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_reason = BaseScreen.SCREEN_END_REASON_QUIT
                    running = False
                if event.type == pygame.KEYUP:
                    quit_reason = BaseScreen.SCREEN_END_REASON_NORMAL
                    running = False
            pygame.display.flip()

        return {BaseScreen.SCREEN_END_REASON: quit_reason}
