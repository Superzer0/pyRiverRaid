import configparser
import os
import unittest

from objects.resources.ConfigReader import ConfigReader


class ConfigParserTests(unittest.TestCase):
    def setUp(self):
        self.base_test_case_data = os.path.join(os.path.dirname(__file__), 'test_data')
        self.test_file_path = os.path.join(self.base_test_case_data, 'example_ini.ini')

    def test_read_from_default_section(self):
        config_reader = configparser.ConfigParser()
        config_reader.read(self.test_file_path)
        service = ConfigReader(config_reader)

        single_value = service.get_config_property('some_value')
        self.assertEquals('5', single_value)

        multi_value = service.get_config_property_value_list('list_of_values')
        self.assertEquals(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], multi_value)

    def test_read_from_custom_section(self):
        config_reader = configparser.ConfigParser()
        config_reader.read(self.test_file_path)
        service = ConfigReader(config_reader, 'OTHER')

        single_value = service.get_config_property('some_value')
        self.assertEquals('1', single_value)

        multi_value = service.get_config_property_value_list('list_of_values')
        self.assertEquals(['9', '8', '7', '6', '5', '4', '3', '2', '1', '0'], multi_value)

    def test_read_from_empty_section_section(self):
        config_reader = configparser.ConfigParser()
        config_reader.read(self.test_file_path)
        service = ConfigReader(config_reader, 'EMPTY_SECTION')

        single_value = service.get_config_property('some_value')
        self.assertEquals('5', single_value)

        multi_value = service.get_config_property_value_list('list_of_values')
        self.assertEquals(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], multi_value)

    def test_property_not_exist(self):
        config_reader = configparser.ConfigParser()
        config_reader.read(self.test_file_path)
        service = ConfigReader(config_reader)

        with self.assertRaises(KeyError):
            single_value = service.get_config_property('non_exisitng_property')
