class ScoreService:
    @staticmethod
    def count_final_score(entry, bonus):
        return entry.score + bonus

    @staticmethod
    def count_bonus(entry):
        bonus = 0
        bonus += int(entry.level * entry.hits * 0.5)
        bonus += int(entry.level * entry.power_ups * 0.5)
        return bonus
