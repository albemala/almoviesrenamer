from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from preferences import preferences

__author__ = "Alberto Malagoli"


class StatsAgreementDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        # load UI
        self.ui = loadUi("stats_agreement_dialog.ui", self)
        # slots connection
        self.ui.radio_agree.clicked.connect(self.stats_agreement_agree)
        self.ui.radio_disagree.clicked.connect(self.stats_agreement_disagree)

        self.ui.button_box.accepted.connect(self.close)

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


def close(self):
    self.accept()
