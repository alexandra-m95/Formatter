from gi.repository import Gtk
from formatter import *


class FormatterWindow(Gtk.Window):
    def __init__(self):
        """
        Метод создает объекты классов Formatter и Settings. Множество
        called_formatter_functions_for_apply будет сохранять те функции,
        которые необходимо вызвать после нажатие кнопки "Apply". Затем оно
        будет очищено.
        sensitive_custom_style - доступно ли редактирование пользовательского стиля кода.
        all_called_formatter_functions - храние всех вызванных функции объекта класса
        Formatter за все время работы программы. Это необходимо для того, чтобы после
        повторной загрузки файла можно было применить к коду все старые настройки.
        communications_of_widgets_and_settings - связь между виджетами и
        методами класса Settings. Сразу после применения действий к виджету вызывается
        настройка, которая с ним связана. communications_of_widgets_and_formatter_functions -
        аналогично (только для функций объекта класса Formatter.)
        sensitives_in_widgets - связь между виджетами, которая определяет, какие
        виджеты необходимо сделать недоступными после активации того или иного виджета.
        self.keyword_combo_widgets - содержит все выпадающие списки, которые отвечают
        за настройку расположения ключевых слов. После того, как мы изменяем стиль кода,
        идет проверка, какие виджеты из self.keyword_combo_widgets являлись во время
        предыдущего применения настроек активными и в них вписываетс пустое значение. Это делается
        потому что изменение стиля кода изменяет расположение ключевых слов.

        """
        Gtk.Window.__init__(self, title="Formatter")
        self.set_border_width(20)
        self.set_resizable(False)
        self.formatter = Formatter()
        self.settings = Settings()
        self.input_file_name = ""
        self.sensitive_custom_style = False
        self.called_formatter_functions_for_apply = set()
        self.called_formatter_functions_for_apply.add(self.formatter.use_style)
        self.all_called_formatter_functions = set()
        self.settings.set_1TBS()
        self.communications_of_widgets_and_settings = {}
        self.communications_of_widgets_and_formatter_functions = {}
        self.sensitives_in_widgets = {}
        self.keyword_combo_widgets = []
        self.custom_widgets = []
        self.add(self.add_widgets())

    def add_widgets(self):
        """
        Метод создает контейнер и вызывает методы для
        добавления всех виджетов в него.
        :return: контейнер с виджетами.
        """
        fixing_box = Gtk.Fixed()
        fixing_box.add(self.add_menu_bar())
        fixing_box.put(self.add_text_view(), 380, 0)
        fixing_box.put(self.add_notebook(), 0, 0)
        apply_button = Gtk.Button("Apply")
        apply_button.set_size_request(120, 35)
        apply_button.connect("clicked", self.on_apply_clicked)
        fixing_box.put(apply_button, 120, 370)
        return fixing_box

    def add_text_view(self):
        """
        Создает контейнер, в который добавляется рамка с другим контейнером.
        В него добавляется многострочный текстовый редактор с полосами прокрутки.
        :return: рамка с контейнером, который содержит многострочный текстовый редактор.
        """
        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_buffer = self.text_view.get_buffer()
        box = Gtk.Box()
        scrolledwindow = Gtk.ScrolledWindow()
        frame = Gtk.Frame()
        scrolledwindow.set_size_request(350, 400)
        scrolledwindow.add(self.text_view)
        box.pack_start(scrolledwindow, True, True, 0)
        frame.add(box)
        return frame

    def add_notebook(self):
        """
        Возвращает закладки и вызывает функции для добавления контейнеров с виджетами в
        каждую закладку.

        :return: закладки
        """
        notebook = Gtk.Notebook()
        notebook.set_size_request(150, 350)
        notebook.append_page(self.add_page1_to_notebook(), Gtk.Label("Code style"))
        notebook.append_page(self.add_page2_to_notebook(), Gtk.Label("Blank lines"))
        notebook.append_page(self.add_page3_to_notebook(), Gtk.Label("Keywords"))
        notebook.append_page(self.add_page4_to_notebook(), Gtk.Label("Other Settings"))
        return notebook

    def add_menu_bar(self):
        """
        Создает меню.

        :return: меню.
        """
        menu_bar = Gtk.MenuBar()
        file_menu = Gtk.Menu()
        help_menu = Gtk.Menu()
        file_item = Gtk.MenuItem("File")
        help_item = Gtk.MenuItem("Help")
        open_item = Gtk.MenuItem("Open..")
        quit_item = Gtk.MenuItem("Exit")
        information_item = Gtk.MenuItem("About Formatter")
        self.save_item = Gtk.MenuItem("Save")
        self.save_as_item = Gtk.MenuItem("Save As..")
        self.save_item.set_sensitive(False)
        self.save_as_item.set_sensitive(False)
        open_item.connect_object("activate", self.show_file_open, "file.open")
        self.save_item.connect_object("activate", self.show_file_save, "file.save")
        self.save_as_item.connect_object("activate", self.show_file_save_as, "file.save")
        quit_item.connect_object("activate", self.destroy, "file.quit")
        information_item.connect_object("activate", self.show_help, "file.help.txt")
        file_menu.append(open_item)
        file_menu.append(self.save_item)
        file_menu.append(self.save_as_item)
        file_menu.append(quit_item)
        help_menu.append(information_item)
        file_item.set_submenu(file_menu)
        help_item.set_submenu(help_menu)
        menu_bar.append(file_item)
        menu_bar.append(help_item)
        return menu_bar

    def add_page1_to_notebook(self):
        """
        Создается контейнер и виджеты, которые будет он содержать(для первой страницы
        закладок).

        :return: контейнер с виджетами.
        """
        fixing_box = Gtk.Fixed()
        bbracket_positions = ["on new line", "near operator"]
        labels = ["Begin bracket:", "Spaces", "Before brackets:", "Before begin bracket:",
                  "Inside block:"]
        checkbutton_labels = ["BSD", "WS", "GNU", "Custom"]
        settings_for_checkbutton = [self.settings.set_BSD, self.settings.set_WS,
                                    self.settings.set_GNU]
        otbs_button = Gtk.RadioButton.new_with_label_from_widget(None, "1TBS")
        otbs_button.connect("toggled", self.on_built_style_toggled)
        fixing_box.put(otbs_button, 0, 15)
        self.communications_of_widgets_and_settings[otbs_button] = self.settings.set_1TBS
        for i in range(len(checkbutton_labels)):
                checkbutton = Gtk.RadioButton.new_with_label_from_widget(otbs_button,
                                                                         checkbutton_labels[i])
                if i != 3:
                    checkbutton.connect("toggled", self.on_built_style_toggled)
                    self.communications_of_widgets_and_settings[checkbutton] = \
                        settings_for_checkbutton[i]
                else:
                    checkbutton.connect("toggled", self.on_custom_toggled)
                fixing_box.put(checkbutton, 75 + 67 * i, 15)
        bbracket_positions_combo = Gtk.ComboBoxText()
        bbracket_positions_combo.set_sensitive(False)
        bbracket_positions_combo.connect("changed", self.on_name_combo_changed)
        for i in bbracket_positions:
            bbracket_positions_combo.append_text(i)
        self.custom_widgets.append(bbracket_positions_combo)
        settings_for_spinbuttons = [self.settings.set_number_of_spaces_before_brackets,
                                    self.settings.set_number_of_spaces_before_begin_bracket,
                                    self.settings.set_number_of_spaces_inside_block]
        for i in range(3):
            spinbutton = Gtk.SpinButton()
            self.custom_widgets.append(spinbutton)
            spinbutton.set_sensitive(False)
            adjustment = Gtk.Adjustment(0, 0, 10, 1, 10, 0)
            adjustment.connect("value_changed", self.change_digits)
            spinbutton.set_adjustment(adjustment)
            fixing_box.put(spinbutton, 240, 165 + 50 * i)
            self.communications_of_widgets_and_settings[adjustment] = settings_for_spinbuttons[i]
            self.communications_of_widgets_and_formatter_functions[adjustment] = \
                self.formatter.use_style
        for i in range(len(labels)):
            if i != 1:
                fixing_box.put(Gtk.Label(labels[i]), 10, 70 + 50 * i)
            else:
                fixing_box.put(Gtk.Label(labels[i]), 140, 70 + 50 * i)
        fixing_box.put(bbracket_positions_combo, 215, 60)
        self.communications_of_widgets_and_settings[bbracket_positions_combo] =\
            self.settings.set_move_begin_bracket_to_operator
        self.communications_of_widgets_and_formatter_functions[bbracket_positions_combo] = \
            self.formatter.use_style
        return fixing_box

    def add_page2_to_notebook(self):
        """
        Создается контейнер и виджеты, которые будет он содержать(для второй страницы
        закладок).
        :return: контейнер с виджетами.
        """
        fixing_box = Gtk.Fixed()
        keyblock_labels = ["Around class:", "Around interface:", "Around method:",
                           "Around while:", "Around for:", "Around switch:"]
        settings_for_keyblocks = [self.settings.set_blank_lines_near_class,
                                  self.settings.set_blank_lines_near_interface,
                                  self.settings.set_blank_lines_near_method,
                                  self.settings.set_blank_lines_near_while,
                                  self.settings.set_blank_lines_near_for,
                                  self.settings.set_blank_lines_near_switch]
        formatter_funcs_for_keyblocks = [self.formatter.blank_lines_near_class,
                                         self.formatter.blank_lines_near_interface,
                                         self.formatter.blank_lines_near_method,
                                         self.formatter.blank_lines_near_while,
                                         self.formatter.blank_lines_near_for,
                                         self.formatter.blank_lines_near_switch]
        for i in range(len(keyblock_labels)):
            fixing_box.put(Gtk.Label(keyblock_labels[i]), 10, 20 + 50 * i)
        for i in range(6):
            spin_button = Gtk.SpinButton()
            adjustment = Gtk.Adjustment(0, 0, 10, 1, 10, 0)
            adjustment.connect("value_changed", self.change_digits)
            self.communications_of_widgets_and_settings[adjustment] = settings_for_keyblocks[i]
            self.communications_of_widgets_and_formatter_functions[adjustment] =\
                formatter_funcs_for_keyblocks[i]
            spin_button.set_adjustment(adjustment)
            fixing_box.put(spin_button, 240, 15 + 50 * i)
        return fixing_box

    def add_page3_to_notebook(self):
        """
        Создается контейнер и виджеты, которые будет он содержать(для третьей страницы
        закладок).
        :return: контейнер с виджетами.
        """
        fixing_box = Gtk.Fixed()
        formatter_funcs_for_keywords = [self.formatter.move_else, self.formatter.move_catch,
                                        self.formatter.move_finally, self.formatter.move_while,
                                        self.formatter.move_if]
        movable_settings_for_keywords = [self.settings.set_move_else_to_end_bracket,
                                         self.settings.set_move_catch_to_end_bracket,
                                         self.settings.set_move_finally_to_end_bracket,
                                         self.settings.set_move_while_to_end_bracket,
                                         self.settings.set_move_if_to_else]
        spaces_settings_for_keywords = [self.settings.set_number_of_spaces_before_else,
                                        self.settings.set_number_of_spaces_before_catch,
                                        self.settings.set_number_of_spaces_before_finally,
                                        self.settings.set_number_of_spaces_before_while,
                                        self.settings.set_number_of_spaces_before_if]
        for i in range(5):
            spinbutton = Gtk.SpinButton()
            spinbutton.set_sensitive(False)
            positions_combo = Gtk.ComboBoxText()
            positions_combo.connect("changed", self.on_name_combo_changed)
            positions_combo.append_text("on new line")
            if i != 4:
                adjustment = Gtk.Adjustment(0, 0, 10, 1, 10, 0)
                positions_combo.append_text("near end bracket")
            else:
                adjustment = Gtk.Adjustment(1, 1, 10, 1, 10, 0)
                positions_combo.append_text("near else")
                positions_combo.set_size_request(153, 20)
            adjustment.connect("value_changed", self.change_digits)
            self.sensitives_in_widgets[positions_combo] = spinbutton
            spinbutton.set_adjustment(adjustment)
            fixing_box.put(positions_combo, 70, 53 + 50 * i)
            fixing_box.put(spinbutton, 240, 55 + 50 * i)
            self.keyword_combo_widgets.append(positions_combo)
            self.communications_of_widgets_and_formatter_functions[adjustment] = \
                formatter_funcs_for_keywords[i]
            self.communications_of_widgets_and_formatter_functions[positions_combo] =\
                formatter_funcs_for_keywords[i]
            self.communications_of_widgets_and_settings[positions_combo] = \
                movable_settings_for_keywords[i]
            self.communications_of_widgets_and_settings[adjustment] = \
                spaces_settings_for_keywords[i]
        fixing_box.put(Gtk.Label("Position"), 120, 18)
        fixing_box.put(Gtk.Label("Spaces"), 267, 18)
        labels = ["else:", "catch:", "finally:", "while:", "if:"]
        for i in range(5):
            fixing_box.put(Gtk.Label(labels[i]), 10, 60 + i*50)
        return fixing_box

    def add_page4_to_notebook(self):
        """
        Создается контейнер и виджеты, которые будет он содержать(для четвертой страницы
        закладок).

        :return: контейнер с виджетами.
        """
        fixing_box = Gtk.Fixed()
        fixing_box.put(Gtk.Label("Spaces"), 155, 40)
        labels = ["Around unary operators:", "Around binary operators:", "After comma:",
                  "After semicolon:"]
        settings_for_punct_marks = [self.settings.set_spaces_around_unary_operators,
                                    self.settings.set_spaces_around_binary_operators,
                                    self.settings.set_spaces_after_comma,
                                    self.settings.set_spaces_after_semicolon]
        formatter_funcs_for_punct_marks = [self.formatter.spaces_around_operators,
                                           self.formatter.spaces_around_operators,
                                           self.formatter.spaces_after_comma,
                                           self.formatter.spaces_after_semicolon]
        for i in range(4):
            spinbutton = Gtk.SpinButton()
            adjustment = Gtk.Adjustment(0, 0, 10, 1, 10, 0)
            adjustment.connect("value_changed", self.change_digits)
            fixing_box.put(Gtk.Label(labels[i]), 10, 95 + i * 50)
            fixing_box.put(spinbutton, 245, 90 + i * 50)
            spinbutton.set_adjustment(adjustment)
            self.communications_of_widgets_and_settings[adjustment] = settings_for_punct_marks[i]
            self.communications_of_widgets_and_formatter_functions[adjustment] =\
                formatter_funcs_for_punct_marks[i]
        return fixing_box

    def show_file_open(self, widget):
        """
        Вызывается через меню после нажатия на "File" -- >"Open". Создает диалоговое окно для
        выбора файла.
        :param widget: ссылка на объект, к которому был применен сигнал.
        """
        dialog = Gtk.FileChooserDialog("Please choose a file", self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN,
                                        Gtk.ResponseType.OK))
        text_filter = Gtk.FileFilter()
        java_filter = Gtk.FileFilter()
        text_filter.set_name("Text files")
        java_filter.set_name("Java files")
        text_filter.add_mime_type("text/plain")
        java_filter.add_mime_type("text/x-java")
        dialog.add_filter(text_filter)
        dialog.add_filter(java_filter)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.save_item.set_sensitive(True)
            self.save_as_item.set_sensitive(True)
            self.input_file_name = dialog.get_filename()
            self.formatter.add_code(self.input_file_name)
            self.text_buffer.set_text(self.formatter.java_code)
            self.called_formatter_functions_for_apply = \
                self.called_formatter_functions_for_apply.union(self.all_called_formatter_functions)
        dialog.destroy()

    def show_help(self, widget):
        """
        Вызывается через меню после нажатия на "help.txt" --> "About Formatter".
        :param widget: ссылка на объект, к которому был применен сигнал.
        """
        dialog = Gtk.Dialog("About formatter", None, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_size_request(200, 400)
        dialog.set_resizable(False)
        box = Gtk.Box()
        scrolledwindow = Gtk.ScrolledWindow()
        text_view = Gtk.TextView()
        text_buffer = text_view.get_buffer()
        text_view.set_editable(False)
        text_view.set_wrap_mode(True)
        scrolledwindow.set_size_request(330, 400)
        scrolledwindow.add(text_view)
        frame = Gtk.Frame()
        box.pack_start(scrolledwindow, True, True, 0)
        frame.add(box)
        dialog.vbox.pack_start(frame, True, False, 0)
        with open("help.txt") as helps:
            text_buffer.set_text(helps.read())
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
        dialog.destroy()

    def show_file_save(self, widget):
        """
        Вызывается через меню после нажатия на "File" --> "Save".
        :param widget: ссылка на объект, к которому был применен сигнал.
        """
        self.formatter.output_code_to_file(self.input_file_name)

    def show_file_save_as(self, widget):
        """
        Вызывается через меню после нажатия на "File" --> "Save As".
        :param widget: ссылка на объект, к которому был применен сигнал.
        """
        dialog = Gtk.FileChooserDialog("Please choose a file", self, Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.formatter.output_code_to_file(dialog.get_filename())
        dialog.destroy()

    def destroy(self, widget):
        """
        Уничтожает диалоговые окна.
        :param widget: ссылка на виджет, к которому был применен сигнал.
        """
        Gtk.main_quit()

    def on_built_style_toggled(self, widget):
        """
        Вызывается после изменения стиля кода(изменение состояния группы кнопок checkbutton).
        Вызывает метод check_custom_style_sensitive(проверка: являются ли виджеты настройки
        пользовательского стиля кода в данный момент активными.)
        :param widget: ссылка на виджет, к которому был применен сигнал.
        """
        self.check_custom_style_sensitive()
        self.communications_of_widgets_and_settings[widget]()
        self.called_formatter_functions_for_apply.add(self.formatter.use_style)

    def on_custom_toggled(self, widget):
        """
        Вызывается после нажатия на кнопку настроек пользовательского стиля.
        Делает активными настройки и добавляет в них значения по умолчанию.
        :param widget: ссылка на виджет, к которому был применен сигнал.
        """
        self.settings.set_default_style()
        for i in range(len(self.custom_widgets)):
            self.custom_widgets[i].set_sensitive(True)
            if i == 0:
                self.custom_widgets[i].set_active(0)
            else:
                self.custom_widgets[i].set_value(0)
        self.sensitive_custom_style = True
        self.called_formatter_functions_for_apply.add(self.formatter.use_style)

    def check_custom_style_sensitive(self):
        """
        Проверяет, являются ли виджеты, отвечающие за настройку пользовательского стиля,
        активными в данный момент. Если да, то делает виджеты неактивными.

        """
        if self.sensitive_custom_style:
            for i in range(len(self.custom_widgets)):
                self.custom_widgets[i].set_sensitive(False)
                if i == 0:
                    self.custom_widgets[i].set_active(-1)
                else:
                    self.custom_widgets[i].delete_text(0, -1)
            self.sensitive_custom_style = False

    def on_apply_clicked(self, widget):
        """
        Вызывает все функции объекта класса Formatter, которые были добавлены в переменную
        self.called_formatter_functions_for_apply. При этом, если среди данных функций есть
        функция изменения стиля кода, то она вызывается в первую очередь, так как, если среди функ-
        ций есть функции переноса ключевых слов, то изменение стиля кода собьет перенос слов
        к закрывающейся фигурной скобке. Из всех виджетов, отвечающих за перенос ключевых слов,
        которые содержали какие-либо значения во время предыдущего нажатия на "Apply",
        удаляются это самые значения (т.е. виджеты принимают изначальное состояние).
        :param widget: ссылка на виджет, к которому был применен сигнал.
        """
        if self.formatter.java_code == "":
            return
        self.all_called_formatter_functions = \
            self.all_called_formatter_functions.union(self.called_formatter_functions_for_apply)
        if self.formatter.use_style in self.called_formatter_functions_for_apply:
            self.formatter.use_style(self.settings)
            self.called_formatter_functions_for_apply.remove(self.formatter.use_style)
            for i in self.keyword_combo_widgets:
                if not self.communications_of_widgets_and_formatter_functions[i] in \
                        self.called_formatter_functions_for_apply:
                    i.set_active(-1)
                    self.sensitives_in_widgets[i].delete_text(0, -1)
                    self.sensitives_in_widgets[i].set_sensitive(False)
        for i in self.called_formatter_functions_for_apply:
            i(self.settings)
        self.called_formatter_functions_for_apply.clear()
        self.text_buffer.set_text(self.formatter.java_code)

    def on_name_combo_changed(self, combo):
        """
        Вызывается после изменение состояния выпадающих списков.
        Если это список, которые отвечают за настройку переноса ключевых слов и
        текущее состояние "on new line", то виджет, отвечающие за изменение количества
        пробелов после закрывающейся фигурной скобкой (после "else" для настройки переноса
        if) становится неактивным. И наоборот.Также добавляет новую функцию объекта класса
        Formatter в переменную self.called_formatter_functions_for_apply, которую необходимо вызвать
        после нажатия на "Apply".
        :param combo: ссылка на виджет, к которому был применен сигнал.
        """
        text = combo.get_active_text()
        if text == "on new line":
            self.communications_of_widgets_and_settings.get(combo)(False)
            if combo in self.sensitives_in_widgets:
                self.sensitives_in_widgets[combo].set_sensitive(False)
                self.sensitives_in_widgets[combo].delete_text(0, -1)
        else:
            self.communications_of_widgets_and_settings.get(combo)(True)
            if combo in self.sensitives_in_widgets:
                self.sensitives_in_widgets[combo].set_sensitive(True)
                self.sensitives_in_widgets[combo].set_text(str(int(
                    self.sensitives_in_widgets[combo].get_value())))
        self.called_formatter_functions_for_apply.add(
            self.communications_of_widgets_and_formatter_functions[combo])

    def change_digits(self, widget):
        """
        Вызывается после изменения значения в виджетах SpinButton. Применяются
        соотвествующие настройки объекта класса Settings и добавляются соответвующие
        функции объекта класса Formatter, которые необходимо вызвать после нажатия "Apply"
        :param widget: ссылка на виджет, к которому был применен сигнал.
        """
        self.communications_of_widgets_and_settings.get(widget)(int(widget.get_value()))
        self.called_formatter_functions_for_apply.add(
            self.communications_of_widgets_and_formatter_functions[widget])


win = FormatterWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()