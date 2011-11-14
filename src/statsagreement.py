# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QDialog, QListWidgetItem
from PyQt4.uic import loadUi
from movie import Movie

class StatsAgreementDialog(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.ui = loadUi("stats_agreement_dialog.ui", self)
        # load settings
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
#        self.renaming_rule = self.settings.value("renaming_rule").toString()
#        # creates an example movie, used to test the renaming rule
#        self.example_movie = Movie()
#
#        self.populate_list_renaming_rule()
#        ## slots connection
#        self.ui.list_renaming_rule.model().rowsInserted.connect(self.rule_changed)
#        self.ui.list_renaming_rule.model().rowsRemoved.connect(self.rule_changed)
#
#        self.ui.button_remove_rule.clicked.connect(self.remove_rule)
#        self.ui.button_clean_rule.clicked.connect(self.clean_rule)
#
#        self.ui.button_add_title.clicked.connect(self.add_title)
#        self.ui.button_add_canonical_title.clicked.connect(self.add_canonical_title)
#        self.ui.button_add_aka.clicked.connect(self.add_aka)
#        self.ui.button_add_year.clicked.connect(self.add_year)
#        self.ui.button_add_director.clicked.connect(self.add_director)
#        self.ui.button_add_runtime.clicked.connect(self.add_runtime)
#        self.ui.button_add_language.clicked.connect(self.add_language)
#
#        self.ui.button_add_round_brackets.clicked.connect(self.add_round_brackets)
#        self.ui.button_add_square_brackets.clicked.connect(self.add_square_brackets)
#        self.ui.button_add_curly_brackets.clicked.connect(self.add_curly_brackets)

    def populate_list_renaming_rule(self):
        """
        populate renaming rule by rule read from settings
        """

        # split rule
        rules = self.renaming_rule.split('.')
        # if rule is empty, reset it to 'title'
        if rules[0] == '':
            rules[0] = Movie.TITLE
            self.renaming_rule = Movie.TITLE
            self.settings.setValue("renaming_rule", self.renaming_rule)
        # loop on rules
        for rule in rules:
            # creates an item with current rule
            item = QListWidgetItem(self.ui.list_renaming_rule, self.RULES_KEY_INDEX[rule])
            # add it to rule list
            item.setText(self.RULES_KEY_TEXT[rule])
        # generate new name for example movie
        example_movie_new_name = self.example_movie.generate_new_name(self.renaming_rule)
        # show it on label
        self.ui.label_example_movie_name.setText(example_movie_new_name)

    def rule_changed(self, parent = None, start = None, end = None):
        """
        called when renaming rule changes
        
        creates and saves new renaming rule, and generate the movie example's new name
        """

        rule = []
        # if rule not empty
        if self.ui.list_renaming_rule.count() != 0:
            #generate new rule
            # loop on rule list
            for i in range(self.ui.list_renaming_rule.count()):
                # get rule item
                item = self.ui.list_renaming_rule.item(i)
                # when an item is moved inside the list_renaming_rule, firstly 
                # a new empty item is inserted into the destination location, then 
                # the item from source location is deleted. that function is called 
                # for both events (insertion and deletion), and when is called for
                # the insertion event after a list items move, the list contains an empty item,
                # which is a kind of error. 
                if item.text() == '':
                    return
                # get corresponding rule from rule item text
                rule.append(self.RULES_TEXT_KEY[item.text()])
        # creates renaming rule
        self.renaming_rule = '.'.join(rule)
        #save renaming rule on settings
        self.settings.setValue("renaming_rule", self.renaming_rule)
        #update example movie
        example_movie_new_name = self.example_movie.generate_new_name(self.renaming_rule)
        self.ui.label_example_movie_name.setText(example_movie_new_name)

    def remove_rule(self):
        """
        removes selected rule
        """

        # get selected rule
        current_item = self.ui.list_renaming_rule.currentItem()
        # remove it from list
        row = self.ui.list_renaming_rule.row(current_item)
        self.ui.list_renaming_rule.takeItem(row)

    def clean_rule(self):
        """
        cleans rule (remove all renaming rules)
        """

        self.ui.list_renaming_rule.clear()
        # needs to call rule_changed because clear() doesn't 
        # throw any signal
        self.rule_changed()

    def add_title(self):
        """
        add title to rule
        """

        item = QListWidgetItem()
        item.setText(self.RULES_INDEX_TEXT[self.TITLE])
        self.ui.list_renaming_rule.addItem(item)

    def add_canonical_title(self):
        """
        add canonical title to rule
        """

        item = QListWidgetItem()
        item.setText(self.RULES_INDEX_TEXT[self.CANONICAL_TITLE])
        self.ui.list_renaming_rule.addItem(item)

    def add_aka(self):
        """
        add aka to rule
        """

        item = QListWidgetItem()
        item.setText(self.RULES_INDEX_TEXT[self.AKAS])
        self.ui.list_renaming_rule.addItem(item)

    def add_year(self):
        """
        add year to rule
        """

        item = QListWidgetItem()
        item.setText(self.RULES_INDEX_TEXT[self.YEAR])
        self.ui.list_renaming_rule.addItem(item)

    def add_director(self):
        """
        add director to rule
        """

        item = QListWidgetItem()
        item.setText(self.RULES_INDEX_TEXT[self.DIRECTOR])
        self.ui.list_renaming_rule.addItem(item)

    def add_runtime(self):
        """
        add runtime to rule
        """

        item = QListWidgetItem()
        item.setText(self.RULES_INDEX_TEXT[self.RUNTIMES])
        self.ui.list_renaming_rule.addItem(item)

    def add_language(self):
        """
        add language to rule
        """

        item = QListWidgetItem()
        item.setText(self.RULES_INDEX_TEXT[self.LANGUAGE])
        self.ui.list_renaming_rule.addItem(item)

    def add_round_brackets(self):
        """
        add opened and closed round brackets to rule
        """

        item1 = QListWidgetItem()
        item1.setText(self.RULES_INDEX_TEXT[self.OPENED_ROUND_BRACKET])
        self.ui.list_renaming_rule.addItem(item1)

        item2 = QListWidgetItem()
        item2.setText(self.RULES_INDEX_TEXT[self.CLOSED_ROUND_BRACKET])
        self.ui.list_renaming_rule.addItem(item2)

    def add_square_brackets(self):
        """
        add opened and closed square brackets to rule
        """

        item1 = QListWidgetItem()
        item1.setText(self.RULES_INDEX_TEXT[self.OPENED_SQUARE_BRACKET])
        self.ui.list_renaming_rule.addItem(item1)

        item2 = QListWidgetItem()
        item2.setText(self.RULES_INDEX_TEXT[self.CLOSED_SQUARE_BRACKET])
        self.ui.list_renaming_rule.addItem(item2)

    def add_curly_brackets(self):
        """
        add opened and closed curly brackets to rule
        """

        item1 = QListWidgetItem()
        item1.setText(self.RULES_INDEX_TEXT[self.OPENED_CURLY_BRACKET])
        self.ui.list_renaming_rule.addItem(item1)

        item2 = QListWidgetItem()
        item2.setText(self.RULES_INDEX_TEXT[self.CLOSED_CURLY_BRACKET])
        self.ui.list_renaming_rule.addItem(item2)



