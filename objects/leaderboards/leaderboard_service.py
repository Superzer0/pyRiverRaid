import csv
import logging
from collections import OrderedDict

from objects.leaderboards.leaderboard_entry import LeaderboardEntry


class LeaderBoardService:
    CSV_HEADER = [LeaderboardEntry.DATE, LeaderboardEntry.PLAYER_NAME, LeaderboardEntry.HITS,
                  LeaderboardEntry.POWER_UPS, LeaderboardEntry.SCORE, LeaderboardEntry.LEVEL]

    def __init__(self, file_path):
        if not file_path:
            raise ValueError('file_path cannot be empty')
        self.__file_path = file_path
        self.__logger = logging.getLogger(LeaderBoardService.__module__)
        self.__loaded_leader_board = []

    def load_leader_board(self):
        try:
            with open(self.__file_path, newline='') as csv_file:
                board_reader = csv.DictReader(csv_file)
                self.__loaded_leader_board = [row for row in board_reader]
        except IOError:
            self.__logger.exception('problems with reading leaderboard file.')

    @property
    def leader_board(self):
        return sorted([LeaderboardEntry(row) for row in self.__loaded_leader_board], key=lambda x: x.score,
                      reverse=True)

    def add_entry(self, entry):
        ordered_dict = OrderedDict(entry.row.items())
        self.__loaded_leader_board.append(ordered_dict)

    def persist_leader_board(self):
        if self.__loaded_leader_board and len(self.__loaded_leader_board):
            with open(self.__file_path, mode='w', newline='') as csv_file:
                dict_writer = csv.DictWriter(csv_file, fieldnames=LeaderBoardService.CSV_HEADER, extrasaction='ignore')

                dict_writer.writeheader()
                dict_writer.writerows(self.__loaded_leader_board)
