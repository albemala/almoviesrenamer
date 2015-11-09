from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from preferences import preferences

__author__ = "Alberto Malagoli"


class PreferencesDialog(QDialog):
    STATS_AGREE = 1
    STATS_DISAGREE = 0

    DURATION_REPRESENTATIONS = (
        QApplication.translate('PreferencesDialog', "Minutes only"),
        QApplication.translate('PreferencesDialog', "Hours and minutes"),
    )
    LANGUAGE_REPRESENTATIONS = (
        QApplication.translate('PreferencesDialog', "English name"),
        QApplication.translate('PreferencesDialog', "3-letters"),
    )
    WORDS_SEPARATORS_REPRESENTATIONS = (
        QApplication.translate('PreferencesDialog', ", (comma-space)"),
        QApplication.translate('PreferencesDialog', "- (space-dash-space)"),
        QApplication.translate('PreferencesDialog', " (space)"),
    )

    WORDS_SEPARATORS = (', ', ' - ', ' ',)

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        # load UI
        self.ui = loadUi("preferences_dialog.ui", self)
        # load settings
        # TODO
        # self.load_settings()
        ## slots connection
        self.ui.radio_agree.clicked.connect(self.stats_agreement_agree)
        self.ui.radio_disagree.clicked.connect(self.stats_agreement_disagree)
        self.ui.combo_duration.currentIndexChanged.connect(self.duration_representation_changed)
        self.ui.combo_language.currentIndexChanged.connect(self.language_representation_changed)
        self.ui.combo_words_separator.currentIndexChanged.connect(self.words_separator_representation_changed)

        self.ui.button_close.clicked.connect(self.close)

        self.ui.tab_widget.setCurrentIndex(0)

    def load_settings(self):
        """
        loads settings, and sets GUI elements according to
        user choices
        """

        # get usage statistics agreement choice
        stats_agreement = preferences.get_stats_agreement()
        # set radio buttons checked
        if stats_agreement == self.STATS_AGREE:
            self.ui.radio_agree.setChecked(True)
        else:
            self.ui.radio_disagree.setChecked(True)

        duration_representation = preferences.get_duration_representation()
        self.ui.combo_duration.setCurrentIndex(duration_representation)
        language_representation = preferences.get_language_representation()
        self.ui.combo_language.setCurrentIndex(language_representation)
        words_separator = preferences.get_words_separator()
        self.ui.combo_words_separator.setCurrentIndex(words_separator)

    def stats_agreement_agree(self, checked):
        """
        called when user clicks on radio button to agree with
        usage statistics agreement
        """

        # save value on settings file
        preferences.set_stats_agreement(True)

    def stats_agreement_disagree(self, checked):
        """
        called when user clicks on radio button to disagree with
        usage statistics agreement
        """

        # save value on settings file
        preferences.set_stats_agreement(False)

    def duration_representation_changed(self, index):
        preferences.set_duration_representation(index)

    def language_representation_changed(self, index):
        preferences.set_language_representation(index)

    def words_separator_representation_changed(self, index):
        preferences.set_words_separator(index)

    def close(self):
        # TODO
        # send_usage_statistics()
        self.accept()
