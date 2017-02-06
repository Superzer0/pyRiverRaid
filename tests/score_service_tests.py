import unittest

from objects.leaderboards.leaderboard_entry import LeaderboardEntry
from objects.leaderboards.score_service import ScoreService


class ScoreServiceTests(unittest.TestCase):
    def test_score_count_happy_path(self):
        row = {LeaderboardEntry.LEVEL: 1,
               LeaderboardEntry.POWER_UPS: 1,
               LeaderboardEntry.HITS: 18,
               LeaderboardEntry.SCORE: 200}

        leader_board_entry = LeaderboardEntry(row)
        bonus = ScoreService.count_bonus(leader_board_entry)
        final_score = ScoreService.count_final_score(leader_board_entry, bonus)
        self.assertEqual(bonus, 9)
        self.assertEqual(final_score, 209)

    def test_score_count_edge_values(self):
        row = {LeaderboardEntry.LEVEL: 1,
               LeaderboardEntry.POWER_UPS: 0,
               LeaderboardEntry.HITS: 0,
               LeaderboardEntry.SCORE: 0}

        leader_board_entry = LeaderboardEntry(row)
        bonus = ScoreService.count_bonus(leader_board_entry)
        final_score = ScoreService.count_final_score(leader_board_entry, bonus)
        self.assertEqual(bonus, 0)
        self.assertEqual(final_score, 0)

    def test_score_count_invalid_score_values(self):
        row = {LeaderboardEntry.LEVEL: -20,
               LeaderboardEntry.POWER_UPS: 8,
               LeaderboardEntry.HITS: 5,
               LeaderboardEntry.SCORE: -50}

        leader_board_entry = LeaderboardEntry(row)
        bonus = ScoreService.count_bonus(leader_board_entry)
        final_score = ScoreService.count_final_score(leader_board_entry, bonus)
        self.assertEqual(bonus, 0)
        self.assertEqual(final_score, 0)

    def test_score_count_empty_score_values(self):
        row = {'some': 'value'}
        leader_board_entry = LeaderboardEntry(row)
        bonus = ScoreService.count_bonus(leader_board_entry)
        final_score = ScoreService.count_final_score(leader_board_entry, bonus)
        self.assertEqual(bonus, 0)
        self.assertEqual(final_score, 0)

    def test_invalid_data_exception(self):
        row = None
        with self.assertRaises(TypeError):
            leader_board_entry = LeaderboardEntry(row)
            ScoreService.count_bonus(leader_board_entry)


if __name__ == '__main__':
    unittest.main()
