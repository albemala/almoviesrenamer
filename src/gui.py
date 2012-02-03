# -*- coding: latin-1 -*-

from PyQt4.QtCore import PYQT_VERSION_STR, QSettings, Qt, pyqtSignal
from PyQt4.QtGui import QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, \
    QBrush, QPixmap
from PyQt4.uic import loadUi
from movie import Movie
from renamingrule import RenamingRuleDialog
from settings import SettingsDialog
from statsagreement import StatsAgreementDialog
import imdb
import os.path
import sys
import threading
import urllib
import utils

__author__ = "Alberto Malagoli"

class GUI(QMainWindow):

    VIDEO_EXTENSIONS = [".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", \
                        ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", \
                        ".rm", ".swf", ".vob", ".wmv"]

    load_movies_finished = pyqtSignal()
    search_title_finished = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)

        # check internet connection
        self.check_connection()
        # check for new program version
#        self.check_new_version()

        ## variables
        # load settings
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        # get renaming rule from settings
        self.renaming_rule = self.settings.value("renaming_rule").toString()
        # get last visited directory from settings
        self.last_visited_directory = self.settings.value("last_visited_directory").toString()
        # stores movies objects
        self.movies = []
        # stores current (selected) movie
        self.current_movie = None

        # show stats agreement dialog
        self.show_stats_agreement()

        # load GUI
        self.ui = loadUi("ui/main_window.ui", self)
        # create RenamingRuleDialog
#        self.ui.renaming_rule_dialog = RenamingRuleDialog(self)
        # create SettingsDialog
