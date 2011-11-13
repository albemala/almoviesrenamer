# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

import sip
# using version 2 of SIP API
sip.setapi('QString', 2)

from gui import GUI
from PyQt4.QtCore import QTranslator, QLocale
from PyQt4.QtGui import QApplication
import sys
import exceptionhandler

if __name__ == "__main__":

    # using my excepthook
    sys.excepthook = exceptionhandler.excepthook

    # create the GUI and shows it
    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load("app_" + QLocale.system().name())
    app.installTranslator(translator)

    gui = GUI()
    gui.show()

    exitcode = app.exec_()

    # execute the application
    sys.exit(exitcode)

