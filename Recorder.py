# -*- coding: utf-8 -*-

__author__ = 'Ricky Chen'

import ConfigParser

_file_name = 'data.txt'
_data_name_total = 'total'
_data_name_happened = 'happened'


class Recorder():
    def __init__(self):
        self.parser = ConfigParser.RawConfigParser()
        self.parser.read(_file_name)

        # Set first section as default
        self.load_first_section_without_saving()

    def __del__(self):
        self.__save_current_section_to_file()

    def get_sections(self):
        return self.parser.sections()

    def record_happened(self):
        self.current_total += 1
        self.current_happened += 1

    def record_not_happened(self):
        self.current_total += 1

    def add_section(self, section_name):
        if not self.parser.has_section(section_name):
            self.parser.add_section(section_name)
            self.__set_config_data(section_name, 0, 0)

        self.change_section(section_name)

    def change_section(self, next_section):
        if self.current_section != next_section:
            self.__save_current_section_to_file()
            self.current_section = next_section
            self.current_total = self.parser.getint(next_section, _data_name_total)
            self.current_happened = self.parser.getint(next_section, _data_name_happened)

    def load_first_section_without_saving(self):
        section = self.parser.sections()[0]
        self.current_section = section
        self.current_total = self.parser.getint(section, _data_name_total)
        self.current_happened = self.parser.getint(section, _data_name_happened)

    # Can be remove when there are other sections
    def remove_section(self, section_name):
        is_removable = False
        if section_name == self.current_section:
            for each_section in self.parser.sections():
                if each_section != section_name:
                    self.change_section(each_section)
                    is_removable = True
                    break
        if is_removable:
            self.parser.remove_section(section_name)
            self.load_first_section_without_saving()

    def __save_current_section_to_file(self):
        self.__set_config_data()
        with open(_file_name, 'wb') as data_file:
            self.parser.write(data_file)

    def __set_config_data(self, section=None, total=None, happened=None):
        if section is None:
            section = self.current_section
        if total is None:
            total = self.current_total
        if happened is None:
            happened = self.current_happened

        self.parser.set(section, _data_name_total, total)
        self.parser.set(section, _data_name_happened, happened)
