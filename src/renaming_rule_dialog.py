from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from movie import Movie
from preferences import preferences
from preferences_dialog import PreferencesDialog

__author__ = "Alberto Malagoli"


class RenamingRuleDialog(QDialog):
    TITLE = QApplication.translate('RenamingRuleDialog', "Title")
    ORIGINAL_TITLE = QApplication.translate('RenamingRuleDialog', "Original title")
    YEAR = QApplication.translate('RenamingRuleDialog', "Year")
    DIRECTOR = QApplication.translate('RenamingRuleDialog', "Director")
    DURATION = QApplication.translate('RenamingRuleDialog', "Duration")
    LANGUAGE = QApplication.translate('RenamingRuleDialog', "Language")
    OPENED_ROUND_BRACKET = "("
    CLOSED_ROUND_BRACKET = ")"
    OPENED_SQUARE_BRACKET = "["
    CLOSED_SQUARE_BRACKET = "]"
    OPENED_CURLY_BRACKET = "{"
    CLOSED_CURLY_BRACKET = "}"

    RENAMING_TO_VISUAL_RULE = {
        Movie.TITLE: TITLE,
        Movie.ORIGINAL_TITLE: ORIGINAL_TITLE,
        Movie.YEAR: YEAR,
        Movie.DIRECTOR: DIRECTOR,
        Movie.DURATION: DURATION,
        Movie.LANGUAGE: LANGUAGE,
        OPENED_ROUND_BRACKET: OPENED_ROUND_BRACKET,
        CLOSED_ROUND_BRACKET: CLOSED_ROUND_BRACKET,
        OPENED_SQUARE_BRACKET: OPENED_SQUARE_BRACKET,
        CLOSED_SQUARE_BRACKET: CLOSED_SQUARE_BRACKET,
        OPENED_CURLY_BRACKET: OPENED_CURLY_BRACKET,
        CLOSED_CURLY_BRACKET: CLOSED_CURLY_BRACKET
    }

    VISUAL_TO_RENAMING_RULE = {
        TITLE: Movie.TITLE,
        ORIGINAL_TITLE: Movie.ORIGINAL_TITLE,
        YEAR: Movie.YEAR,
        DIRECTOR: Movie.DIRECTOR,
        DURATION: Movie.DURATION,
        LANGUAGE: Movie.LANGUAGE,
        OPENED_ROUND_BRACKET: OPENED_ROUND_BRACKET,
        CLOSED_ROUND_BRACKET: CLOSED_ROUND_BRACKET,
        OPENED_SQUARE_BRACKET: OPENED_SQUARE_BRACKET,
        CLOSED_SQUARE_BRACKET: CLOSED_SQUARE_BRACKET,
        OPENED_CURLY_BRACKET: OPENED_CURLY_BRACKET,
        CLOSED_CURLY_BRACKET: CLOSED_CURLY_BRACKET
    }

    def __init__(self, parent, preferences_dialog):
        QDialog.__init__(self, parent)

        self.ui = loadUi("renaming_rule_dialog.ui", self)

        self.ui.preferences_dialog = preferences_dialog

        # creates an example movie, used to test the renaming rule
        self.example_movie = Movie()

        # TODO
        # self.populate_list_visual_rule()
        # self.update_representations()
        # TODO
        # renaming_rule = utils.preferences.value("renaming_rule").toString()
        # self.update_example_movie(renaming_rule)

        ## slots connection
        self.ui.list_visual_rule.model().rowsInserted.connect(self.rule_changed)
        self.ui.list_visual_rule.model().rowsRemoved.connect(self.rule_changed)

        self.ui.button_remove_rule.clicked.connect(self.remove_rule)
        self.ui.button_clean_rule.clicked.connect(self.clean_rule)

        self.ui.button_add_title.clicked.connect(self.add_title)
        self.ui.button_add_original_title.clicked.connect(self.add_original_title)
        self.ui.button_add_year.clicked.connect(self.add_year)
        self.ui.button_add_director.clicked.connect(self.add_director)
        self.ui.button_add_duration.clicked.connect(self.add_duration)
        self.ui.button_add_language.clicked.connect(self.add_language)

        self.ui.button_add_round_brackets.clicked.connect(self.add_round_brackets)
        self.ui.button_add_square_brackets.clicked.connect(self.add_square_brackets)
        self.ui.button_add_curly_brackets.clicked.connect(self.add_curly_brackets)

        self.ui.button_show_preferences.clicked.connect(self.show_preferences)

        self.ui.button_close.clicked.connect(self.close)

    def populate_list_visual_rule(self):
        """
        populate renaming rule by rule read from settings
        """

        renaming_rule = preferences.get_renaming_rule()
        # split rule
        rules = renaming_rule.split('.')
        # if rule is empty, reset it to 'title'
        if rules[0] == '':
            rules[0] = Movie.TITLE
            renaming_rule = Movie.TITLE
            preferences.set_renaming_rule(renaming_rule)
        visual_rule = []
        # loop on rules
        for rule in rules:
            visual_rule.append(self.RENAMING_TO_VISUAL_RULE[rule])
        self.ui.list_visual_rule.addItems(visual_rule)

    def update_representations(self):
        duration_index = preferences.get_duration_representation()
        duration_representation = PreferencesDialog.DURATION_REPRESENTATIONS[duration_index]
        self.ui.label_duration_representation.setText(duration_representation)

        language_index = preferences.get_language_representation()
        language_representation = PreferencesDialog.LANGUAGE_REPRESENTATIONS[language_index]
        self.ui.label_language_representation.setText(language_representation)

        separator_index = preferences.get_words_separator()
        separator_representation = PreferencesDialog.WORDS_SEPARATORS_REPRESENTATIONS[separator_index]
        self.ui.label_separator_representation.setText(separator_representation)

    def update_example_movie(self, renaming_rule):
        # generate new name for example movie
        example_movie_new_name = self.example_movie.generate_new_name(renaming_rule)
        # show it on label
        self.ui.label_example_movie_name.setText(example_movie_new_name)

    def rule_changed(self, parent=None, start=None, end=None):
        """
        called when renaming rule changes

        creates and saves new renaming rule, and generate the movie example's new name
        """

        rule = []
        for index in range(self.ui.list_visual_rule.count()):
            text = self.ui.list_visual_rule.item(index).text()
            # when an item is moved inside the list_visual_rule, firstly
            # a new empty item is inserted into the destination location, then
            # the item from source location is deleted. that function is called
            # for both events (insertion and deletion), and when is called for
            # the insertion event after a list items move, the list contains an empty item,
            # which is a kind of error.
            if text != '':
                rule.append(self.VISUAL_TO_RENAMING_RULE[text])
        # creates renaming rule
        renaming_rule = '.'.join(rule)
        # save renaming rule on settings
        preferences.set_renaming_rule(renaming_rule)
        # update example movie
        self.update_example_movie(renaming_rule)

    def remove_rule(self):
        """
        removes selected rule
        """

        # get selected items in rule
        selected_items = self.ui.list_visual_rule.selectedItems()
        # remove its from list
        for item in reversed(selected_items):
            row = self.ui.list_visual_rule.row(item)
            self.ui.list_visual_rule.takeItem(row)

    def clean_rule(self):
        """
        cleans rule (remove all renaming rules)
        """

        self.ui.list_visual_rule.clear()
        # needs to call rule_changed because clear() doesn't
        # throw any signal
        self.rule_changed()

    def add_title(self):
        """
        add title to rule
        """

        self.ui.list_visual_rule.addItem(self.TITLE)

    def add_original_title(self):
        """
        add aka to rule
        """

        self.ui.list_visual_rule.addItem(self.ORIGINAL_TITLE)

    def add_year(self):
        """
        add year to rule
        """

        self.ui.list_visual_rule.addItem(self.YEAR)

    def add_director(self):
        """
        add director to rule
        """

        self.ui.list_visual_rule.addItem(self.DIRECTOR)

    def add_duration(self):
        """
        add runtime to rule
        """

        self.ui.list_visual_rule.addItem(self.DURATION)

    def add_language(self):
        """
        add language to rule
        """

        self.ui.list_visual_rule.addItem(self.LANGUAGE)

    def add_round_brackets(self):
        """
        add opened and closed round brackets to rule
        """

        self.ui.list_visual_rule.addItem(self.OPENED_ROUND_BRACKET)
        self.ui.list_visual_rule.addItem(self.CLOSED_ROUND_BRACKET)

    def add_square_brackets(self):
        """
        add opened and closed square brackets to rule
        """

        self.ui.list_visual_rule.addItem(self.OPENED_SQUARE_BRACKET)
        self.ui.list_visual_rule.addItem(self.CLOSED_SQUARE_BRACKET)

    def add_curly_brackets(self):
        """
        add opened and closed curly brackets to rule
        """

        self.ui.list_visual_rule.addItem(self.OPENED_CURLY_BRACKET)
        self.ui.list_visual_rule.addItem(self.CLOSED_CURLY_BRACKET)

    def show_preferences(self):
        self.ui.preferences_dialog.exec_()
        # TODO
        # renaming_rule = utils.preferences.value("renaming_rule").toString()
        # self.update_representations()
        # update example movie
        # self.update_example_movie(renaming_rule)

    def close(self):
        # TODO
        # send_usage_statistics()
        self.accept()
