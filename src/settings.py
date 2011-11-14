# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QDialog, QListWidgetItem
from PyQt4.uic import loadUi
from movie import Movie

class SettingsDialog(QDialog):

    STATS_AGREE = 1
    STATS_DISAGREE = 0

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.ui = loadUi("settings_dialog.ui", self)
        # load settings
        self.load_settings()
        ## slots connection
        self.ui.radio_agree.clicked.connect(self.stats_agreement_agree)
        self.ui.radio_disagree.clicked.connect(self.stats_agreement_disagree)

    def load_settings(self):
        """
        populate renaming rule by rule read from settings
        """

        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        stats_agreement = self.settings.value("stats_agreement").toInt()[0]
        if stats_agreement == self.STATS_AGREE:
            self.ui.radio_agree.setChecked(True)
        else:
            self.ui.radio_disagree.setChecked(True)

    def stats_agreement_agree(self, checked):
        """
        called when renaming rule changes
        
        creates and saves new renaming rule, and generate the movie example's new name
        """

        self.settings.setValue("stats_agreement", self.STATS_AGREE)

    def stats_agreement_disagree(self, checked):
        """
        called when renaming rule changes
        
        creates and saves new renaming rule, and generate the movie example's new name
        """

        self.settings.setValue("stats_agreement", self.STATS_DISAGREE)


