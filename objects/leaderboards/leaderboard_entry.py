import datetime


class LeaderboardEntry:
    """Used to group information about user score and stats during the game

    Internally simple dictionary is used. Each field is dictionary based.
    """
    SCORE = "SCORE"
    HITS = "HITS"
    POWER_UPS = "POWER_UPS"
    LEVEL = "LEVEL"
    PLAYER_NAME = "PLAYER_NAME"
    DATE = "DATE"

    def __init__(self, row):
        """Initializes LeaderboardEntry with dictionary.

        :param row: data row, dictionary like. If row is empty or None TypeError is raised
        """
        if not row:
            raise TypeError('Value should be dictionary like, non empty object.')
        self.__row = row

    @property
    def row(self):
        """Data row

        :return: Underlying dictionary
        """
        return self.__row

    @property
    def score(self):
        """User score

        :return: data dictionary score entry
        """
        return int(self.__row.get(LeaderboardEntry.SCORE, 0))

    @score.setter
    def score(self, value):
        """Sets value for player score

        :param value: score
        :return: None
        """
        self.__row[LeaderboardEntry.SCORE] = value

    @property
    def hits(self):
        """User hits

        :return: data dictionary hit entry int
        """
        return int(self.__row.get(LeaderboardEntry.HITS, 0))

    @property
    def power_ups(self):
        """User collected power ups

        :return: data dictionary power ups entry int
        """
        return int(self.__row.get(LeaderboardEntry.POWER_UPS, 0))

    @property
    def level(self):
        """Level that user reached

        :return: data dictionary level entry int
        """
        return int(self.__row.get(LeaderboardEntry.LEVEL, 1))

    @property
    def player_name(self):
        """User player name

        :return: data dictionary player name entry
        """
        return self.__row.get(LeaderboardEntry.PLAYER_NAME, '')

    @player_name.setter
    def player_name(self, value):
        """Sets value for player name

        :param value: player name
        :return: None
        """
        self.__row[LeaderboardEntry.PLAYER_NAME] = value

    @property
    def date(self):
        """Value for user play time

        :return: Datetime
        """
        return self.__row.get(LeaderboardEntry.DATE, datetime.datetime.min)
