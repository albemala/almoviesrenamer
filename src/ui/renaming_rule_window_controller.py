from preferences import preferences
from ui.renaming_rule_window_view import RenamingRuleWindowView


class RenamingRuleWindowController:
    def __init__(self):
        self.__main_window = RenamingRuleWindowView()
        self.__main_window.get_rule_changed_signal().connect(self.__rule_changed)
        self.__main_window.get_remove_rule_clicked_signal().connect(self.__remove_rule)
        self.__main_window.get_remove_all_rules_clicked_signal().connect(self.__remove_all_rules)
        self.__main_window.get_add_title_clicked_signal().connect(self.__add_title)
        self.__main_window.get_add_original_title_clicked_signal().connect(self.__add_original_title)
        self.__main_window.get_add_year_clicked_signal().connect(self.__add_year)
        self.__main_window.get_add_directors_clicked_signal().connect(self.__add_directors)
        self.__main_window.get_add_duration_clicked_signal().connect(self.__add_duration)
        self.__main_window.get_add_language_clicked_signal().connect(self.__add_language)
        self.__main_window.get_add_round_brackets_clicked_signal().connect(self.__add_round_brackets)
        self.__main_window.get_add_square_brackets_clicked_signal().connect(self.__add_square_brackets)
        self.__main_window.get_add_curly_brackets_clicked_signal().connect(self.__add_curly_brackets)
        self.__main_window.get_close_clicked_signal().connect(self.__close)

    def __rule_changed(self):
        rules = self.__main_window.get_rules()
        print(rules)
        # renaming_rule = ".".join(rules)
        # preferences.set_renaming_rule(renaming_rule)

    def __remove_rule(self, index: int):
        self.__main_window.remove_rule(index)

    def __remove_all_rules(self):
        self.__main_window.remove_all_rules()

    def __add_title(self):
        self.__main_window.add_rule("Title")

    def __add_original_title(self):
        self.__main_window.add_rule("OriginalTitle")

    def __add_year(self):
        self.__main_window.add_rule("Year")

    def __add_directors(self):
        self.__main_window.add_rule("Director")

    def __add_duration(self):
        self.__main_window.add_rule("Duration")

    def __add_language(self):
        self.__main_window.add_rule("Language")

    def __add_round_brackets(self):
        self.__main_window.add_rule("(")
        self.__main_window.add_rule(")")

    def __add_square_brackets(self):
        self.__main_window.add_rule("[")
        self.__main_window.add_rule("]")

    def __add_curly_brackets(self):
        self.__main_window.add_rule("{")
        self.__main_window.add_rule("}")

    def __close(self):
        pass
