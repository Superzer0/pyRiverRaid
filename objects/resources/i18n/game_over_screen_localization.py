from objects.resources.ConfigReader import ConfigReader


class GameOverLocalization(ConfigReader):
    def __init__(self, config, section_name):
        ConfigReader.__init__(self, config, section_name)

    @property
    def title_label(self):
        return self.get_config_property('game_over_summary_title')

    @property
    def score_label(self):
        return self.get_config_property('game_over_summary_score')

    @property
    def bonus_label(self):
        return self.get_config_property('game_over_bonus_label')

    @property
    def hits_label(self):
        return self.get_config_property('game_over_summary_hits')

    @property
    def power_ups_label(self):
        return self.get_config_property('game_over_summary_power_ups')

    @property
    def level_label(self):
        return self.get_config_property('game_over_summary_level')

    @property
    def name_enter_label(self):
        return self.get_config_property('game_over_enter_name')

    @property
    def continue_label(self):
        return self.get_config_property('game_over_continue')
