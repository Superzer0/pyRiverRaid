import os
import unittest

from objects.leaderboards.leaderboard_entry import LeaderboardEntry
from objects.leaderboards.leaderboard_service import LeaderBoardService


class LeaderBoardServiceTests(unittest.TestCase):
    def setUp(self):
        self.base_test_case_data = os.path.join(os.path.dirname(__file__), 'test_data')
        self.test_file = os.path.join(self.base_test_case_data, 'empty.csv')
        self.expected_file = os.path.join(self.base_test_case_data, 'expected_file.csv')
        self.examplary_data_record = LeaderboardEntry({
            LeaderboardEntry.DATE: '2017-02-06 02:13:36.082461',
            LeaderboardEntry.PLAYER_NAME: 'anonymous player ',
            LeaderboardEntry.LEVEL: '5',
            LeaderboardEntry.POWER_UPS: '6',
            LeaderboardEntry.HITS: '10',
            LeaderboardEntry.SCORE: '20'})

    def tearDown(self):
        # empty file:
        open(self.test_file, 'w').close()

    def test_file_path_empty_value_error(self):
        with self.assertRaises(ValueError):
            LeaderBoardService('')

    def test_entries_only_added_file_not_saved(self):
        service = LeaderBoardService(self.test_file)

        service.add_entry(self.examplary_data_record)
        service.add_entry(self.examplary_data_record)
        service.add_entry(self.examplary_data_record)

        # in memory we have 3 entries
        self.assertEquals(len(service.leader_board), 3)

        # but file should be empty:
        self.assertTrue(os.stat(self.test_file).st_size == 0)

        service.persist_leader_board()

        # now should not be empty
        self.assertFalse(os.stat(self.test_file).st_size == 0)
        with open(self.expected_file, 'r') as expected_file:
            with open(self.test_file, 'r') as output_file:
                expected_content = expected_file.read()
                output_content = output_file.read()
                self.assertEquals(expected_content, output_content)

        # create new service to see if entries were persisted
        service = LeaderBoardService(self.test_file)
        service.load_leader_board()

        self.assertEquals(len(service.leader_board), 3)

    def test_entries_read_happy_path(self):
        service = LeaderBoardService(self.expected_file)
        service.load_leader_board()

        for entry in service.leader_board:
            self.assertEquals(self.examplary_data_record.row, entry.row)

    def test_file_not_found_empty_list_returned(self):
        service = LeaderBoardService(self.expected_file + 'non existing')
        service.load_leader_board()
        self.assertEquals([], service.leader_board)


if __name__ == '__main__':
    unittest.main()
