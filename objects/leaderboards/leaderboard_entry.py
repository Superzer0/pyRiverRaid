import datetime


class LeaderboardEntry:
    SCORE = "SCORE"
    HITS = "HITS"
    POWER_UPS = "POWER_UPS"
    LEVEL = "LEVEL"
    PLAYER_NAME = "PLAYER_NAME"
    DATE = "DATE"

    def __init__(self, row):
        if not row:
            raise TypeError('Value should be dictionary like, non empty object.')
        self.__row = row

    @property
    def row(self):
        return self.__row

    @property
    def score(self):
        return int(self.__row.get(LeaderboardEntry.SCORE, 0))

    @score.setter
    def score(self, value):
        self.__row[LeaderboardEntry.SCORE] = value

    @property
    def hits(self):
        return int(self.__row.get(LeaderboardEntry.HITS, 0))

    @property
    def power_ups(self):
        return int(self.__row.get(LeaderboardEntry.POWER_UPS, 0))

    @property
    def level(self):
        return int(self.__row.get(LeaderboardEntry.LEVEL, 1))

    @property
    def player_name(self):
        return self.__row.get(LeaderboardEntry.PLAYER_NAME, '')

    @player_name.setter
    def player_name(self, value):
        self.__row[LeaderboardEntry.PLAYER_NAME] = value

    @property
    def date(self):
        return self.__row.get(LeaderboardEntry.DATE, datetime.datetime.min)