#        self.ui.preferences_dialog = SettingsDialog(self)
        # set some GUI parameters
        self.setWindowTitle(utils.PROGRAM_NAME)
        self.ui.panel_loading.setVisible(False)
        self.ui.stack_movie.setVisible(False)
        self.ui.table_movies.resizeColumnToContents(0)
        # adjust wondow size to content
        self.adjustSize()

        ## signals connection
        # MENU Movies
        self.ui.action_add_movies.triggered.connect(self.add_movies)
        self.ui.action_add_all_movies_in_folder.triggered.connect(self.add_movies_in_folder)
        self.ui.action_add_all_movies_in_folder_subfolders.triggered.connect(self.add_movies_in_folder_subfolders)
        self.ui.action_remove_selected_movies.triggered.connect(self.remove_selected_movies)
        self.ui.action_remove_all_movies.triggered.connect(self.remove_all_movies)
        self.ui.action_change_renaming_rule.triggered.connect(self.change_renaming_rule)
        self.ui.action_rename_movies.triggered.connect(self.rename_movies)
        self.load_movies_finished.connect(self.load_movies_end)
        self.ui.text_search_title.returnPressed.connect(self.search_new_title)
        self.ui.button_search_title.clicked.connect(self.search_new_title)
        self.search_title_finished.connect(self.search_title_end)
        # MENU Settings
        self.ui.action_preferences.triggered.connect(self.show_preferences)
        # MENU ?
        self.ui.action_about.triggered.connect(self.show_about)
        # TABLE movies
        self.ui.table_movies.itemSelectionChanged.connect(self.movies_selection_changed)
        # STACK movie
        self.ui.button_change_movie.toggled.connect(self.change_movie)
        self.ui.table_alternative_movies.itemSelectionChanged.connect(self.alternative_movies_selection_changed)

        #XXX da togliere
        # create a new movie object
        movie = Movie(None)
        self.movies.append(movie)
        # insert a new row in movie table
        self.ui.table_movies.insertRow(self.ui.table_movies.rowCount())
        # create a table item with original movie file name
        item_original_name = QTableWidgetItem(movie.original_name())
        self.ui.table_movies.setItem(self.ui.table_movies.rowCount() - 1, 0, item_original_name)

    def check_connection(self):
        """
        checks if internet connection is up.
        
        if internet connection is down, notifies the user with a message.
        """

        try:
            # try to open a web URL
            f = urllib.urlopen("http://almoviesrenamer.appspot.com/rulestats")
        except Exception:
            # if an error occurs, notify the user with a message
            msg_box = QMessageBox()
            msg_box.setWindowTitle(self.tr("Internet connection down?"))
            msg_box.setText(self.tr("""
            <p>
                It seems your internet connection is down
                (but maybe I'm wrong).
            </p>
            <p>
                That program needs access to the internet, 
                to get information about movies, 
                so please check your connection.
            </p>
            <p>
                If I'm wrong, sorry for the interruption...
            </p>
            """))
            icon = QPixmap()
            icon.load('ui/icons/exclamation.png')
            msg_box.setIconPixmap(icon)
            msg_box.exec_()

    def check_new_version(self):
        """
        checks for new program version, and notify in case of
        a newer version
        """

        # create url, with current program version
        url = "http://almoviesrenamer.appspot.com/checknewversion?version=" + \
              utils.PROGRAM_VERSION
        # call web service
        f = urllib.urlopen(url)
        # read the answer (could be "yes" for new version, or "no")
        answer = f.read()
        # if there is a new version
        if answer[:-1] == "new":
            title = self.tr("New version available")
            msg = self.tr("""
            <p>
                A new version of {0} is available! 
            </p>
            <p>
                <a href="http://code.google.com/p/almoviesrenamer/downloads/list">
                    Download it.
                </a>
            </p>
            """).format(utils.PROGRAM_NAME)
            # show a notification dialog, with link to download page
            QMessageBox.information(None, title, msg)

    def show_stats_agreement(self):
        """
        shows usage statistics agreement dialog
        """

        # get if this is the first time user opens the program
        first_time = self.settings.value("first_time").toBool()
        if first_time:
            # create agreement dialog
            stats_agreement_dialog = StatsAgreementDialog(self)
            # show it
            stats_agreement_dialog.exec_()
            # send usage statistics
            self.send_usage_statistics()
            # nex time user will open the program, don't show that dialog
            self.settings.setValue("first_time", False)

    def send_usage_statistics(self):
        """
        checks user choice about sending usage statistics and
        sends usage statistics to a dedicated web service
        """

        # get user choice about sending usage statistics
        send_usage_statistics = self.settings.value("stats_agreement").toInt()[0]
        # if user chose to send usage statistics
        if send_usage_statistics == SettingsDialog.STATS_AGREE:
            # start sending thread
            threading.Thread(target = self.send_usage_statistics_run).start()

    def send_usage_statistics_run(self):
        """
        sends usage statistics to a dedicated web service
        """

        # get renaming rule from settings
        renaming_rule = self.settings.value("renaming_rule").toString()
        # creates url, using renaming rule
        url = "http://almoviesrenamer.appspot.com/rulestats?addrule=" + renaming_rule
        # call web service
        f = urllib.urlopen(url)

    #--------------------------------- SLOTS ----------------------------------

    # MENU Movies

    def add_movies(self):
        """
        select video files from file system using a FileDialog, 
        then creates corresponding movie objects
        
        these movies will populate movie table
        
        get information from selected files
        """

        # create a filter, only video files can be selected
        video_filter = self.tr("Video (*") + ' *'.join(self.VIDEO_EXTENSIONS) + ")"
        # dialog title
        title = self.tr("Select movies you want to rename...")
        # select video files from file system
        filepaths = QFileDialog.getOpenFileNames(self, title, self.last_visited_directory, video_filter)
        # if at least one file has been selected
        if len(filepaths) > 0:
            self.load_movies(filepaths)

    def add_movies_in_folder(self):
        """
        select all video files from a selected folder using a FileDialog, 
        then creates corresponding movie objects
        
        these movies will populate movie table
        
        get information from selected files
        """

        # dialog title
        title = self.tr("Select a folder containing movies...")
        # select folder from file system
        dirpath = QFileDialog.getExistingDirectory(self, title, self.last_visited_directory)
        # if a directory has been selected
        if dirpath != '':
            filepaths = []
            # for each entry (files + folders) in selected folder
            for entry in os.listdir(dirpath):
                entry = os.path.join(dirpath, entry)
                # select only video files
                extension = os.path.splitext(entry)[1].lower()
                if os.path.isfile(entry) and extension in self.VIDEO_EXTENSIONS:
                    # save entry with path
                    filepaths.append(entry)

            self.load_movies(filepaths)

    def add_movies_in_folder_subfolders(self):
        """
        select all video files from a selected folder and subfolders using a FileDialog, 
        then creates corresponding movie objects
        
        these movies will populate movie table
        
        get information from selected files
        """

        # dialog title
        title = self.tr("Select a folder containing movies...")
        # select folder from file system
        dirpath = QFileDialog.getExistingDirectory(self, title, self.last_visited_directory)
        # if a directory has been selected
        if dirpath != '':
            filepaths = []
            # walk on chosen directory, and loop on files and directories
            for root, dirs, files in os.walk(dirpath):
                # for each file
                for name in files:
                    entry = os.path.join(root, name)
                    # select only video files
                    extension = os.path.splitext(name)[1].lower()
                    if extension in self.VIDEO_EXTENSIONS:
                        # save entry with path
                        filepaths.append(entry)

            self.load_movies(filepaths)

    def load_movies(self, filepaths):
        """
        given a list of file paths, creates a movie object for each
        file, get info from it, and populate movies table
        """

        # takes first selected file and get the file path, use it as the last visited directory
        self.last_visited_directory = os.path.normpath(os.path.split(filepaths[0])[0])
        # save it in settings
        self.settings.setValue("last_visited_directory", self.last_visited_directory)
        # disable gui elements which cannot be used during loading
        self.set_gui_enabled_load_movies(False)
        # show loading panel
        self.ui.panel_loading.setVisible(True)
        # start loading thread
        threading.Thread(target = self.load_movies_run, args = (filepaths,)).start()

    def load_movies_run(self, filepaths):
        # loop on file paths
        for filepath in filepaths:
            # set loading label text, show current file name
            self.ui.label_loading.setText(self.tr("Getting information from ")\
                                           + os.path.split(filepath)[1])
            # create a new movie object
            movie = Movie(filepath)
            # generate new movie name based on renaming rule
