# -*- coding: latin-1 -*-

import sip
# using version 2 of SIP API
sip.setapi('QString', 2)

from gui import GUI
from PyQt4.QtCore import QTranslator, QLocale
from PyQt4.QtGui import QApplication
import sys
import exceptionhandler
import utils

__author__ = "Alberto Malagoli"

#if __name__ == "__main__":

# using my excepthook
sys.excepthook = exceptionhandler.excepthook

utils.load_languages_db()
utils.load_country_to_languages_db()

# create the GUI and shows it
app = QApplication(sys.argv)

translator = QTranslator()
translator.load("tr/app_" + QLocale.system().name())
app.installTranslator(translator)

gui = GUI()
gui.show()

exitcode = app.exec_()

# execute the application
sys.exit(exitcode)

