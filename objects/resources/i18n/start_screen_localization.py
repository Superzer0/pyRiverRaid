from objects.resources.ConfigReader import ConfigReader


class StartScreenLocalization(ConfigReader):
    def __init__(self, config, section_name):
        ConfigReader.__init__(self, config, section_name)

    @property
    def title_label(self):
        return self.get_config_property('initial_screen_title')

    @property
    def instructions_1_label(self):
        return self.get_config_property('initial_screen_instruction_1')

    @property
    def instructions_2_label(self):
        return self.get_config_property('initial_screen_instruction_2')

    @property
    def game_over_label(self):
        return self.get_config_property('initial_screen_game_over')
