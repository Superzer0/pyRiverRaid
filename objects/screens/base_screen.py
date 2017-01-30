from objects.globals.gamecolors import GameColors


class BaseScreen:
    SCREEN_END_REASON = "SCREEN_END_REASON"
    SCREEN_END_REASON_QUIT = "QUIT_GAME"
    SCREEN_END_REASON_NORMAL = "REASON_NORMAL"

    def __init__(self, resourceContext):
        self.__resourceContext = resourceContext

    def draw_text(self, surf, text, size, x, y):
        font = self.__resourceContext.miscResources.get_font(size)
        text_surface = font.render(text, True, GameColors.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    @staticmethod
    def screen_finished_normally(screen_result):
        return not screen_result[BaseScreen.SCREEN_END_REASON] == BaseScreen.SCREEN_END_REASON_QUIT