#            movie.generate_new_name(self.renaming_rule)
            # add movie to list
            self.movies.append(movie)
            # insert a new row in movie table
            self.ui.table_movies.insertRow(self.ui.table_movies.rowCount())
            # create a table item with original movie file name
            item_original_name = QTableWidgetItem(movie.original_name())
            self.ui.table_movies.setItem(self.ui.table_movies.rowCount() - 1, 0, item_original_name)
            # create a table item with new movie file name
#            item_new_name = QTableWidgetItem(movie.new_name())
#            self.ui.table_movies.setItem(self.ui.table_movies.rowCount() - 1, 1, item_new_name)
        self.load_movies_finished.emit()

    def load_movies_end(self):
        # re-enable gui elements
        self.set_gui_enabled_load_movies(True)
        # auto resize table columns
        self.ui.table_movies.resizeColumnToContents(0)
        # hide loading panel
        self.ui.panel_loading.setVisible(False)

    def set_gui_enabled_load_movies(self, enabled):
        # set enabled property on actions
        self.ui.action_add_movies.setEnabled(enabled)
        self.ui.action_add_all_movies_in_folder.setEnabled(enabled)
        self.ui.action_add_all_movies_in_folder_subfolders.setEnabled(enabled)
        self.ui.action_remove_selected_movies.setEnabled(enabled)
        self.ui.action_remove_all_movies.setEnabled(enabled)
        self.ui.action_change_renaming_rule.setEnabled(enabled)
        self.ui.action_rename_movies.setEnabled(enabled)
        self.ui.action_preferences.setEnabled(enabled)
        if enabled == False:
            # clear table selection (and hide movie panel, if visible)
            self.ui.table_movies.selectionModel().clear()
        # set enabled property on table
        self.ui.table_movies.setEnabled(enabled)

    def remove_selected_movies(self):
        """
        removes selected movies from movies table
        """

        # get selected items
        selected_items = self.ui.table_movies.selectedItems()
        # loop on items
        for item in reversed(selected_items):
            # get item row
            row = item.row()
            # first remove items from table
            self.ui.table_movies.takeItem(row, 0)
            self.ui.table_movies.takeItem(row, 1)
            # them remove corresponding row
            self.ui.table_movies.removeRow(row)
            # delete movie item
            del self.movies[row]

    def remove_all_movies(self):
        """
        removes all movies from movies table
        """

        del self.movies[:]
        # clear table contents
        self.ui.table_movies.clearContents()
        # remove all rows
        self.ui.table_movies.setRowCount(0)

    def change_renaming_rule(self):
        """
        show renaming rule dialog
        """

        #show renaming rule dialog
        self.ui.renaming_rule_dialog.exec_()
        # when dialog is closed, save new rule on settings
        self.renaming_rule = self.settings.value("renaming_rule").toString()
        self.send_usage_statistics()
        # loop on movies
        for i in range(len(self.movies)):
            movie = self.movies[i]
            # generate new movie name based on new renaming rule
            movie.generate_new_name(self.renaming_rule)
            # set "before renaming state", because after renaming a movie
            # can be renamed a second time, after having changed the rule
            movie.state = Movie.STATE_BEFORE_RENAMING #XXX da cambiare col metodo set_state
            self.ui.table_movies.item(i, 1).setForeground(QBrush(Qt.black))
            self.ui.table_movies.item(i, 1).setText(movie.new_name)

        self.movies_selection_changed()

    def rename_movies(self):
        """
        rename files with new name
        """

        # loop on movies
        for i in range(len(self.movies)):
            movie = self.movies[i]
            # check if new title is a valid file name
            if movie.check_and_clean_new_name():
                # set "new name" table item with new movie name
                self.ui.table_movies.item(i, 1).setText(movie.new_name)
                try:
                    # rename file
                    os.rename(movie.get_abs_original_name(), movie.get_abs_new_name())
                except OSError as e:
                    # set state and renaming error
                    movie.set_state(Movie.STATE_RENAMING_ERROR, e.strerror)
                    # paint "new name" table item with red
                    self.ui.table_movies.item(i, 1).setForeground(QBrush(Qt.red))
                else:
                    # correclty renamed
                    movie.set_state(Movie.STATE_RENAMED)
                    # set "original name" table item with new movie name
                    self.ui.table_movies.item(i, 0).setText(movie.new_name)
                    # paint "new name" table item with green
                    self.ui.table_movies.item(i, 1).setForeground(QBrush(Qt.darkGreen))
        # if a table item is selected, update panel
        self.movies_selection_changed()

    # MENU Program

    def show_preferences(self):
        #show renaming rule dialog
        self.ui.preferences_dialog.exec_()
        self.send_usage_statistics()

    def show_about(self):
        """
        shows an about dialog, with info on program
        """

        # message shown on about dialog
        msg = self.tr("""
        <p>
            <b>{0}</b>
        </p>
        <p>
            Version: {1}<br />
            License: GNU General Public License version 3 (GPLv3)
        </p>
        <p>
            Programmed by: Alberto Malagoli<br />
            Email: <a href="mailto:albemala@gmail.com">albemala@gmail.com</a>
        </p>
        <p>
            Libraries:
            <ul>
                <li>Python: {2}</li>
                <li>PyQt: {3}</li>
                <li>IMDbPY: {4}</li>
                <li>cx-Freeze: 4.2.3</li>
            </ul>
        </p>
        <p>
            Thanks to:
            <ul>
                <li><a href="http://www.riverbankcomputing.co.uk/software/pyqt/download">PyQt</a></li>
                <li><a href="http://imdbpy.sourceforge.net/">IMDbPY</a></li>
                
                <li><a href="http://file-folder-ren.sourceforge.net/">M\xe9tamorphose</a>
                    for some stolen code</li>
                <li><a href="http://eric-ide.python-projects.org/">Eric IDE</a>
                    for code in <i>excepthook</i> function (exceptionhandler.py file)</li>

                <li><a href="http://p.yusukekamiyamane.com/">Yusuke Kamiyamane</a>
                    for Fugue Icons</li>
            </ul>
        </p>
        """).format(utils.PROGRAM_NAME, utils.PROGRAM_VERSION, sys.version.split()[0], PYQT_VERSION_STR, imdb.VERSION)
        # show the about dialog
        QMessageBox.about(self, self.tr("About {0}").format(utils.PROGRAM_NAME), msg)

    # TABLE movies

    def movies_selection_changed(self):
        """
        called when selection in table_movies changes, i.e. user selects
        different movies from previously selected ones.
        """

        selected_items = self.ui.table_movies.selectedItems()
        # no movies selected
        if len(selected_items) == 0:
            # hide movie panel
            self.ui.stack_movie.setVisible(False)
        else:
            # store first selected movie
            index = selected_items[0].row()
            self.current_movie = self.movies[index]
            movie = self.current_movie

            # set movie panel based on movie state (
            self.ui.stack_movie.setCurrentIndex(movie.state())
            # populate movie panel
            if movie.state() == Movie.STATE_RENAMING_ERROR:
                self.ui.label_error.setText(movie.renaming_error)
            elif movie.state() == Movie.STATE_BEFORE_RENAMING:
                self.populate_movie_panel()
                self.ui.stack_search_title.setCurrentIndex(0)
                self.ui.text_search_title.clear()

            self.ui.button_change_movie.setChecked(False)

            # set panel visible
            self.ui.stack_movie.setVisible(True)
            self.ui.adjustSize()

    def populate_movie_panel(self):
        movie = self.current_movie

        self.ui.label_title.setText(movie.title())
        self.ui.label_original_title.setText(movie.original_title())
        self.ui.label_year.setText(movie.year())
        self.ui.label_director.setText(movie.director())
        self.ui.label_duration.setText(movie.duration())
        self.ui.label_language.setText(movie.language())

        # clear table contents
        self.ui.table_alternative_movies.clearContents()
        # remove all rows
        self.ui.table_alternative_movies.setRowCount(0)
        for alternative_movie in movie.alternative_movies():
            title = alternative_movie.title()
            year = alternative_movie.year()
            countries = alternative_movie.countries()
            # insert a new row in movie table
            self.ui.table_alternative_movies.insertRow(self.ui.table_alternative_movies.rowCount())
            # create a table item with original movie file name
            item_title = QTableWidgetItem(title)
            self.ui.table_alternative_movies.setItem(self.ui.table_alternative_movies.rowCount() - 1, 0, item_title)
            item_year = QTableWidgetItem(year)
            self.ui.table_alternative_movies.setItem(self.ui.table_alternative_movies.rowCount() - 1, 1, item_year)
            item_countries = QTableWidgetItem(countries)
            self.ui.table_alternative_movies.setItem(self.ui.table_alternative_movies.rowCount() - 1, 2, item_countries)
        # auto resize table columns
        self.ui.table_alternative_movies.resizeColumnToContents(0)

    # PANEL movie

    def change_movie(self, checked):
        self.ui.widget_alternative_movies.setVisible(checked)
        self.ui.adjustSize()

    def alternative_movies_selection_changed(self):
        selected_items = self.ui.table_alternative_movies.selectedItems()
        if len(selected_items) > 0:
            index = selected_items[0].row()
            movie = self.current_movie
            movie.set_movie(index)

            self.ui.label_title.setText(movie.title())
            self.ui.label_original_title.setText(movie.original_title())
            self.ui.label_year.setText(movie.year())
            self.ui.label_director.setText(movie.director())
            self.ui.label_duration.setText(movie.duration())
            self.ui.label_language.setText(movie.language())

    def search_new_title(self):
        # get title to look for
        title = unicode(self.ui.text_search_title.text())
        # do not start searching if textTitleSearch is empty
        if title.strip() == '':
            return
        # set gui elements disabled
        self.set_gui_enabled_search_title(False)
        # show searching panel
        self.ui.stack_search_title.setCurrentIndex(1)
        # start searching thread
        threading.Thread(target = self.search_title_run, args = (title,)).start()

    def search_title_run(self, title):
        """
        thread used for movie title searching
        """

        self.current_movie.search_new_title(title)
        # emit signal
        self.search_title_finished.emit()

    def search_title_end(self):
        """
        used when movie title searching finishes (thread returns)
        """

        # re-enable gui elements
        self.set_gui_enabled_search_title(True)
        self.populate_movie_panel()
        self.ui.stack_search_title.setCurrentIndex(0)

    def set_gui_enabled_search_title(self, enabled):
        # set enabled property on actions
        self.ui.action_add_movies.setEnabled(enabled)
        self.ui.action_add_all_movies_in_folder.setEnabled(enabled)
        self.ui.action_add_all_movies_in_folder_subfolders.setEnabled(enabled)
        self.ui.action_remove_selected_movies.setEnabled(enabled)
        self.ui.action_remove_all_movies.setEnabled(enabled)
        self.ui.action_change_renaming_rule.setEnabled(enabled)
        self.ui.action_rename_movies.setEnabled(enabled)
        self.ui.action_preferences.setEnabled(enabled)
        # set enabled property on table
        self.ui.table_movies.setEnabled(enabled)

        self.ui.button_change_movie.setEnabled(enabled)
        self.ui.table_alternative_movies.setEnabled(enabled)

