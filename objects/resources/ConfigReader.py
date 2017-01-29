from os import path


class ConfigReader:
    __CONFIG_LIST_SEPARATOR = ','
    __DEFAULT_SECTION = "DEFAULT"
    __RESOURCES_FOLDER = "resourcesFolderName"

    def __init__(self, game_folder, config, section_name):
        self.__config = config
        self.__section_name = section_name
        self.__game_folder = path.join(game_folder,
                                       config[ConfigReader.__DEFAULT_SECTION][ConfigReader.__RESOURCES_FOLDER])

    @property
    def resources_folder(self):
        return self.__game_folder

    def get_config_property(self, property_name):
        return self.__config[self.__section_name][property_name].strip()

    def get_config_property_value_list(self, property_name):
        value = self.get_config_property(property_name)
        if not value:
            raise IndexError('Error when reading configuration file')
        return [x.strip() for x in value.split(ConfigReader.__CONFIG_LIST_SEPARATOR)]
