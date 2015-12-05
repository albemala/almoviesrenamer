from PyQt5.QtQml import QQmlApplicationEngine


class RenamingRuleDialogView:
    def __init__(self):
        self.__engine = QQmlApplicationEngine()
        self.__engine.load("ui/renaming_rule_dialog.qml")

    def __get_root_window(self):
        return self.__engine.rootObjects()[0]

    def __get_property(self, property_name: str):
        return self.__get_root_window().property(property_name)

    def __set_property(self, property_name: str, property_value):
        return self.__get_root_window().setProperty(property_name, property_value)
