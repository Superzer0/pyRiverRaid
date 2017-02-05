import logging

import pygame

from objects.globals.gamecolors import GameColors
from objects.globals.gamesettings import GameSettings
from objects.leaderboards.leaderboard_entry import LeaderboardEntry
from objects.leaderboards.score_service import ScoreService
from objects.screens.base_screen import BaseScreen
from objects.screens.game_screens import GameScreens
from other.py_text_input import TextInput


class GameOverScreen(BaseScreen):
    def __init__(self, resourceContext, localizationContext, leaderBoardService):
        BaseScreen.__init__(self, resourceContext)
        self.__leaderBoardService = leaderBoardService
        self.__logger = logging.getLogger(GameOverScreen.__module__)
        self.__resourceContext = resourceContext
        self.__localizationContext = localizationContext

    def run(self, clock, screen, args=None):

        entry = LeaderboardEntry(args)
        bonus = ScoreService.count_bonus(entry)
        entry.score = ScoreService.count_final_score(entry, bonus)

        self.__leaderBoardService.load_leader_board()
        text_input = TextInput(font_size=25, antialias=True, text_color=GameColors.WHITE)

        running = True
        next_screen = GameScreens.LEADER_BOARD_SCREEN
        user_entered_nick = ''
        while running:
            clock.tick(GameSettings.FPS)
            events = pygame.event.get()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_screen = GameScreens.QUIT_GAME
                    running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        running = False

            user_accepted_text = text_input.update(events)

            screen.fill(GameColors.BLACK)
            screen.blit(self.__resourceContext.imgResources.background,
                        self.__resourceContext.imgResources.background.get_rect())

            self.draw_text(screen, self.__localizationContext.game_over_screen.title_label, 50,
                           GameSettings.WIDTH // 2,
                           GameSettings.HEIGHT // 2 - 300)

            self.draw_text(screen, self.__localizationContext.game_over_screen.score_label + str(entry.score), 50,
                           GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2 - 200)

            self.draw_text(screen, self.__localizationContext.game_over_screen.bonus_label + str(bonus),
                           18,
                           GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2 - 150)

            self.draw_text(screen, self.__localizationContext.game_over_screen.level_label + str(entry.level), 25,
                           GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2 - 100)

            self.draw_text(screen, self.__localizationContext.game_over_screen.hits_label + str(entry.hits), 25,
                           GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2 - 50)

            self.draw_text(screen, self.__localizationContext.game_over_screen.power_ups_label + str(entry.power_ups),
                           25,
                           GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2)

            self.draw_text(screen, self.__localizationContext.game_over_screen.name_enter_label,
                           25,
                           GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2 + 100)

            screen.blit(text_input.get_surface(), (GameSettings.WIDTH // 2 - 50, GameSettings.HEIGHT // 2 + 150))

            if len(user_entered_nick) > 0:
                self.draw_text(screen, self.__localizationContext.game_over_screen.continue_label,
                               25,
                               GameSettings.WIDTH // 2, GameSettings.HEIGHT // 2 + 200)

            pygame.display.flip()
            user_entered_nick = text_input.get_text()
            if user_accepted_text and len(user_entered_nick) > 0:
                running = False

        entry.player_name = user_entered_nick
        self.__leaderBoardService.add_entry(entry)
        self.__leaderBoardService.persist_leader_board()

        return {BaseScreen.SCREEN_NEXT: next_screen, "entry": entry}
