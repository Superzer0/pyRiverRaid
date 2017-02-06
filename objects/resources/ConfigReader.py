from os import path


class ConfigReader:
    """Base class for configuration reading. Uses standard python configReader."""
    __CONFIG_LIST_SEPARATOR = ','
    DEFAULT_SECTION = "DEFAULT"

    def __init__(self, config, section_name=None, strip_properties=False):
        """Initializes instalce of Config Reader that wraps python configReader
        If no section_name is provided then default section is used
        """
        self.__config = config
        self.__section_name = section_name
        self.__strip_properties = strip_properties
        if not self.__section_name:
            self.__section_name = ConfigReader.DEFAULT_SECTION

    def get_config_property(self, property_name):
        """Gets property from underlying configReader.

        Performs stripping if needed
        :param property_name: property name in *.ini file
        :return: string with value for the property
        """
        return self.__strip_property(self.__config[self.__section_name][property_name])

    def get_config_property_value_list(self, property_name):
        """Gets list for the given property_name.

        :param property_name: property name in *.ini file
        :return: Stripped list of values separated by __CONFIG_LIST_SEPARATOR
        """
        value = self.get_config_property(property_name)
        if not value:
            raise IndexError('Error when reading configuration file')
        return [self.__strip_property(x) for x in value.split(ConfigReader.__CONFIG_LIST_SEPARATOR)]

    def __strip_property(self, txt):
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
