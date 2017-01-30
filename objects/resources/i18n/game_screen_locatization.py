from objects.resources.ConfigReader import ConfigReader


class GameScreenLocalization(ConfigReader):
    def __init__(self, config, section_name):
        ConfigReader.__init__(self, config, section_name)

    @property
    def fuel_label(self):
        return self.get_config_property('play_screen_fuel')

    @property
    def shield_label(self):
        return self.get_config_property('play_screen_shield')
