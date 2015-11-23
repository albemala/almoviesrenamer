from PyQt5.QtCore import QSettings

__author__ = "Alberto Malagoli"


class Preferences:
    """

    """

    DURATION_REPRESENTATION_MINUTES = 0
    DURATION_REPRESENTATION_HOURS_MINUTES = 1

    __WORDS_SEPARATOR = "words_separator"
    __LANGUAGE_REPRESENTATION = "language_representation"
    __DURATION_REPRESENTATION = "duration_representation"
    __STATS_AGREEMENT = "stats_agreement"
    __RENAMING_RULE = "renaming_rule"
    __FIRST_TIME_OPENING = "first_time_opening"
    __LAST_VISITED_DIRECTORY = "last_visited_directory"

    def __init__(self):
        self.__preferences = QSettings("preferences.ini", QSettings.IniFormat)

    #
    # last_visited_directory
    #

    def get_last_visited_directory(self) -> str:
        return self.__preferences.value(Preferences.__LAST_VISITED_DIRECTORY, "")

    def set_last_visited_directory(self, value: str):
        self.__preferences.setValue(Preferences.__LAST_VISITED_DIRECTORY, value)

    #
    # first_time_opening
    #

    def get_first_time_opening(self) -> bool:
        return self.__preferences.value(Preferences.__FIRST_TIME_OPENING, True).toBool()

    def set_first_time_opening(self, value: bool):
        self.__preferences.setValue(Preferences.__FIRST_TIME_OPENING, value)

    #
    # renaming_rule
    #

    def get_renaming_rule(self) -> str:
        return self.__preferences.value(Preferences.__RENAMING_RULE, "")

    def set_renaming_rule(self, value: str):
        self.__preferences.setValue(Preferences.__RENAMING_RULE, value)

    #
    # stats_agreement
    #

    def get_stats_agreement(self) -> bool:
        return self.__preferences.value(Preferences.__STATS_AGREEMENT, False).toBool()

    def set_stats_agreement(self, value: bool):
        self.__preferences.setValue(Preferences.__STATS_AGREEMENT, value)

    #
    # duration_representation
    #

    def get_duration_representation(self) -> int:
        return self.__preferences.value(Preferences.__DURATION_REPRESENTATION, 0)

    def set_duration_representation(self, value: int):
        self.__preferences.setValue(Preferences.__DURATION_REPRESENTATION, value)

    #
    # language_representation
    #

    def get_language_representation(self) -> int:
        return self.__preferences.value(Preferences.__LANGUAGE_REPRESENTATION, 0).toInt()

    def set_language_representation(self, value: int):
        self.__preferences.setValue(Preferences.__LANGUAGE_REPRESENTATION, value)

    #
    # words_separator
    #

    def get_words_separator(self) -> int:
        return self.__preferences.value(Preferences.__WORDS_SEPARATOR, 0).toInt()

    def set_words_separator(self, value: int):
        self.__preferences.setValue(Preferences.__WORDS_SEPARATOR, value)


preferences = Preferences()
