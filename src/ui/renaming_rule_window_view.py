from PyQt5.QtQml import QQmlApplicationEngine


class RenamingRuleWindowView:
    def __init__(self):
        self.__engine = QQmlApplicationEngine()
        self.__engine.load("ui/renaming_rule_window.qml")

    def __get_root_window(self):
        return self.__engine.rootObjects()[0]

    def __get_property(self, property_name: str):
        return self.__get_root_window().property(property_name)

    def __set_property(self, property_name: str, property_value):
        return self.__get_root_window().setProperty(property_name, property_value)

    def add_rule(self, rule: str):
        self.__get_root_window().addRule(rule)

    def remove_rule(self, index: int):
        self.__get_root_window().removeRule(index)

    def remove_all_rules(self):
        self.__get_root_window().removeAllRules()

    def get_rule_changed_signal(self):
        return self.__get_root_window().ruleChanged

    def get_remove_rule_clicked_signal(self):
        return self.__get_root_window().removeRuleClicked

    def get_remove_all_rules_clicked_signal(self):
        return self.__get_root_window().removeAllRulesClicked

    def get_add_title_clicked_signal(self):
        return self.__get_root_window().addTitleClicked

    def get_add_original_title_clicked_signal(self):
        return self.__get_root_window().addOriginalTitleClicked

    def get_add_year_clicked_signal(self):
        return self.__get_root_window().addYearClicked

    def get_add_directors_clicked_signal(self):
        return self.__get_root_window().addDirectorsClicked

    def get_add_duration_clicked_signal(self):
        return self.__get_root_window().addDurationClicked

    def get_add_language_clicked_signal(self):
        return self.__get_root_window().addLanguageClicked

    def get_add_round_brackets_clicked_signal(self):
        return self.__get_root_window().addRoundBracketsClicked

    def get_add_square_brackets_clicked_signal(self):
        return self.__get_root_window().addSquareBracketsClicked

    def get_add_curly_brackets_clicked_signal(self):
        return self.__get_root_window().addCurlyBracketsClicked

    def get_close_clicked_signal(self):
        return self.__get_root_window().closeClicked
