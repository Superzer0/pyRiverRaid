import logging

import pygame

from objects.globals.gamesettings import GameSettings
from objects.leaderboards.leaderboard_entry import LeaderboardEntry
from objects.screens.base_screen import BaseScreen


class GameOverScreen(BaseScreen):
    def __init__(self, resourceContext, localizationContext, leaderBoardService):
        BaseScreen.__init__(self, resourceContext)
        self.__leaderBoardService = leaderBoardService
        self.__logger = logging.getLogger(GameOverScreen.__module__)
        self.__resourceContext = resourceContext
        self.__localizationContext = localizationContext

    def run(self, clock, screen, args=None):

        entry = LeaderboardEntry(args)
        entry.score = self.count_final_score(entry)

        self.__leaderBoardService.load_leader_board()
        self.__leaderBoardService.add_entry(entry)
        self.__leaderBoardService.persist_leader_board()

        screen.blit(self.__resourceContext.imgResources.background,
                    self.__resourceContext.imgResources.background.get_rect())

        self.draw_text(screen, self.__localizationContext.game_over_screen.title_label, 50,
                       GameSettings.WIDTH // 2,
                       GameSettings.HEIGHT // 2 - 70)

        self.draw_text(screen, self.__localizationContext.game_over_screen.score_label + str(entry.score), 50,
                       GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2)

        self.draw_text(screen, self.__localizationContext.game_over_screen.level_label + str(entry.level), 25,
                       GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2 + 100)

        self.draw_text(screen, self.__localizationContext.game_over_screen.hits_label + str(entry.hits), 25,
                       GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2 + 150)

        self.draw_text(screen, self.__localizationContext.game_over_screen.power_ups_label + str(entry.power_ups), 25,
                       GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2 + 200)

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

    @staticmethod
    def count_final_score(entry):
        score = entry.score
        score += int(entry.level * entry.hits * 0.5)
        score += int(entry.level * entry.power_ups * 0.5)
        return score
