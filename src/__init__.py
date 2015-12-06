#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Alberto Malagoli"

try:
    import sys
    from PyQt5.QtWidgets import QApplication
    import utils
    from ui.main_window_controller import MainWindowController
    from ui.renaming_rule_window_view import RenamingRuleWindowView
    from ui.renaming_rule_window_controller import RenamingRuleWindowController

    # load languages and preferences
    utils.load_languages()

    app = QApplication(sys.argv)
    # main_window_controller = MainWindowController()
    view = RenamingRuleWindowController()
    app.exec_()

except:
    import traceback

    # TODO
    # import exceptionhandler
    # exceptionhandler.save_exception()
    traceback.print_exc()
