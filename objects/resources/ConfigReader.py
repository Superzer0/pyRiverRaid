from os import path


class ConfigReader:
    __CONFIG_LIST_SEPARATOR = ','
    DEFAULT_SECTION = "DEFAULT"

    def __init__(self, config, section_name, strip_properties=False):
        self.__config = config
        self.__section_name = section_name
        self.__strip_properties = strip_properties
        if not self.__section_name:
            self.__section_name = ConfigReader.DEFAULT_SECTION

    def get_config_property(self, property_name):
        return self.strip_property(self.__config[self.__section_name][property_name])

    def get_config_property_value_list(self, property_name):
        value = self.get_config_property(property_name)
        if not value:
            raise IndexError('Error when reading configuration file')
        return [self.strip_property(x) for x in value.split(ConfigReader.__CONFIG_LIST_SEPARATOR)]

    def strip_property(self, txt):
        return txt.strip() if self.__strip_properties else txt


class ResourcesReader(ConfigReader):
    __RESOURCES_FOLDER = "resourcesFolderName"

    def __init__(self, game_folder, config, section_name):
        ConfigReader.__init__(self, config, section_name, True)
        self.__game_folder = path.join(game_folder,
                                       config[ConfigReader.DEFAULT_SECTION][ResourcesReader.__RESOURCES_FOLDER])

    @property
    def resources_folder(self):
        return self.__game_folder
