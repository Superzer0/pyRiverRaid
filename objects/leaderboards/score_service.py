class ScoreService:
    @staticmethod
    def count_final_score(entry, bonus):
        """Counts user final score based on base score and bonus

        :param entry: LeaderboardEntry
        :param bonus: int
        :return: int
        """
        final_score = entry.score + bonus
        return final_score if final_score >= 0 else 0

    @staticmethod
    def count_bonus(entry):
        """Counts user bonus based on custom rules"""
        bonus = 0
        bonus += int(entry.level * entry.hits * 0.5)
        bonus += int(entry.level * entry.power_ups * 0.5)
        return bonus if bonus >= 0 else 0
