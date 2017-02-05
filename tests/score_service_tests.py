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


if __name__ == '__main__':
    unittest.main()
