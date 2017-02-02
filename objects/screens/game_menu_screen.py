import logging

import pygame

from objects.globals.gamesettings import GameSettings
from objects.screens.base_screen import BaseScreen


class GameMenuScreen(BaseScreen):
    def __init__(self, resourceContext, localizationContext):
        BaseScreen.__init__(self, resourceContext)
        self.__logger = logging.getLogger(GameMenuScreen.__module__)
        self.__resourceContext = resourceContext
        self.__localizationContext = localizationContext

    def run(self, clock, screen, args=None):
        screen.blit(self.__resourceContext.imgResources.background,
                    self.__resourceContext.imgResources.background.get_rect())
        self.draw_text(screen, self.__localizationContext.initial_screen.title_label, 64, GameSettings.WIDTH / 2,
                       GameSettings.HEIGHT / 4)
        self.draw_text(screen, self.__localizationContext.initial_screen.instructions_1_label, 22,
                       GameSettings.WIDTH / 2, GameSettings.HEIGHT / 2)
        self.draw_text(screen, self.__localizationContext.initial_screen.instructions_2_label, 18,
                       GameSettings.WIDTH / 2,
                       GameSettings.HEIGHT * 3 / 4)
        pygame.display.flip()
        running = True
        quit_reason = BaseScreen.SCREEN_END_REASON_NORMAL
        while running:
            clock.tick(GameSettings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_reason = BaseScreen.SCREEN_END_REASON_QUIT
                    running = False
                if event.type == pygame.KEYUP:
                    running = False

        return {BaseScreen.SCREEN_END_REASON: quit_reason}
