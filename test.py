__author__ = 'alexandra'
import unittest
from formatter import *
from settings import *


class Test(unittest.TestCase):
    def setUp(self):
        self.formatter = Formatter()
        self.formatter.add_code("Tests/test.txt")
        self.settings = Settings()

    def test_OTBS(self):
        self.settings.set_1TBS()
        self.result = self.formatter.use_style(self.settings)
        self.otbs_file = open("Tests/otbs_test.txt")
        self.otbs_result = self.otbs_file.read()
        self.otbs_file.close()
        self.assertMultiLineEqual(self.result, self.otbs_result)

    def test_BSD(self):
        self.settings.set_BSD()
        self.result = self.formatter.use_style(self.settings)
        self.bsd_file = open("Tests/bsd_test.txt")
        self.bsd_result = self.bsd_file.read()
        self.bsd_file.close()
        self.assertMultiLineEqual(self.result, self.bsd_result)

    def test_WS(self):
        self.settings.set_WS()
        self.result = self.formatter.use_style(self.settings)
        self.ws_file = open("Tests/ws_test.txt")
        self.ws_result = self.ws_file.read()
        self.ws_file.close()
        self.assertMultiLineEqual(self.result, self.ws_result)

    def test_GNU(self):
        self.settings.set_GNU()
        self.result = self.formatter.use_style(self.settings)
        self.gnu_file = open("Tests/gnu_test.txt")
        self.gnu_result = self.gnu_file.read()
        self.gnu_file.close()
        self.assertMultiLineEqual(self.result, self.gnu_result)

    def test_blank_lines_near_class(self):
        self.settings.set_blank_lines_near_class(4)
        self.result = self.formatter.blank_lines_near_class(self.settings)
        self.class_file = open("Tests/lines_near_class_test.txt")
        self.class_result = self.class_file.read()
        self.class_file.close()
        self.assertMultiLineEqual(self.result, self.class_result)

    def test_blank_lines_near_method(self):
        self.settings.set_blank_lines_near_method(3)
        self.result = self.formatter.blank_lines_near_method(self.settings)
        self.method_file = open("Tests/lines_near_method_test.txt")
        self.method_result = self.method_file.read()
        self.method_file.close()
        self.assertMultiLineEqual(self.result, self.method_result)

    def test_blank_lines_near_for(self):
        self.settings.set_blank_lines_near_for(3)
        self.result = self.formatter.blank_lines_near_for(self.settings)
        self.for_file = open("Tests/lines_near_for_test.txt")
        self.for_result = self.for_file.read()
        self.for_file.close()
        self.assertMultiLineEqual(self.result, self.for_result)

    def test_blank_lines_near_while(self):
        self.settings.set_blank_lines_near_while(3)
        self.result = self.formatter.blank_lines_near_while(self.settings)
        self.while_file = open("Tests/lines_near_while_test.txt")
        self.while_result = self.while_file.read()
        self.while_file.close()
        self.assertMultiLineEqual(self.result, self.while_result)

    def test_catch_near_end_bracket(self):
        self.settings.set_move_catch_to_end_bracket(True)
        self.settings.set_number_of_spaces_before_catch(4)
        self.result = self.formatter.move_catch(self.settings)
        self.catch_file = open("Tests/move_catch_test.txt")
        self.catch_result = self.catch_file.read()
        self.catch_file.close()
        self.assertMultiLineEqual(self.result, self.catch_result)

    def test_finally_on_new_line(self):
        self.settings.set_move_finally_to_end_bracket(False)
        self.settings.set_number_of_spaces_before_finally(3)
        self.result = self.formatter.move_finally(self.settings)
        self.finally_file = open("Tests/move_finally_test.txt")
        self.finally_result = self.finally_file.read()
        self.finally_file.close()
        self.assertMultiLineEqual(self.result, self.finally_result)

    def test_while_near_end_bracket(self):
        self.settings.set_move_while_to_end_bracket(True)
        self.settings.set_number_of_spaces_before_while(2)
        self.result = self.formatter.move_while(self.settings)
        self.while_file = open("Tests/move_while_test.txt")
        self.while_result = self.while_file.read()
        self.while_file.close()
        self.assertMultiLineEqual(self.result, self.while_result)

    def test_if_on_new_line(self):
        self.settings.set_move_if_to_else(False)
        self.result = self.formatter.move_if(self.settings)
        self.if_file = open("Tests/move_if_test.txt")
        self.if_result = self.if_file.read()
        self.if_file.close()
        self.assertMultiLineEqual(self.result, self.if_result)

    def test_spaces_around_operators(self):
        self.settings.set_spaces_around_unary_operators(1)
        self.settings.set_spaces_around_binary_operators(3)
        self.result = self.formatter.spaces_around_operators(self.settings)
        self.operators_file = open("Tests/operators_test.txt")
        self.operators_result = self.operators_file.read()
        self.operators_file.close()
        self.assertMultiLineEqual(self.result, self.operators_result)

    def test_spaces_after_comma(self):
        self.settings.set_spaces_after_comma(2)
        self.result = self.formatter.spaces_after_comma(self.settings)
        self.comma_file = open("Tests/comma_test.txt")
        self.comma_result = self.comma_file.read()
        self.comma_file.close()
        self.assertMultiLineEqual(self.result, self.comma_result)

    def test_spaces_after_semicolon(self):
        self.settings.set_spaces_after_semicolon(2)
        self.result = self.formatter.spaces_after_semicolon(self.settings)
        self.semicolon_file = open("Tests/semicolon_test.txt")
        self.semicolon_result = self.semicolon_file.read()
        self.semicolon_file.close()
        self.assertMultiLineEqual(self.result, self.semicolon_result)

    def test_set_and_get_default_setting(self):
        self.settings.set_default_style()
        move_begin_bracket = self.settings.get_move_begin_bracket_to_operator()
        spaces_before_brackets = self.settings.get_number_of_spaces_before_brackets()
        spapes_before_bbracket = self.settings.get_number_of_spaces_before_begin_bracket()
        spaces_inside_block = self.settings.get_number_of_spaces_inside_block()
        self.assertEquals(move_begin_bracket, False)
        self.assertEquals(spaces_before_brackets, 0)
        self.assertEquals(spapes_before_bbracket, 0)
        self.assertEquals(spaces_inside_block, 0)

    def test_set_and_get_bsd_setting(self):
        self.settings.set_BSD()
        move_begin_bracket = self.settings.get_move_begin_bracket_to_operator()
        spaces_before_brackets = self.settings.get_number_of_spaces_before_brackets()
        spapes_before_bbracket = self.settings.get_number_of_spaces_before_begin_bracket()
        spaces_inside_block = self.settings.get_number_of_spaces_inside_block()
        self.assertEquals(move_begin_bracket, False)
        self.assertEquals(spaces_before_brackets, 0)
        self.assertEquals(spapes_before_bbracket, 1)
        self.assertEquals(spaces_inside_block, 4)

    def test_set_and_get_otbs_setting(self):
        self.settings.set_1TBS()
        move_begin_bracket = self.settings.get_move_begin_bracket_to_operator()
        spaces_before_brackets = self.settings.get_number_of_spaces_before_brackets()
        spapes_before_bbracket = self.settings.get_number_of_spaces_before_begin_bracket()
        spaces_inside_block = self.settings.get_number_of_spaces_inside_block()
        self.assertEquals(move_begin_bracket, True)
        self.assertEquals(spaces_before_brackets, 0)
        self.assertEquals(spapes_before_bbracket, 1)
        self.assertEquals(spaces_inside_block, 8)

    def test_set_and_get_ws_setting(self):
        self.settings.set_WS()
        move_begin_bracket = self.settings.get_move_begin_bracket_to_operator()
        spaces_before_brackets = self.settings.get_number_of_spaces_before_brackets()
        spapes_before_bbracket = self.settings.get_number_of_spaces_before_begin_bracket()
        spaces_inside_block = self.settings.get_number_of_spaces_inside_block()
        self.assertEquals(move_begin_bracket, False)
        self.assertEquals(spaces_before_brackets, 4)
        self.assertEquals(spapes_before_bbracket, 1)
        self.assertEquals(spaces_inside_block, 0)

    def test_set_and_get_gnu_setting(self):
        self.settings.set_GNU()
        move_begin_bracket = self.settings.get_move_begin_bracket_to_operator()
        spaces_before_brackets = self.settings.get_number_of_spaces_before_brackets()
        spapes_before_bbracket = self.settings.get_number_of_spaces_before_begin_bracket()
        spaces_inside_block = self.settings.get_number_of_spaces_inside_block()
        self.assertEquals(move_begin_bracket, False)
        self.assertEquals(spaces_before_brackets, 4)
        self.assertEquals(spapes_before_bbracket, 1)
        self.assertEquals(spaces_inside_block, 4)

    def test_set_and_get_move_else(self):
        self.settings.set_move_else_to_end_bracket(True)
        self.settings.set_number_of_spaces_before_else(4)
        move_else = self.settings.get_move_else_to_end_bracket()
        spaces = self.settings.get_number_of_spaces_before_else()
        self.assertEquals(move_else, True)
        self.assertEquals(spaces, 4)

    def test_set_and_get_move_catch(self):
        self.settings.set_move_catch_to_end_bracket(False)
        self.settings.set_number_of_spaces_before_catch(3)
        move_else = self.settings.get_move_catch_to_end_bracket()
        spaces = self.settings.get_number_of_spaces_before_catch()
        self.assertEquals(move_else, False)
        self.assertEquals(spaces, 3)

    def test_set_and_get_spaces_comma(self):
        self.settings.set_spaces_after_comma(2)
        spaces = self.settings.get_spaces_after_comma()
        self.assertEquals(spaces, 2)

    def test_set_and_get_spaces_semicolon(self):
        self.settings.set_spaces_after_semicolon(3)
        spaces = self.settings.get_spaces_after_semicolon()
        self.assertEquals(spaces, 3)


if __name__ == "__main__":
    unittest.main()
