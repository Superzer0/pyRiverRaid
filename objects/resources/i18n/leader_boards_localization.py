from objects.resources.ConfigReader import ConfigReader


class LeaderBoardLocalization(ConfigReader):
    def __init__(self, config, section_name):
        ConfigReader.__init__(self, config, section_name)

    @property
    def title_label(self):
        return self.get_config_property('leaderboards_title')

    @property
    def header_player_label(self):
        return self.get_config_property('leaderboards_header_player')

    @property
    def header_lvl_label(self):
        return self.get_config_property('leaderboards_header_lvl')

    @property
    def header_power_label(self):
        return self.get_config_property('leaderboards_header_power_ups')

    @property
    def header_hits_label(self):
        return self.get_config_property('leaderboards_header_hits')

    @property
    def header_score_label(self):
        return self.get_config_property('leaderboards_header_score')

    @property
    def next_label(self):
        return self.get_config_property('leaderboards_next_page')

    @property
    def prev_label(self):
        return self.get_config_property('leaderboards_prev_page')

    @property
    def exit_label(self):
        return self.get_config_property('leaderboards_exit')
