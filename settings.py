__author__ = 'alexandra'
import configparser


class Settings:
    def __init__(self):
        self.setting_reader = configparser.ConfigParser()
        self.setting_writer = configparser.ConfigParser()
        self.setting_reader.read("built_in_style_settings.txt")
        self.setting_reader.read("default settings.txt")
        self.setting_writer['Other_settings'] = self.setting_reader['Other_settings']
        self.setting_writer['Current_style'] = self.setting_reader['Default_current_style']

    def set_default_style(self):
        self.setting_writer['Current_style'] = self.setting_reader['Default_current_style']
        self.write_to_configfile()

    def set_BSD(self):
        self.setting_writer['Current_style'] = self.setting_reader['BSD']
        self.write_to_configfile()

    def set_GNU(self):
        self.setting_writer['Current_style'] = self.setting_reader['GNU']
        self.write_to_configfile()

    def set_1TBS(self):
        self.setting_writer['Current_style'] = self.setting_reader['1TBS']
        self.write_to_configfile()

    def set_WS(self):
        self.setting_writer['Current_style'] = self.setting_reader['WS']
        self.write_to_configfile()

    def set_move_begin_bracket_to_operator(self, move_bbracket):
        self.setting_writer['Current_style']['move_begin_bracket_to_operator'] = \
            str(int(move_bbracket))
        self.write_to_configfile()

    def set_number_of_spaces_before_brackets(self, number_of_spaces):
        self.setting_writer['Current_style']['number_of_spaces_before_brackets'] = \
            str(number_of_spaces)
        self.write_to_configfile()

    def set_number_of_spaces_before_begin_bracket(self, number_of_spaces):
        self.setting_writer['Current_style']['number_of_spaces_before_begin_bracket'] = \
            str(number_of_spaces)
        self.write_to_configfile()

    def set_number_of_spaces_inside_block(self, number_of_spaces):
        self.setting_writer['Current_style']['number_of_spaces_inside_block'] = \
            str(number_of_spaces)
        self.write_to_configfile()

    def set_move_else_to_end_bracket(self, move_else):
        self.setting_writer['Other_settings']['move_else_to_end_bracket'] = str(int(move_else))
        self.write_to_configfile()

    def set_number_of_spaces_before_else(self, number_of_spaces):
        self.setting_writer['Other_settings']['number_of_spaces_before_else'] = \
            str(number_of_spaces)
        self.write_to_configfile()

    def set_move_catch_to_end_bracket(self, move_catch):
        self.setting_writer['Other_settings']['move_catch_to_end_bracket'] = str(int(move_catch))
        self.write_to_configfile()

    def set_number_of_spaces_before_catch(self, number_of_spaces):
        self.setting_writer['Other_settings']['number_of_spaces_before_catch'] = \
            str(number_of_spaces)
        self.write_to_configfile()

    def set_move_finally_to_end_bracket(self, move_finally):
        self.setting_writer['Other_settings']['move_finally_to_end_bracket'] = \
            str(int(move_finally))
        self.write_to_configfile()

    def set_number_of_spaces_before_finally(self, number_of_spaces):
        self.setting_writer['Other_settings']['number_of_spaces_before_finally'] = \
            str(number_of_spaces)
        self.write_to_configfile()

    def set_move_while_to_end_bracket(self, move_while):
        self.setting_writer['Other_settings']['move_while_to_end_bracket'] = str(int(move_while))
        self.write_to_configfile()

    def set_number_of_spaces_before_while(self, number_of_spaces):
        self.setting_writer['Other_settings']['number_of_spaces_before_while'] = \
            str(number_of_spaces)
        self.write_to_configfile()

    def set_move_if_to_else(self, move_if):
        self.setting_writer['Other_settings']['move_if_to_else'] = str(int(move_if))
        self.write_to_configfile()

    def set_number_of_spaces_before_if(self, number_of_spaces):
        self.setting_writer['Other_settings']['number_of_spaces_before_if'] = str(number_of_spaces)
        self.write_to_configfile()

    def set_spaces_after_comma(self, number_of_spaces):
        self.setting_writer['Other_settings']['spaces_after_comma'] = str(number_of_spaces)
        self.write_to_configfile()

    def set_spaces_around_unary_operators(self, number_of_spaces):
        self.setting_writer['Other_settings']['spaces_around_unary_operators'] = \
            str(number_of_spaces)
        self.write_to_configfile()

    def set_spaces_around_binary_operators(self, number_of_spaces):
        self.setting_writer['Other_settings']['spaces_around_binary_operators'] = \
            str(number_of_spaces)
        self.write_to_configfile()

    def set_spaces_after_semicolon(self, number_of_spaces):
        self.setting_writer['Other_settings']['spaces_after_semicolon'] = str(number_of_spaces)
        self.write_to_configfile()

    def set_blank_lines_near_class(self, number_of_spaces):
        self.setting_writer['Other_settings']['blank_lines_near_class'] = str(number_of_spaces)
        self.write_to_configfile()

    def set_blank_lines_near_interface(self, number_of_spaces):
        self.setting_writer['Other_settings']['blank_lines_near_interface'] = str(number_of_spaces)
        self.write_to_configfile()

    def set_blank_lines_near_method(self, number_of_spaces):
        self.setting_writer['Other_settings']['blank_lines_near_method'] = str(number_of_spaces)
        self.write_to_configfile()

    def set_blank_lines_near_while(self, number_of_spaces):
        self.setting_writer['Other_settings']['blank_lines_near_while'] = str(number_of_spaces)
        self.write_to_configfile()

    def set_blank_lines_near_for(self, number_of_spaces):
        self.setting_writer['Other_settings']['blank_lines_near_for'] = str(number_of_spaces)
        self.write_to_configfile()

    def set_blank_lines_near_switch(self, number_of_spaces):
        self.setting_writer['Other_settings']['blank_lines_near_switch'] = str(number_of_spaces)
        self.write_to_configfile()

    def get_move_begin_bracket_to_operator(self):
        self.setting_reader.read("current_settings.txt")
        return bool(int(self.setting_reader['Current_style']['move_begin_bracket_to_operator']))

    def get_number_of_spaces_before_brackets(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Current_style']['number_of_spaces_before_brackets'])

    def get_number_of_spaces_before_begin_bracket(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Current_style']['number_of_spaces_before_begin_bracket'])

    def get_number_of_spaces_inside_block(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Current_style']['number_of_spaces_inside_block'])

    def get_move_else_to_end_bracket(self):
        self.setting_reader.read("current_settings.txt")
        return bool(int(self.setting_reader['Other_settings']['move_else_to_end_bracket']))

    def get_number_of_spaces_before_else(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['number_of_spaces_before_else'])

    def get_move_catch_to_end_bracket(self):
        self.setting_reader.read("current_settings.txt")
        return bool(int(self.setting_reader['Other_settings']['move_catch_to_end_bracket']))

    def get_number_of_spaces_before_catch(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['number_of_spaces_before_catch'])

    def get_move_finally_to_end_bracket(self):
        self.setting_reader.read("current_settings.txt")
        return bool(int(self.setting_reader['Other_settings']['move_finally_to_end_bracket']))

    def get_number_of_spaces_before_finally(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['number_of_spaces_before_finally'])

    def get_move_while_to_end_bracket(self):
        self.setting_reader.read("current_settings.txt")
        return bool(int(self.setting_reader['Other_settings']['move_while_to_end_bracket']))

    def get_number_of_spaces_before_while(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['number_of_spaces_before_while'])

    def get_move_if_to_else(self):
        self.setting_reader.read("current_settings.txt")
        return bool(int(self.setting_reader['Other_settings']['move_if_to_else']))

    def get_number_of_spaces_before_if(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['number_of_spaces_before_if'])

    def get_spaces_after_comma(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['spaces_after_comma'])

    def get_spaces_around_unary_operators(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['spaces_around_unary_operators'])

    def get_spaces_around_binary_operators(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['spaces_around_binary_operators'])

    def get_spaces_after_semicolon(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['spaces_after_semicolon'])

    def get_blank_lines_near_class(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['blank_lines_near_class'])

    def get_blank_lines_near_interface(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['blank_lines_near_interface'])

    def get_blank_lines_near_method(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['blank_lines_near_method'])

    def get_blank_lines_near_while(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['blank_lines_near_while'])

    def get_blank_lines_near_for(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['blank_lines_near_for'])

    def get_blank_lines_near_switch(self):
        self.setting_reader.read("current_settings.txt")
        return int(self.setting_reader['Other_settings']['blank_lines_near_switch'])

    def write_to_configfile(self):
        with open("current_settings.txt", "w") as configfile:
            self.setting_writer.write(configfile)