# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from PyQt4.QtCore import PYQT_VERSION_STR, QSettings, Qt, pyqtSignal
from PyQt4.QtGui import QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, \
    QBrush
from PyQt4.uic import loadUi
from movie import Movie
from renamingrule import RenamingRuleDialog
import imdb
import os.path
import sys
import threading
import utils
import urllib

class GUI(QMainWindow):

    VIDEO_EXTENSIONS = [".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", \
                        ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", \
                        ".rm", ".swf", ".vob", ".wmv"]

    load_movies_finished = pyqtSignal()
    search_title_finished = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)

        #-------------------- variables
        # load settings
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        # get renaming rule from settings
        self.renaming_rule = self.settings.value("renaming_rule").toString()
        # get last visited directory from settings
        self.last_visited_directory = self.settings.value("last_visited_directory").toString()
        # stores movies objects
        self.movies = []
        # stores current (selected) movie
        self.selected_movie = None

        # load GUI
        self.ui = loadUi("main_window.ui", self)
        # create RenamingRuleDialog
        self.ui.renaming_rule_dialog = RenamingRuleDialog(self)
        # set some GUI parameters
        self.ui.panel_loading.setVisible(False)
        self.ui.stack_movie.setVisible(False)
        self.ui.stack_title_search.setVisible(False)
        self.ui.table_movies.resizeColumnToContents(0)
        # adjust wondow size to content
        self.adjustSize()

        ## connect signals
        # MENU Movies
        self.ui.action_add_movies.triggered.connect(self.add_movies)
        self.ui.action_add_all_movies_in_folder.triggered.connect(self.add_movies_in_folder)
        self.ui.action_add_all_movies_in_folder_subfolders.triggered.connect(self.add_movies_in_folder_subfolders)
        self.ui.action_remove_selected_movies.triggered.connect(self.remove_selected_movies)
        self.ui.action_remove_all_movies.triggered.connect(self.remove_all_movies)
        self.ui.action_change_rename_pattern.triggered.connect(self.change_renaming_rule)
        self.ui.action_rename_movies.triggered.connect(self.rename_movies)
        self.load_movies_finished.connect(self.load_movies_end)
        # MENU ?
        self.ui.action_about.triggered.connect(self.show_about)
        # TABLE movies
        self.ui.table_movies.itemSelectionChanged.connect(self.movies_selection_changed)
        # STACK movie
        self.ui.combo_movie_titles.activated.connect(self.movie_title_changed)
        self.ui.combo_aka.activated.connect(self.aka_changed)
        self.ui.combo_runtime.activated.connect(self.runtime_changed)
        self.ui.combo_language.activated.connect(self.language_changed)
        # searching panel
        self.ui.button_manual_title_search.toggled.connect(self.manual_title_search)
        self.ui.text_title_search.returnPressed.connect(self.search_title)
        self.ui.button_title_search.clicked.connect(self.search_title)
        self.ui.button_title_new_research.clicked.connect(self.search_again_for_title)
        self.search_title_finished.connect(self.search_title_end)

        # check internet connection
        self.check_connection()

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
            title = self.tr("Internet connection down?")
            msg = self.tr("""
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
            """)
            QMessageBox.warning(self, title, msg)

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
        load_movies_thread = threading.Thread(target = self.load_movies_run, args = (filepaths,))
        load_movies_thread.start()

    def load_movies_run(self, filepaths):
        # loop on file paths
        for filepath in filepaths:
            # set loading label text, show current file name
            self.ui.label_loading.setText(self.tr("Getting information from ")\
                                           + os.path.split(filepath)[1])
            # create a new movie object
            movie = Movie(filepath)
            # generate new movie name based on renaming rule
            movie.generate_new_name(self.renaming_rule)
            # add movie to list
            self.movies.append(movie)
            # insert a new row in movie table
            self.ui.table_movies.insertRow(self.ui.table_movies.rowCount())
            # create a table item with original movie file name
            item_original_name = QTableWidgetItem(movie.original_name)
            self.ui.table_movies.setItem(self.ui.table_movies.rowCount() - 1, 0, item_original_name)
            # create a table item with new movie file name
            item_new_name = QTableWidgetItem(movie.new_name)
            self.ui.table_movies.setItem(self.ui.table_movies.rowCount() - 1, 1, item_new_name)
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
        self.ui.action_change_rename_pattern.setEnabled(enabled)
        self.ui.action_rename_movies.setEnabled(enabled)
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
        # loop on movies
        for i in range(len(self.movies)):
            movie = self.movies[i]
            # generate new movie name based on new renaming rule
            movie.generate_new_name(self.renaming_rule)
            # set "before renaming state", because after renaming a movie
            # can be renamed a second time, after having changed the rule
            movie.state = Movie.STATE_BEFORE_RENAMING
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

    # MENU ?

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
            self.selected_movie = selected_items[0]
            movie = self.movies[self.selected_movie.row()]

            # set movie panel based on movie state (
            self.ui.stack_movie.setCurrentIndex(movie.state)
            # populate movie panel
            self.populate_movie_stack(movie)
            # set panel visible
            self.ui.stack_movie.setVisible(True)

    # STACK movie

    def movie_title_changed(self, index):
        """
        called when current movie title changes.
        
        each movie have at least one title associated, and user can change 
        the proper one.
        """

        row = self.selected_movie.row()
        movie = self.movies[row]
        # set new index on movie
        movie.info_index = index
        # generate new movie name
        movie.generate_new_name(self.renaming_rule)
        # update table with new name
        self.ui.table_movies.item(row, 1).setText(movie.new_name)
        # selected movie title changed, so movie panel needs to
        # be populated with current movie title information
        self.populate_movie_info(movie)

    def aka_changed(self, index):
        """
        called when AKA, for current movie, changes
        """

        row = self.selected_movie.row()
        movie = self.movies[row]
        # set new index on movie
        movie.info[movie.info_index][Movie.AKAS_INDEX] = index
        # generate new movie name
        movie.generate_new_name(self.renaming_rule)
        # update table with new name
        self.ui.table_movies.item(row, 1).setText(movie.new_name)

    def runtime_changed(self, index):
        """
        called when runtime, for selected movie, changes
        """

        row = self.selected_movie.row()
        movie = self.movies[row]
        # set new index on movie
        movie.info[movie.info_index][Movie.RUNTIMES_INDEX] = index
        # generate new movie name
        movie.generate_new_name(self.renaming_rule)
        # update table with new name
        self.ui.table_movies.item(row, 1).setText(movie.new_name)

    def language_changed(self, index):
        """
        called when language, for selected movie, changes
        """

        row = self.selected_movie.row()
        movie = self.movies[row]
        # set new index on movie
        movie.language_index = index
        # generate new movie name
        movie.generate_new_name(self.renaming_rule)
        # update table with new name
        self.ui.table_movies.item(row, 1).setText(movie.new_name)

    def manual_title_search(self, checked):
        """
        show or hide manual title search_title_run panel
        
        button associated with that slot is a toggle button,
        so checked represents its state
        """

        # title search_title_run panel visibility
        self.ui.stack_title_search.setVisible(checked)
        # search_title_run panel visible
        if checked:
            self.prepare_new_search()

    def search_title(self):
        """
        search_title_run for a movie title
        """

        # get title to look for
        title = unicode(self.ui.text_title_search.text())
        # do not start searching if textTitleSearch is empty
        if title.strip() == "":
            return
        # set gui elements disabled
        self.set_gui_enabled_search_title(False)
        # show searching panel
        self.ui.stack_title_search.setCurrentIndex(1)
        # start searching thread
        search_thread = threading.Thread(target = self.search_title_run, args = (title,))
        search_thread.start()

    def search_title_run(self, title):
        """
        thread used for movie title searching
        """

        row = self.selected_movie.row()
        movie = self.movies[row]
        # search_title_run for movie title
        movie.search_title(title)
        # emit signal
        self.search_title_finished.emit()

    def search_title_end(self):
        """
        used when movie title searching finishes (thread returns)
        """

        row = self.selected_movie.row()
        movie = self.movies[row]
        # re-enable gui elements
        self.set_gui_enabled_search_title(True)
        # no corresponding movie found
        if len(movie.info) == 0:
            # set failed search_title_run panel
            self.ui.stack_title_search.setCurrentIndex(2)
        else:
            # generate new movie name, based on new information
            movie.generate_new_name(self.renaming_rule)
            # update table with new name
            self.ui.table_movies.item(row, 1).setText(movie.new_name)
            # populate movie panel
            self.populate_movie_stack(movie)

    def set_gui_enabled_search_title(self, enabled):
        # set enabled property on actions
        self.ui.action_add_movies.setEnabled(enabled)
        self.ui.action_add_all_movies_in_folder.setEnabled(enabled)
        self.ui.action_add_all_movies_in_folder_subfolders.setEnabled(enabled)
        self.ui.action_remove_selected_movies.setEnabled(enabled)
        self.ui.action_remove_all_movies.setEnabled(enabled)
        self.ui.action_change_rename_pattern.setEnabled(enabled)
        self.ui.action_rename_movies.setEnabled(enabled)
        # set enabled property on movie panel
        self.ui.combo_movie_titles.setEnabled(enabled)
        self.ui.button_manual_title_search.setEnabled(enabled)
        self.ui.combo_aka.setEnabled(enabled)
        self.ui.combo_language.setEnabled(enabled)
        self.ui.combo_runtime.setEnabled(enabled)
        # set enabled property on table
        self.ui.table_movies.setEnabled(enabled)

    def search_again_for_title(self):
        """
        called when user wants to search_title_run again for a title
        """

        self.prepare_new_search()

    def prepare_new_search(self):
        """
        prepare searching panel for a new title search_title_run
        """

        # set stack index on search_title_run panel
        self.ui.stack_title_search.setCurrentIndex(0)
        # select all text in searching text field
        self.ui.text_title_search.selectAll()
        # set focus on searching text field
        self.ui.text_title_search.setFocus()

    def populate_movie_stack(self, movie):
        """
        used to update movie panel with information about selected movie,
        based on movie state
        """

        if movie.state == Movie.STATE_RENAMING_ERROR:
            self.ui.label_error.setText(movie.renaming_error)
        elif movie.state == Movie.STATE_BEFORE_RENAMING:
            # clear the titles combo...
            self.ui.combo_movie_titles.clear()
            # if movie info not empty
            if len(movie.info) != 0:
                # populate combo with titles
                for movie_info in movie.info:
                    self.ui.combo_movie_titles.addItem(movie_info['title'])
                # set the proper index
                self.ui.combo_movie_titles.setCurrentIndex(movie.info_index)
            # update also the panel
            self.populate_movie_info(movie)

    def populate_movie_info(self, movie):
        """
        used to update movie panel with information about 
        selected movie title
        """

        self.ui.combo_aka.clear()
        self.ui.combo_runtime.clear()
        # reset search_title_run panel
        self.ui.button_manual_title_search.setChecked(False)
        self.ui.stack_title_search.setCurrentIndex(0)
        self.ui.text_title_search.setText("")
        # if movie info not empty
        if len(movie.info) != 0:
            # get movie index
            info = movie.info[movie.info_index]
            self.ui.label_canonical_title.setText(info[Movie.CANONICAL_TITLE])
            self.ui.combo_aka.addItems(info[Movie.AKAS])
            self.ui.combo_aka.setCurrentIndex(info[Movie.AKAS_INDEX])
            self.ui.label_year.setText(info[Movie.YEAR])
            self.ui.label_director.setText(info[Movie.DIRECTOR])
            self.ui.combo_runtime.addItems(info[Movie.RUNTIMES])
            self.ui.combo_runtime.setCurrentIndex(info[Movie.RUNTIMES_INDEX])
        else:
            self.ui.label_canonical_title.setText('')
            self.ui.label_year.setText('')
            self.ui.label_director.setText('')
        self.ui.combo_language.setCurrentIndex(movie.language_index)





