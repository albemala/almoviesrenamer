#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Alberto Malagoli"

try:
    import sys
    from PyQt5.QtCore import QTranslator, QLocale
    from PyQt5.QtWidgets import QApplication
    import utils
    from main_window import MainWindow

    # load languages and preferences
    utils.load_languages()
    utils.load_preferences()
    # create the GUI and shows it
    app = QApplication(sys.argv)

    # TODO
    # load translation
    # translator = QTranslator()
    # translator.load("qm/app_" + QLocale.system().name())
    # app.installTranslator(translator)

    # show gui
    gui = MainWindow()
    # execute the application
    app.exec_()
except:
    import traceback

    # import exceptionhandler
    # exceptionhandler.save_exception()
    traceback.print_exc()
