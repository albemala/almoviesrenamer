# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

try:
    import sip
    # using version 2 of SIP API
    sip.setapi('QString', 2)

    from PyQt4.QtCore import QTranslator, QLocale
    from PyQt4.QtGui import QApplication
    import sys
    import utils
    from gui import GUI

    # load languages and preferences
    utils.load_languages()
    utils.load_preferences()
    # create the GUI and shows it
    app = QApplication(sys.argv)
    # load translation
    translator = QTranslator()
    translator.load("qm/app_" + QLocale.system().name())
    app.installTranslator(translator)
    # show gui
    gui = GUI()
    gui.show()
    # execute the application
    app.exec_()
except:
    import traceback
    import exceptionhandler
    exceptionhandler.save_exception()
    traceback.print_exc()


