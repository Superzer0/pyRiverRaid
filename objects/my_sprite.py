import abc


class MySprite:
    def __init__(self):
        self._speedy = None
        self._origin_speedy = None

    @abc.abstractmethod
    def speedUp(self):
        pass

    @abc.abstractmethod
    def slowDown(self):
        pass
