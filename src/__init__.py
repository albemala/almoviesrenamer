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

    app = QApplication(sys.argv)
    gui = MainWindow()
    app.exec_()

except:
    import traceback

    # TODO
    # import exceptionhandler
    # exceptionhandler.save_exception()
    traceback.print_exc()
