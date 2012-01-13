# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QDialog
from PyQt4.uic import loadUi

class PreferencesDialog(QDialog):

    STATS_AGREE = 1
    STATS_DISAGREE = 0

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        # load UI
        self.ui = loadUi("ui/preferences_dialog.ui", self)
        # adjust wondow size to content
        self.adjustSize()
        # load settings
        self.load_settings()
        ## slots connection
        self.ui.radio_agree.clicked.connect(self.stats_agreement_agree)
        self.ui.radio_disagree.clicked.connect(self.stats_agreement_disagree)

    def load_settings(self):
        """
        loads settings, and sets GUI elements according to 
        user choices
        """

        # load settings
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        # get usage statistics agreement choice
        stats_agreement = self.settings.value("stats_agreement").toInt()[0]
        # set radio buttons checked
        if stats_agreement == self.STATS_AGREE:
            self.ui.radio_agree.setChecked(True)
        else:
            self.ui.radio_disagree.setChecked(True)

    def stats_agreement_agree(self, checked):
        """
        called when user clicks on radio button to agree with 
        usage statistics agreement
        """

        # save value on settings file
        self.settings.setValue("stats_agreement", self.STATS_AGREE)

    def stats_agreement_disagree(self, checked):
        """
        called when user clicks on radio button to disagree with 
        usage statistics agreement
        """

        # save value on settings file
        self.settings.setValue("stats_agreement", self.STATS_DISAGREE)


