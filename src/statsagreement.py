# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QDialog
from PyQt4.uic import loadUi

class StatsAgreementDialog(QDialog):

    STATS_AGREE = 1
    STATS_DISAGREE = 0

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        # load UI
        self.ui = loadUi("stats_agreement_dialog.ui", self)
        # adjust wondow size to content
        self.adjustSize()
        # load settings
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        ## slots connection
        self.ui.radio_agree.clicked.connect(self.stats_agreement_agree)
        self.ui.radio_disagree.clicked.connect(self.stats_agreement_disagree)

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




