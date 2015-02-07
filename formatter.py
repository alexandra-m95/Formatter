__author__ = 'Alexandra'
import re
from settings import *


class Formatter:
    def __init__(self):
        """
        Инициализация переменной, содержащей код,
        установка связей для ключевых слов else, catch, finally, while, if(
        какие методы класса Settings необходимо вызывать для получения параметров
        перемещения для соотвествующего ключевого слова, а также то, к чему
        необходимо из перемещать.) Все это сохраняется в переменной self.communications_for_keywords
        в виде словаря, где ключ - это ключевое слово, а значение - кортеж из трех элеметов:
        две ф-ии класса Settings и то, к чему перемещается ключевое слово.
        Аналогично инициализируется переменная self.communications_for_keyblocks, где
        ключ - ключевой блок, значение - кортеж из двух элеметов: регулярное выражение,
        необходимое для поиска данного ключевого блока и метод класса Settings, возвращающий
        количество пустых строк для данного ключевого блока.
        """
        self.java_code = ""
        movable_words = ["else", "catch", "finally", "while", "if"]
        movement = [Settings.get_move_else_to_end_bracket, Settings.get_move_catch_to_end_bracket,
                    Settings.get_move_finally_to_end_bracket,
                    Settings.get_move_while_to_end_bracket,
                    Settings.get_move_if_to_else]
        number_of_spaces = [Settings.get_number_of_spaces_before_else,
                            Settings.get_number_of_spaces_before_catch,
                            Settings.get_number_of_spaces_before_finally,
                            Settings.get_number_of_spaces_before_while,
                            Settings.get_number_of_spaces_before_if]
        destination = ["}", "}", "}", "}", "else"]
        self.communications_for_keywords = dict(zip(movable_words, list(zip(movement,
                                                                            number_of_spaces,
                                                                            destination))))
        keyblocks = ["class", "interface", "method", "while", "for", "switch"]
        reg_keyblock = ["[\w\n\s]*class[\w,\s\n]*\{", "[\w\n\s]*interface[\w,\s\n]*\{",
                        "[\n\s\w]*\w+[\n\s]+\w+[\n\s]*\([\w,<>\n\s\[\]*\)[\n\s]*\w*\{",
                        "[\n\s]*while[\n\s]*\([\w;=<>+\(\).\-\n\s]*\)[\n\s]*\{",
                        "[\n\s]*for[\n\s]*\([\w;=<>+\(\).\-\n\s]*\)[\n\s]*\{",
                        "[\n\s]*switch[\n\s]*\([\w;=<>+\(\).\-\n\s]*\)[\n\s]*\{"]
        number_of_lines = [Settings.get_blank_lines_near_class,
                           Settings.get_blank_lines_near_interface,
                           Settings.get_blank_lines_near_method,
                           Settings.get_blank_lines_near_while,
                           Settings.get_blank_lines_near_for, Settings.get_blank_lines_near_switch]
        self.communications_for_keyblocks = dict(zip(keyblocks, list(zip(reg_keyblock,
                                                                         number_of_lines))))

    def add_code(self, file_name):
        """
        Считывание кода из файла в переменную "self.java_code" без пустых строк.
        :param file_name: имя файла, из которого необходимо считать код.
        """
        java_code = ""
        with open(file_name) as input_file_reader:
            for line in input_file_reader:
                if line.strip() != "":
                    java_code += line
        self.java_code = java_code

    def __check_code_emptiness(self):
        """
        Проверка, был ли загружен код.
        :return: True - файл не был загружен. False - файл был загружен.
        """
        if self.java_code == "":
            print("Код не был загружен или файл, откуда вы пытались загрузить его, был пуст.")
            return True
        else:
            return False

    def __move_bbracket_to_new_line(self, i, number_of_begin_bracket, settings):
        """
        Вызов происходит из метода use_style, если 1) встретилась открывающаяся
        фигурная скобка и в настройках (файл current_settings.txt) переменная
        "move_begin_bracket_to_operator" имеет значение False 2) обрабатывается
        нестатический блок.
        :param i: текущая позиция в обрабатываемом коде.
        :param number_of_begin_bracket: текущее количество открывающихся фигурных скобок
        :param settings: объект класса Settings
        :return: позиция, с которой необходимо начинать следующую обработку кода.
        """
        setting1 = settings.get_number_of_spaces_before_brackets()
        setting2 = settings.get_number_of_spaces_inside_block()
        if not self.java_code[:i].endswith("\n"):
            self.java_code = self.java_code[:i] + "\n" + self.java_code[i:]
            i += 1
        prew_number_of_newlines = self.java_code[i + 1:].count("\n") - \
            self.java_code[i + 1:].lstrip().count("\n")
        if prew_number_of_newlines == 0:
            prew_number_of_newlines = 1
        shift = setting1 * number_of_begin_bracket \
            + setting2 * (number_of_begin_bracket - 1)
        self.java_code = self.java_code[:i] + \
            " " * shift + \
            "{" + "\n" * prew_number_of_newlines + self.java_code[i + 1:].lstrip()
        i += shift + 1
        return i

    def __process_bbracket_without_movement(self, i, settings):
        """
        Вызов происходит из метода "use_style", если 1) встретилась открывающаяся фигурная скобка и
        в файле "current_settings.txt" переменная "move_begin_bracket_to_operator" имеет значение True
        2) обрабатывается инициализация массива.
        :param i: текущая позиция в обрабатываемом коде.
        :param settings: объект класса Settings.
        :return: позиция, с которой необходимо начать следующую обработку кода.
        """
        setting = settings.get_number_of_spaces_before_begin_bracket()
        number_of_spaces_for_move = i - \
            len(self.java_code[:i].rstrip())
        prew_number_of_newlines = self.java_code[i + 1:].count("\n") -\
            self.java_code[i + 1:].lstrip().count("\n")
        if prew_number_of_newlines == 0:
            prew_number_of_newlines = 1
        self.java_code = self.java_code[:i].rstrip() \
            + " " * setting \
            + "{" + "\n" * prew_number_of_newlines + self.java_code[i + 1:].lstrip()
        i += setting + 1 - number_of_spaces_for_move
        return i

    def __process_newline(self, i, number_of_begin_bracket, settings):
        """
        Вызов происходит из метода "use_style", если встретился символ перевода строки.
        Если за ним не следует открывающаяся или закрывающаяся фигурная скобка, то
        вставляется необходимое количество пробелов после символа перевода строки.
        :param i: текущая позиция в обратываемом коде
        :param number_of_begin_bracket: текущее количество открывающихся фигурных скобок.
        :param settings: объект класса Settings
        :return: позиция, с которой необходимо начать следующую обработку кода.
        """
        setting1 = settings.get_number_of_spaces_before_brackets()
        setting2 = settings.get_number_of_spaces_inside_block()
        self.java_code += "\n"
        if self.java_code[i + 1] != "{" \
                and self.java_code[i + 1] != "}":
            self.java_code = self.java_code[:i + 1] \
                + " " * number_of_begin_bracket * (setting2 + setting1) \
                + self.java_code[i + 1:]
        self.java_code = self.java_code[:-1]
        i += 1
        return i

    def __process_end_bracket(self, i, number_of_begin_bracket, settings):
        """
        Вызов происходит из метода "use_style", если встретилась закрывающаяся фигурная
        скобка.
        :param i: текущая позиция в обрабатываемом коде.
        :param number_of_begin_bracket: текущее количество открывающихся фигурных
        скобок.
        :param settings: объект класса Settings.
        :return: позиция, с которой необходимо начать следующую обработку кода.
        """
        setting1 = settings.get_number_of_spaces_before_brackets()
        setting2 = settings.get_number_of_spaces_inside_block()
        if not self.java_code[:i].endswith("\n"):
            self.java_code = self.java_code[:i] + "\n" + self.java_code[i:]
            i += 1
        prew_number_of_newlines = self.java_code[i + 1:].count("\n") - \
            self.java_code[i + 1:].lstrip().count("\n")
        if i == len(self.java_code.rstrip()) - 1:
            prew_number_of_newlines -= 1
        elif prew_number_of_newlines == 0:
            prew_number_of_newlines = 1
        if len(self.java_code.rstrip()) - 1 == i:
            prew_number_of_newlines += 1
        self.java_code = self.java_code[:i] \
            + " " * setting1 * number_of_begin_bracket \
            + " " * setting2 * (number_of_begin_bracket - 1) \
            + "}" + "\n" * prew_number_of_newlines + self.java_code[i + 1:].lstrip()
        i += setting1 * number_of_begin_bracket + setting2 * \
            (number_of_begin_bracket - 1) + 1
        self.java_code += "\n\n"
        if self.java_code[i + 1] == ";":
            self.java_code = self.java_code[:i] + self.java_code[i + 1:]
        self.java_code = self.java_code[:-2]
        return i

    def __move_keyword(self, settings, movable_word):
        """
        Перемещение ключевых слов(else, catch, finally, while, if).
        Вызов происходит из методов "move_else", "move_catch", "move_finally",'move_while",
        "move_if".
        если значение переменной "move_*" для данного ключевого слова в файле "current_settings.txt"
        равно True, то ключевое слово перемещается к закрывающейся фигурной скобке (за исключением
        if. перемещается к else). Если значение переменной False, то перемещается на новую строку.
        Код внутри теста и внутри комментариев не обрабатывается.
        :param settings: объект класса Settings
        :param movable_word: перемещаемое ключевое слово.
        :return:
        """
        if self.__check_code_emptiness():
            return
        move_to_destination = self.communications_for_keywords.get(movable_word)[0](settings)
        destination = self.communications_for_keywords.get(movable_word)[2]
        number_of_spaces = self.communications_for_keywords.get(movable_word)[1](settings)
        i = 0
        setting = settings.get_number_of_spaces_before_brackets()
        reg_comments = re.compile("[/\"]")
        while True:
            position_key_word = self.java_code.find(
                movable_word, i)
            if position_key_word == -1:
                break
            position_comment_or_text = reg_comments.search(self.java_code, i)
            if not position_comment_or_text is None and position_comment_or_text.span()[0] <\
                    position_key_word:
                i = self.__process_comments_and_text(position_comment_or_text.span()[0]) + 1
                if i == 2:
                    return self.java_code
                continue
            i = position_key_word
            if self.java_code[:i].rstrip().endswith(destination):
                if not move_to_destination:
                    over_future_position_key_word = self.java_code.rfind("}", 0, i)
                    position_newline = self.java_code.rfind("\n", 0,
                                                            over_future_position_key_word)
                    need_number_of_spaсes = over_future_position_key_word - position_newline - \
                        setting - 1
                    self.java_code = self.java_code[:i].rstrip() \
                        + "\n" + " " * need_number_of_spaсes \
                        + self.java_code[i:]
                    i += need_number_of_spaсes + 2
                else:
                    number_of_spaсes_for_move = len(self.java_code[:i]) - len(
                        self.java_code[:i].rstrip())
                    self.java_code = self.java_code[:i].rstrip() + \
                        " " * number_of_spaces + self.java_code[i:]
                    i += number_of_spaces - number_of_spaсes_for_move + 1
                    continue
            i += 1

    def __move_operators(self, i):
        """
        Вызывается из метода "use_style". Если несколько операторов расположены в одной строке,
        то перемещает оператор(ы) на новую строку, оставляя в каждой строке один оператор.
        :param i: текущая позиция в обрабатываемом коде.
        :return: позиция, с которой начинается следующая обработка кода.
        """
        self.java_code += "\n"
        if self.java_code[i+1].isalnum() or self.java_code[i+1] == " ":
            self.java_code = self.java_code[:i+1] + "\n" + self.java_code[i+1:].lstrip()
        i += 1
        self.java_code = self.java_code[:-1]
        return i

    def __delete_spaces(self):
        """
        Вызывается из метода "use_style".
        Удаляет пробелы в начале в конце строк обрабатываемого кода, за исключением
        строк, которые располагаются в комментариях и внутри текста.
        :return: позиция, с которой необходимо начинать следующую обработку кода.
        """
        reading_comment = False
        split_java_code = self.java_code.split("\n")
        changed_java_code = ""
        for line in split_java_code:
            if line.find("/*") != -1:
                reading_comment = True
            if not reading_comment:
                changed_java_code += line.strip() + "\n"
            else:
                changed_java_code += line + "\n"
            if "*/" in line:
                reading_comment = False
        return changed_java_code[:-1]

    def __delete_spaces_in_end_of_strings(self):
        """
        Вызывается в конце метода use_style для удаления пробелов в конце строк.
        :return:  измененный код.
        """
        split_java_code = self.java_code.split("\n")
        changed_java_code = ""
        for i in split_java_code:
            changed_java_code += i.rstrip() + "\n"
        return changed_java_code[:-1]

    def __blank_lines_near_keyblock(self, settings, keyword):
        """
        Вызывается из методов "blank_lines_near_*". Используется регулирования
        количество пустых строк вокруг ключевых блоков (классы, интерфейсы,
        методы, циклы for и while, операторы выбора switch).
        Код внутри теста и внутри комментариев не обрабатывается.
        :param settings: объект класса Settings.
        :param keyword: ключевое слово, которое связывется с перемещаемыми ключевыми
        блоками (class, interface, method, for, while, switch).
        """
        if self.__check_code_emptiness():
            return
        setting1 = settings.get_number_of_spaces_before_brackets()
        setting2 = settings.get_number_of_spaces_inside_block()
        i = 0
        reg_comments_and_brackets = re.compile(r"[/\"\{}]")
        if not keyword in self.communications_for_keyblocks:
            return
        reg_keyblock = re.compile(self.communications_for_keyblocks.get(keyword)[0])
        number_of_lines = self.communications_for_keyblocks.get(keyword)[1](settings)
        number_of_begin_brackets = 0
        fixed_number_of_brackets = [-1]
        while True:
            position_keyblock = reg_keyblock.search(self.java_code, i)
            position_comment_or_text = reg_comments_and_brackets.search(self.java_code, i)
            if not position_keyblock is None and not position_comment_or_text is None:
                i = min(position_keyblock.span()[0], position_comment_or_text.span()[0])
            elif position_keyblock is None and position_comment_or_text is None:
                break
            elif not position_keyblock is None:
                i = position_keyblock.span()[0]
            else:
                i = position_comment_or_text.span()[0]
            result_process_comment = self.__process_comments_and_text(i)
            if i != result_process_comment:
                if result_process_comment <= 1:
                    return self.java_code
                i = result_process_comment
                continue
            if self.java_code[i] == "{":
                number_of_begin_brackets += 1
                i += 1
                continue
            elif self.java_code[i] == "}":
                number_of_begin_brackets -= 1
                if fixed_number_of_brackets[-1] == number_of_begin_brackets:
                    self.java_code += "\n"
                    if self.java_code[i+1:].lstrip().startswith("}"):
                        self.java_code = self.java_code[:i+1] + "\n" \
                            * (number_of_lines + 1) + " " * ((number_of_begin_brackets - 1) *
                                                             setting2 + number_of_begin_brackets *
                                                             setting1) + \
                            self.java_code[i+1:].lstrip()
                    else:
                        self.java_code = self.java_code[:i+1] + "\n" \
                            * (number_of_lines + 1) + " " * number_of_begin_brackets * \
                            (setting2 + setting1) + \
                            self.java_code[i+1:].lstrip()
                    self.java_code = self.java_code[:-1]
                    fixed_number_of_brackets.pop()
                i += 1
                continue
            else:
                position_keyblock = position_keyblock.span()
                number_of_spaces_for_move = len(self.java_code[i:]) -\
                    len(self.java_code[i:].lstrip())
                self.java_code = self.java_code[:i] + "\n" * \
                    number_of_lines + " " * number_of_begin_brackets * \
                    (setting2 +
                        setting1) + self.java_code[i:].lstrip()
                if i != 0:
                    self.java_code = self.java_code[:i] + "\n" + self.java_code[i:]
                i = i + number_of_lines + position_keyblock[1]   \
                    - number_of_spaces_for_move - position_keyblock[0] + number_of_begin_brackets *\
                    (setting2 + setting1) + 1
                fixed_number_of_brackets.append(number_of_begin_brackets)
                number_of_begin_brackets += 1

    def spaces_around_operators(self, settings):
        """
        Регулирует количество пробелов вокруг унарных и бинарных операторов, которые
        задаются отдельно друг от друга.
        Код внутри теста и внутри комментариев не обрабатывается.
        :param settings: объект класса Settings.
        """
        if self.__check_code_emptiness():
            return
        spaces_around_binary = settings.get_spaces_around_binary_operators()
        spaces_around_unary = settings.get_spaces_around_unary_operators()
        i = 0
        reg_operators = re.compile("(\+\+)|(\-\-)|[+\-*/=&|^><!~][<>=&|]?[<>=]?")
        reg_comments = re.compile("[/\"]")
        symbols_after_unary_operators = ["\"", ")", "]", "”"]
        symbols_before_unary_operators = ["\"", "(", "-", "+", "~", "[", "{", "“", "!"]
        reg_parameterization = re.compile("<[\w+\s,]+>")
        while True:
            position_operator = reg_operators.search(self.java_code, i)
            if position_operator is None:
                break
            position_parameterization = reg_parameterization.search(self.java_code, i)
            if position_parameterization is not None and position_operator.span()[0] == \
                    position_parameterization.span()[0]:
                i = position_parameterization.span()[1]
                continue
            position_commentary = reg_comments.search(self.java_code, i)
            if position_commentary is None:
                i = position_operator.span()[0]
            else:
                i = min(position_operator.span()[0], position_commentary.span()[0])
                comments_process = self.__process_comments_and_text(i)
                if comments_process <= 1:
                    return self.java_code
                if comments_process != i:
                    i = comments_process
                    continue
            operator = self.java_code[i:position_operator.span()[1]]
            if (self.java_code[:i].rstrip()[-1].isalnum() or self.java_code[:i].rstrip()[-1] in
                symbols_after_unary_operators) and\
                    (self.java_code[i+len(operator):].lstrip()[0].isalnum() or
                        self.java_code[i+len(operator):].lstrip()[0] in
                        symbols_before_unary_operators):
                number_of_spaces = len(self.java_code[:i]) - len(self.java_code[:i].rstrip())
                self.java_code = self.java_code[:i].rstrip() + " " * spaces_around_binary + \
                    self.java_code[i:i+len(operator)] + " " * spaces_around_binary + \
                    self.java_code[i+len(operator):].lstrip()
                i = i - number_of_spaces + spaces_around_binary + len(operator)
            elif self.java_code[:i].rstrip()[-1].isalnum():
                number_of_spaces = len(self.java_code[:i]) - len(self.java_code[:i].rstrip())
                self.java_code = self.java_code[:i].rstrip() + " " * spaces_around_unary +\
                    self.java_code[i:]
                i = i - number_of_spaces + len(operator) + spaces_around_unary
            else:
                self.java_code = self.java_code[:i+len(operator)] + " " * spaces_around_unary +\
                    self.java_code[i+len(operator):].lstrip()
                i += len(operator) + spaces_around_unary
        return self.java_code

    def __spaces_after_punctuation_mark(self, settings, punctuation_mark):
        """
        Вызывается из методов "spaces_after_comma" и "spaces_after_semicolon".
        Регулирует количество пробелов после запятой или после точки с запятой.
        Код внутри теста и внутри комментариев не обрабатывается.
        :param settings: объект класса Settings.
        :param punctuation_mark: знак препинания, после которого необходимо изменить
        число пробелов.
        """
        if self.__check_code_emptiness():
            return
        reg_key_symbols = re.compile("[%s\"/]" % punctuation_mark)
        if punctuation_mark == ",":
            number_of_spaces = settings.get_spaces_after_comma()
        else:
            number_of_spaces = settings.get_spaces_after_semicolon()
        i = 0
        while True:
            process_key_symbols = reg_key_symbols.search(self.java_code, i)
            if process_key_symbols is None:
                break
            i = process_key_symbols.span()[0]
            result_process_comment = self.__process_comments_and_text(i)
            if result_process_comment <= 1:
                self.java_code = self.__delete_spaces_in_end_of_strings()
                return self.java_code
            if i != result_process_comment:
                i = result_process_comment
            elif self.java_code[i+1:].count("\n") == self.java_code[i+1:].lstrip().count("\n"):
                number_of_spaces_for_move = len(self.java_code[:i]) -\
                    len(self.java_code[:i].rstrip())
                self.java_code = self.java_code[:i].rstrip() + punctuation_mark + " " * \
                    number_of_spaces + \
                    self.java_code[i+1:].lstrip()
                i = i - number_of_spaces_for_move + 1
            else:
                i += 1

    def __process_comments_and_text(self, i):
        """
        Проверяет, что распологается на переданной текущей позиции кода:
        многострочный комментарий, однострочный комментарий или текст.
        Если это комментарий, то возвращается позицию конца комментария,
        если тект, то позицию окончания текста. Если ни то, ни другое,
        то возращается позиция без изменений.
        :param i: текущая позиция в обрабатываемом коде.
        :return: позиция, с которой необходимо начинать следующую обработку кода.
        """
        if self.java_code[i:i+2] == "/*":
            i = self.java_code.find("*/", i + 1) + 2
            return i
        if self.java_code[i] == "\"":
            i = self.java_code.find("\"", i + 1) + 1
            return i
        if self.java_code[i:i+2] == "//":
            i = self.java_code.find("\n", i + 1)
        return i

    def blank_lines_near_class(self, settings):
        """
        Вызывает метод "__blank_lines_near_keyblock" для классов.
        :param settings: объект класса Settings.
        """
        self.__blank_lines_near_keyblock(settings, "class")
        return self.java_code

    def blank_lines_near_interface(self, settings):
        """
        Вызывает метод "__blank_lines_near_keyblock" для интерфейсов.
        :param settings: объект класса Settings.
        """
        self.__blank_lines_near_keyblock(settings, "interface")
        return self.java_code

    def blank_lines_near_method(self, settings):
        """
        Вызывает метод "__blank_lines_near_keyblock" для методов.
        :param settings: объект класса Settings.
        """
        self.__blank_lines_near_keyblock(settings, "method")
        return self.java_code

    def blank_lines_near_while(self, settings):
        """
        Вызывает метод "__blank_lines_near_keyblock" для циклов while.
        :param settings: объект класса Settings.
        """
        self.__blank_lines_near_keyblock(settings, "while")
        return self.java_code

    def blank_lines_near_for(self, settings):
        """
        Вызывает метод "__blank_lines_near_keyblock" для циклов for.
        :param settings: объект класса Settings
        """
        self.__blank_lines_near_keyblock(settings, "for")
        return self.java_code

    def blank_lines_near_switch(self, settings):
        """
        Вызывает метод "__blank_lines_near_keyblock" для операторов выбора switch.
        :param settings: объект класса Settings.
        """
        self.__blank_lines_near_keyblock(settings, "switch")
        return self.java_code

    def move_else(self, settings):
        """
        Вызывает метод "__move_keyword" для ключевого слова else".
        :param settings: объект класса Settings.
        """
        self.__move_keyword(settings, "else")
        return self.java_code

    def move_catch(self, settings):
        """
        Вызывает метод "__move_keyword" для ключевого слова catch"
        :param settings: объект класса Settings.
        """
        self.__move_keyword(settings, "catch")
        return self.java_code

    def move_finally(self, settings):
        """
        Вызывает метод "__move_keyword" для ключевого слова finally"
        :param settings: объект класса Settings.
        """
        self.__move_keyword(settings, "finally")
        return self.java_code

    def move_while(self, settings):
        """
        Вызывает метод "__move_keyword" для ключевого слова while"
        :param settings: объект класса Settings.
        """
        self.__move_keyword(settings, "while")
        return self.java_code

    def move_if(self, settings):
        """
        Вызывает метод "__move_keyword" для ключевого слова if"
        :param settings: объект класса Settings.
        """
        self.__move_keyword(settings, "if")
        return self.java_code

    def spaces_after_comma(self, settings):
        """
        Вызывает метод "__spaces_after_punctuation_mark" для запятой.
        :param settings:
        """
        self.__spaces_after_punctuation_mark(settings, ",")
        return self.java_code

    def spaces_after_semicolon(self, settings):
        """
        Вызывает метод "__spaces_after_punctuation_mark" для точки с запятой.
        :param settings: объект класса Settings.
        """
        self.__spaces_after_punctuation_mark(settings, ";")
        return self.java_code

    def use_style(self, settings):
        """
        Изменяет стиль кода, исходя из значений четырех переменных в файле
        "current_settings.txt": "move_begin_bracket_to_operator", "number_of_spaces_before_brackets",
        "number_of_spaces_before_begin_bracket", "number_of_spaces_inside_block".
        Код внутри текста и внутри комментариев не обрабатывается. Если
        массив в коде проинициализирован в одной строке, то вызов методов перемещения открывающейся
        и закрывающейся фигурных скобок не происходит. В случае инициализации на нескольких
        строках, открывающаяся фигурная скобка переносится к знаку "=".
        Открывающаяся фигурная скобка нестатического блока всегда переносится на новую строку.
        :param settings: объект класса Settings.
        """
        if self.__check_code_emptiness():
            return
        self.java_code = self.__delete_spaces()
        setting1 = settings.get_move_begin_bracket_to_operator()
        i = 0
        number_of_begin_brackets = 0
        number_of_b_round_bracket = 0
        reg_processed_symbols = re.compile("[\{}\n/\";()]")
        while True:
            i = reg_processed_symbols.search(self.java_code, i)
            if i is None:
                break
            i = i.span()[0]
            result_process_comment_and_text = self.__process_comments_and_text(i)
            if result_process_comment_and_text != i:
                if result_process_comment_and_text <= 1:
                    self.java_code = self.__delete_spaces_in_end_of_strings()
                    return self.java_code
                i = result_process_comment_and_text
                continue
            if self.java_code[i] == "\n":
                i = self.__process_newline(i, number_of_begin_brackets, settings)
                continue
            if self.java_code[i] == "}":
                i = self.__process_end_bracket(i, number_of_begin_brackets, settings)
                number_of_begin_brackets -= 1
                if number_of_begin_brackets == -1:
                    print("Пожалуйста, проверьте соотвествие числа открывающихся"
                          " и закрывающихся фигурных скобок. Лишние закрывающиеся"
                          " фигурные скобки обработаны не будут.")
                    return
                continue
            if self.java_code[i] == ";":
                if number_of_b_round_bracket == 0:
                    i = self.__move_operators(i)
                else:
                    i += 1
                continue
            if self.java_code[i] == "(":
                number_of_b_round_bracket += 1
                i += 1
                continue
            if self.java_code[i] == ")":
                number_of_b_round_bracket -= 1
                i += 1
                continue
            if self.java_code[i] == "{":
                non_static_and_array_check = self.java_code[:i].rstrip()[-1]
                if non_static_and_array_check == "=" or non_static_and_array_check == "]":
                    if self.java_code.find(";", i) < self.java_code.find("\n", i):
                        i = self.java_code.find(";", i)
                        continue
                    else:
                        number_of_begin_brackets += 1
                        i = self.__process_bbracket_without_movement(i, settings)
                        continue
                number_of_begin_brackets += 1
                if (not setting1 or non_static_and_array_check == ";"
                    or non_static_and_array_check == "{"
                    or non_static_and_array_check == "}"
                        or non_static_and_array_check == "/"):
                    i = self.__move_bbracket_to_new_line(i, number_of_begin_brackets, settings)
                else:
                    i = self.__process_bbracket_without_movement(i, settings)
        self.java_code = self.__delete_spaces_in_end_of_strings()
        return self.java_code

    def output_code_to_file(self, file_name):
        """
        Метод выводит код из переменной "self.java_code" в файл.
        :param file_name: имя файла для вывода.
        """
        if self.__check_code_emptiness():
            return
        with open(file_name, "w") as code_output:
            code_output.write(self.java_code)