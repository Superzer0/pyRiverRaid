import abc

from objects.globals.gamecolors import GameColors


class BaseScreen(object, metaclass=abc.ABCMeta):
    SCREEN_END_REASON = "SCREEN_END_REASON"
    SCREEN_NEXT = "SCREEN_NEXT"
    SCREEN_END_REASON_QUIT = "QUIT_GAME"
    SCREEN_END_REASON_NORMAL = "REASON_NORMAL"

    def __init__(self, resourceContext):
        self.__resourceContext = resourceContext

    @abc.abstractmethod
    def run(self, clock, screen, args=None):
        raise NotImplementedError('users must define run to use this base class')

    def draw_text(self, surf, text, size, x, y, color=GameColors.WHITE, centered=True):
        font = self.__resourceContext.miscResources.get_font(size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if centered:
            text_rect.midtop = (x, y)
        else:
            text_rect.x = x
            text_rect.y = y

        surf.blit(text_surface, text_rect)

    @staticmethod
    def screen_finished_normally(screen_result):
        return not screen_result[BaseScreen.SCREEN_END_REASON] == BaseScreen.SCREEN_END_REASON_QUIT
