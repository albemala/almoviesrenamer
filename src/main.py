# -*- coding: latin-1 -*-

# using my excepthook
#sys.excepthook = exceptionhandler.excepthook

__author__ = "Alberto Malagoli"

import sip
# using version 2 of SIP API
sip.setapi('QString', 2)

from PyQt4.QtCore import QTranslator, QLocale
from PyQt4.QtGui import QApplication
import sys
import exceptionhandler
import utils
from gui import GUI

utils.load_languages()
utils.load_preferences()

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

