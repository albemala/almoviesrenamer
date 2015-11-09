from PyQt5.QtCore import QSettings

__author__ = "Alberto Malagoli"

_WORDS_SEPARATOR = "words_separator"
_LANGUAGE_REPRESENTATION = "language_representation"
_DURATION_REPRESENTATION = "duration_representation"
_STATS_AGREEMENT = "stats_agreement"
_RENAMING_RULE = "renaming_rule"
_FIRST_TIME_OPENING = "first_time_opening"
_LAST_VISITED_DIRECTORY = "last_visited_directory"


class Preferences:
    """

    """

    def __init__(self):
        self._preferences = QSettings("preferences.ini", QSettings.IniFormat)

    #
    # last_visited_directory
    #

    def get_last_visited_directory(self):
        return self._preferences.value(_LAST_VISITED_DIRECTORY).toString()

    def set_last_visited_directory(self, value):
        """
        Args:
            value: String
        """
        self._preferences.setValue(_LAST_VISITED_DIRECTORY, value)

    #
    # first_time_opening
    #

    def get_first_time_opening(self):
        return self._preferences.value(_FIRST_TIME_OPENING, True).toBool()

    def set_first_time_opening(self, value):
        """
        Args:
            value: Bool
        """
        self._preferences.setValue(_FIRST_TIME_OPENING, value)

    #
    # renaming_rule
    #

    def get_renaming_rule(self):
        return self._preferences.value(_RENAMING_RULE).toString()

    def set_renaming_rule(self, value):
        """
        Args:
            value: String
        """
        self._preferences.setValue(_RENAMING_RULE, value)

    #
    # stats_agreement
    #

    def get_stats_agreement(self):
        return self._preferences.value(_STATS_AGREEMENT).toBool()

    def set_stats_agreement(self, value):
        """
        Args:
            value: Bool
        """
        self._preferences.setValue(_STATS_AGREEMENT, value)

    #
    # duration_representation
    #

    def get_duration_representation(self):
        return self._preferences.value(_DURATION_REPRESENTATION).toInt()

    def set_duration_representation(self, value):
        """
        Args:
            value: Int
        """
        self._preferences.setValue(_DURATION_REPRESENTATION, value)

    #
    # language_representation
    #

    def get_language_representation(self):
        return self._preferences.value(_LANGUAGE_REPRESENTATION).toInt()

    def set_language_representation(self, value):
        """
        Args:
            value: Int
        """
        self._preferences.setValue(_LANGUAGE_REPRESENTATION, value)

    #
    # words_separator
    #

    def get_words_separator(self):
        return self._preferences.value(_WORDS_SEPARATOR).toInt()

    def set_words_separator(self, value):
        """
        Args:
            value: Int
        """
        self._preferences.setValue(_WORDS_SEPARATOR, value)


preferences = Preferences()
