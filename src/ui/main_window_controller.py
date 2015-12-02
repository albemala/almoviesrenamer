import os
import platform
import threading
from PyQt5.QtCore import Qt, pyqtSignal, PYQT_VERSION_STR, QUrl, QObject
from PyQt5.QtGui import QBrush, QDesktopServices
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import application
from movie import Movie
from preferences import preferences
from preferences_dialog import PreferencesDialog
from stats_agreement_dialog import StatsAgreementDialog
import utils
from ui.main_window_view import MainWindowView

__author__ = "Alberto Malagoli"


class MainWindowController(QObject):
    __VIDEO_EXTENSIONS = [".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv",
                          ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg",
                          ".rm", ".swf", ".vob", ".wmv"]

    __load_movies_finished = pyqtSignal()
    __movie_added = pyqtSignal(Movie)
    __loading_movie_changed = pyqtSignal(str)
    __search_alternative_movie_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        # TODO
        # # check internet connection
        # self.check_connection()
        # # check for new program version
        # self.check_new_version()

        # variables
        # stores movies objects
        self.__movies = []

        # TODO
        # # show stats agreement dialog
        # self.show_stats_agreement()

        # load GUI
        self.__main_window = MainWindowView()

        # signals connection
        self.__main_window.get_add_movie_button_clicked_signal().connect(self.add_movies)
        # self.__main_window.get_movie_info_changed_signal().connect()
        self.__main_window.get_movie_item_selected_signal().connect(self.__movie_item_selected)
        self.__main_window.get_movie_alternative_title_changed_signal().connect(
            self.__on_movie_alternative_title_changed)
        self.__main_window.get_search_movie_button_clicked_signal().connect(
            self.__on_search_alternative_movie_button_clicked)

        # self._ui.action_add_movies.triggered.connect(self.add_movies)
        # self._ui.action_add_all_movies_in_folder.triggered.connect(self.add_movies_in_folder)
        # self._ui.action_add_all_movies_in_folder_subfolders.triggered.connect(self.add_movies_in_folder_and_subfolders)
        # self._ui.action_remove_selected_movies.triggered.connect(self.remove_selected_movies)
        # self._ui.action_remove_all_movies.triggered.connect(self.remove_all_movies)
        # self._ui.action_change_renaming_rule.triggered.connect(self.change_renaming_rule)
        # self._ui.action_rename_movies.triggered.connect(self.rename_movies)
        self.__load_movies_finished.connect(self.__on_load_movies_finished)
        self.__movie_added.connect(self.__on_movie_added)
        self.__loading_movie_changed.connect(self.__on_loading_movie_changed)
        # self._ui.text_search_title.returnPressed.connect(self.search_new_title)
        # self._ui.button_search_title.clicked.connect(self.search_new_title)
        self.__search_alternative_movie_finished.connect(self.__on_search_alternative_movie_finished)
        # self._ui.action_preferences.triggered.connect(self.show_preferences)
        # self._ui.action_about.triggered.connect(self.show_about)
        # self._ui.table_movies.itemSelectionChanged.connect(self.movies_selection_changed)
        # self._ui.table_movies.itemDoubleClicked.connect(self.movie_double_clicked)
        # self._ui.table_movies.addAction(self.action_copy_title)
        # self._ui.table_movies.addAction(self.action_open_containing_folder)
        # self._ui.action_copy_title.triggered.connect(self.copy_title)
        # self._ui.action_open_containing_folder.triggered.connect(self.open_containing_folder)
        # self._ui.table_others_info.itemSelectionChanged.connect(self.alternative_movies_selection_changed)

        self.__main_window.set_loading_panel_visible(False)
        self.__main_window.set_movie_info_panel_visible(False)
        self.__main_window.set_movie_renamed_panel_visible(False)
        self.__main_window.set_movie_error_panel_visible(False)

    def show_stats_agreement(self):
        """
        shows usage statistics agreement dialog
        """

        # get if this is the first time user opens the program
        first_time = preferences.get_first_time_opening()
        if first_time:
            # create agreement dialog
            stats_agreement_dialog = StatsAgreementDialog(self)
            # show it
            stats_agreement_dialog.exec_()
            # nex time user will open the program, don't show that dialog
            preferences.set_first_time_opening(False)

    def add_movies(self):
        """
        select video files from file system using a FileDialog,
        then creates corresponding movie objects

        these movies will populate movie table

        get information from selected files
        """

        # create a filter, only video files can be selected
        video_filter = "Video (*{0})".format(" *".join(MainWindowController.__VIDEO_EXTENSIONS))
        dialog_title = "Select movies you want to rename..."
        # select video files from file system
        open_files_result = QFileDialog.getOpenFileNames(None,
                                                         dialog_title,
                                                         preferences.get_last_visited_directory(),
                                                         video_filter)
        # open_files_result is a set: ([files_paths], video_filter)
        files_paths = open_files_result[0]
        # if at least one file has been selected
        if len(files_paths) > 0:
            self.load_movies(files_paths)

    def add_movies_in_folder(self):
        """
        select all video files from a selected folder using a FileDialog,
        then creates corresponding movie objects

        these movies will populate movie table

        get information from selected files
        """

        # dialog title
        title = "Select a folder containing movies..."
        # select folder from file system
        folder_path = QFileDialog.getExistingDirectory(None,
                                                       title,
                                                       preferences.get_last_visited_directory())
        # if a directory has been selected
        if folder_path != "":
            files_paths = []
            # for each entry (files + folders) in selected folder
            for entry in os.listdir(folder_path):
                self.add_file_to_list_if_video(folder_path, entry, files_paths)

            self.load_movies(files_paths)

    def add_movies_in_folder_and_subfolders(self):
        """
        select all video files from a selected folder and subfolders using a FileDialog,
        then creates corresponding movie objects

        these movies will populate movie table

        get information from selected files
        """

        # dialog title
        title = "Select a folder containing movies..."
        # select folder from file system
        folder_path = QFileDialog.getExistingDirectory(None,
                                                       title,
                                                       preferences.get_last_visited_directory())
        # if a directory has been selected
        if folder_path != "":
            files_paths = []
            # walk on chosen directory, and loop on files and directories
            for root, dirs, files in os.walk(folder_path):
                # for each file
                for name in files:
                    self.add_file_to_list_if_video(root, name, files_paths)

            self.load_movies(files_paths)

    def add_file_to_list_if_video(self, path, name, files):
        entry = os.path.join(path, name)
        # select only video files
        extension = os.path.splitext(name)[1].lower()
        if os.path.isfile(entry) and extension in MainWindowController.__VIDEO_EXTENSIONS:
            # save entry with path
            files.append(entry)

    def load_movies(self, files_paths):
        """
        given a list of file paths, creates a movie object for each
        file, get info from it, and populate movies table
        """

        self.__set_last_visited_directory(files_paths)
        # disable gui elements which cannot be used during loading
        # TODO
        # self.set_gui_enabled_load_movies(False)
        # show loading panel
        self.__main_window.set_loading_panel_visible(True)
        # start loading thread
        threading.Thread(target=self.load_movies_run, args=(files_paths,)).start()

    def __set_last_visited_directory(self, files_paths):
        # takes first selected file and get the file path, use it as the last visited directory
        first_file_path = files_paths[0]
        file_path = os.path.split(first_file_path)[0]
        last_visited_directory = os.path.normpath(file_path)
        # save it in settings
        preferences.set_last_visited_directory(last_visited_directory)

    def load_movies_run(self, file_paths):
        # loop on file paths
        for file_path in file_paths:
            # set loading label text, show current file name
            file_name = os.path.split(file_path)[1]
            self.__loading_movie_changed.emit(file_name)

            movie = self.__create_movie(file_path)
            self.__movies.append(movie)
            self.__movie_added.emit(movie)
        self.__load_movies_finished.emit()

    def __create_movie(self, file_path):
        movie = Movie()
        movie.fill_with_file(file_path)
        movie_guessed_info = movie.get_guessed_info()
        movie.fetch_tmdb_info(movie_guessed_info.get_title(),
                              movie_guessed_info.get_year(),
                              movie_guessed_info.get_language())
        movie.generate_new_name(preferences.get_renaming_rule())
        return movie

    def __on_movie_added(self, movie: Movie):
        self.insert_movie_in_table_view(movie)

    def __on_loading_movie_changed(self, file_name: str):
        self.__main_window.set_loading_panel_movie_title(file_name)

    def insert_movie_in_table_view(self, movie):
        original_name = movie.get_original_name()
        new_name = movie.get_new_name()
        self.__main_window.add_movie_table_item(original_name, new_name)

    def __on_load_movies_finished(self):
        # re-enable gui elements
        # TODO
        # self.set_gui_enabled_load_movies(True)
        self.__main_window.set_loading_panel_visible(False)
        # play a sound
        QApplication.beep()

    def set_gui_enabled_load_movies(self, enabled):
        # TODO check
        # set enabled property on actions
        self._ui.action_add_movies.setEnabled(enabled)
        self._ui.action_add_all_movies_in_folder.setEnabled(enabled)
        self._ui.action_add_all_movies_in_folder_subfolders.setEnabled(enabled)
        self._ui.action_remove_selected_movies.setEnabled(enabled)
        self._ui.action_remove_all_movies.setEnabled(enabled)
        self._ui.action_change_renaming_rule.setEnabled(enabled)
        self._ui.action_rename_movies.setEnabled(enabled)
        self._ui.action_preferences.setEnabled(enabled)
        if not enabled:
            # clear table selection (and hide movie panel, if visible)
            self._ui.table_movies.selectionModel().clear()
        # set enabled property on table
        self._ui.table_movies.setEnabled(enabled)

    def remove_selected_movies(self):
        """
        removes selected movies from movies table
        """

        # get selected items
        selected_items = self._ui.table_movies.selectionModel().selectedRows()
        # loop on items
        for item in reversed(selected_items):
            # get item row
            row = item.row()
            # first remove items from table
            self._ui.table_movies.takeItem(row, 0)
            self._ui.table_movies.takeItem(row, 1)
            # them remove corresponding row
            self._ui.table_movies.removeRow(row)
            # delete movie item
            del self.__movies[row]

    def remove_all_movies(self):
        """
        removes all movies from movies table
        """

        del self.__movies[:]
        # clear table contents
        self._ui.table_movies.clearContents()
        # remove all rows
        self._ui.table_movies.setRowCount(0)

    def change_renaming_rule(self):
        """
        show renaming rule dialog
        """

        self._ui.table_movies.clearSelection()
        # show renaming rule dialog
        self._ui.renaming_rule_dialog.exec_()
        renaming_rule = preferences.get_renaming_rule()
        # loop on movies
        for i in range(len(self.__movies)):
            movie = self.__movies[i]
            # generate new movie name based on new renaming rule
            movie.generate_new_name(renaming_rule)
            # set "before renaming state", because after renaming a movie
            # can be renamed a second time, after having changed the rule
            movie.set_renaming_state(Movie.STATE_BEFORE_RENAMING)
            self._ui.table_movies.item(i, 1).setForeground(QBrush(Qt.black))
            self._ui.table_movies.item(i, 1).setText(movie.get_renamed_file_name())

    def rename_movies(self):
        """
        rename files with new name
        """

        self._ui.table_movies.clearSelection()
        # loop on movies
        for i in range(len(self.__movies)):
            movie = self.__movies[i]
            # check if new title is a valid file name
            if movie.check_and_clean_new_name():
                # set "new name" table item with new movie name
                self._ui.table_movies.item(i, 1).setText(movie.get_renamed_file_name())
                try:
                    # rename file
                    os.rename(movie.get_absolute_original_file_path(), movie.get_absolute_renamed_file_path())
                except OSError as e:
                    # set state and renaming error
                    movie.set_renaming_state(Movie.STATE_RENAMING_ERROR, e.strerror)
                    # paint "new name" table item with red
                    self._ui.table_movies.item(i, 1).setForeground(QBrush(Qt.red))
                else:
                    # correctly renamed
                    movie.set_renaming_state(Movie.STATE_RENAMED)
                    # set "original name" table item with new movie name
                    self._ui.table_movies.item(i, 0).setText(movie.get_renamed_file_name())
                    # paint "new name" table item with green
                    self._ui.table_movies.item(i, 1).setForeground(QBrush(Qt.darkGreen))

                    # MENU Program

    def show_preferences(self):
        # show renaming rule dialog
        self._ui.preferences_dialog.exec_()
        renaming_rule = preferences.get_renaming_rule()
        # loop on movies
        for i in range(len(self.__movies)):
            movie = self.__movies[i]
            # generate new movie name based on new renaming rule
            movie.generate_new_name(renaming_rule)
            # set "before renaming state", because after renaming a movie
            # can be renamed a second time, after having changed the rule
            movie.set_renaming_state(Movie.STATE_BEFORE_RENAMING)
            self._ui.table_movies.item(i, 1).setForeground(QBrush(Qt.black))
            self._ui.table_movies.item(i, 1).setText(movie.get_renamed_file_name())

    def show_about(self):
        """
        shows an about dialog, with info on program
        """

        # message shown on about dialog
        msg = """
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
            <li>
                <a href="http://www.python.org/">Python</a>: {2}
            </li>
            <li>
                <a href="http://www.riverbankcomputing.co.uk/software/pyqt/download">PyQt</a>: {3}
            </li>
            <li>
                <a href="http://imdbpy.sourceforge.net/">IMDbPY</a>: {4}
            </li>
            <li>
                <a href="https://github.com/Diaoul/enzyme">enzyme</a>: 0.2
            </li>
            <li>
                <a href="http://cx-freeze.sourceforge.net/">cx-Freeze</a>: 4.2.3
            </li>
        </ul>
    </p>
    <p>
        Thanks to:
        <ul>
            <li>
                <a href="http://www.imdbapi.com/">The IMDb API</a>, which is used to retrieve movies information<br>
                <b>Please donate to support this service!</b>
            </li>
            <li>
                <a href="http://file-folder-ren.sourceforge.net/">M\xe9tamorphose</a> for some stolen code :)
            </li>
            <li>
            <a href="http://p.yusukekamiyamane.com/">Yusuke Kamiyamane</a> for Fugue Icons
            </li>
        </ul>
    </p>
            """.format(application.NAME, application.VERSION, platform.python_version(), PYQT_VERSION_STR,
                       0
                       # TODO
                       # imdb.VERSION
                       )
        # show the about dialog
        QMessageBox.about(self, "About {0}".format(application.NAME), msg)

    def __movie_item_selected(self, row):
        if row == -1:
            self.__main_window.set_movie_info_panel_visible(False)
            self.__main_window.set_movie_error_panel_visible(False)
            self.__main_window.set_movie_renamed_panel_visible(False)
        else:
            movie = self.__movies[row]
            if movie.get_renaming_state() == Movie.STATE_RENAMING_ERROR:
                self.__main_window.set_movie_error(movie.get_renaming_error())
                self.__main_window.set_movie_error_panel_visible(True)
            elif movie.get_renaming_state() == Movie.STATE_RENAMED:
                self.__main_window.set_movie_renamed_panel_visible(True)
            elif movie.get_renaming_state() == Movie.STATE_BEFORE_RENAMING:
                self.__main_window.set_movie_info_panel_visible(True)
                self.__main_window.set_movie_alternative_titles_model(movie.get_alternative_titles())
                self.__populate_movie_info_panel(movie)

    def __on_movie_alternative_title_changed(self, index: int):
        movie = self.__get_selected_movie()
        if movie is None:
            return

        movie.set_current_info_index(index)
        self.__populate_movie_info_panel(movie)

    def __populate_movie_info_panel(self, movie: Movie):
        self.__main_window.set_movie_title(movie.get_title())
        self.__main_window.set_movie_original_title(movie.get_original_title())
        self.__main_window.set_movie_year(movie.get_year())
        self.__main_window.set_movie_directors(movie.get_director())
        self.__main_window.set_movie_duration(movie.get_duration())
        self.__main_window.set_movie_language(movie.get_language())

    def __on_search_alternative_movie_button_clicked(self):
        title = self.__main_window.get_movie_search_alternative_title()
        year = self.__main_window.get_movie_search_alternative_year()
        language = self.__main_window.get_movie_search_alternative_language()
        if title.strip() is "":
            return

        # set gui elements disabled
        # TODO
        # self.set_gui_enabled_search_title(False)
        self.__main_window.set_movie_search_progress_bar_visible(True)
        # start searching thread
        threading.Thread(target=self.__search_alternative_movie_run, args=(title, year, language)).start()

    def movies_selection_changed(self):
        """
        called when selection in table_movies changes, i.e. user selects
        different movies from previously selected ones.
        """
        selected_movie = self.__get_selected_movie()
        # no movies selected
        if selected_movie is None:
            # hide movie panel
            self._ui.stack_movie.setVisible(False)
        else:
            # set movie panel based on movie state (
            self._ui.stack_movie.setCurrentIndex(selected_movie.get_renaming_state())
            # populate movie panel
            if selected_movie.get_renaming_state() == Movie.STATE_RENAMING_ERROR:
                self._ui.label_error.setText("""
                    <html><head/><body><p><span style="font-size:11pt; font-weight:400; color:#ff0000;">
                    """
                                             + selected_movie.get_renaming_error() +
                                             """
                                             </span></p></body></html>
                                             """)
            elif selected_movie.get_renaming_state() == Movie.STATE_BEFORE_RENAMING:
                self.populate_movie_panel()
                self._ui.stack_search_title.setCurrentIndex(0)
                self._ui.text_search_title.clear()

            # set panel visible
            self._ui.stack_movie.setVisible(True)

    def movie_double_clicked(self, item):
        """
        when a movie item is double clicked in table,
        it opens operative system file manager
        with file location on disk
        """

        movie = self.__movies[item.row()]
        path = movie.get_directory_path()
        self.open_path(path)

    def open_containing_folder(self):
        movie = self.__get_selected_movie()
        if movie is not None:
            path = movie.get_directory_path()
            self.open_path(path)

    def open_path(self, path):
        """
        opens a path using the operative system file manager/explorer
        """
        QDesktopServices.openUrl(self, QUrl('file:///' + path))

    def copy_title(self):
        """
        copy selected movie title in movie table
        into clipboard
        """

        movie = self.__get_selected_movie()
        if movie != None:
            clipboard = QApplication.clipboard()
            clipboard.setText(movie.get_original_file_name())

    def populate_movie_panel(self):
        movie = self.__get_selected_movie()

        self._ui.label_title.setText(movie.get_title())
        self._ui.label_original_title.setText(movie.get_original_title())
        self._ui.label_year.setText(movie.get_year())
        self._ui.label_director.setText(movie.get_director())
        self._ui.label_duration.setText(movie.get_duration())
        language = movie.get_language()
        if movie.get_subtitle_language() != "":
            language += " (subtitled " + movie.get_subtitle_language() + ")"
        self._ui.label_language.setText(language)

        # clear table contents
        self._ui.table_others_info.clearContents()
        # remove all rows
        self._ui.table_others_info.setRowCount(0)
        # TODO
        # for other_info in movie_info.others_info():
        #     title = other_info[0]
        #     language = other_info[1]
        #     # insert a new row in movie table
        #     self._ui.table_others_info.insertRow(self._ui.table_others_info.rowCount())
        #     # create a table item with original movie file name
        #     item_title = QTableWidgetItem(title)
        #     self._ui.table_others_info.setItem(self._ui.table_others_info.rowCount() - 1, 0, item_title)
        #     item_language = QTableWidgetItem(language)
        #     self._ui.table_others_info.setItem(self._ui.table_others_info.rowCount() - 1, 1, item_language)
        # auto resize table columns
        self._ui.table_others_info.resizeColumnToContents(0)

    def alternative_movies_selection_changed(self):
        selected_info = self._ui.table_others_info.selectedItems()
        if len(selected_info) > 0:
            info_index = selected_info[0].row()
            movie = self.__get_selected_movie()
            movie.set_movie(info_index)
            renaming_rule = preferences.get_renaming_rule()
            # generate new movie name based on renaming rule
            movie.generate_new_name(renaming_rule)
            # create a table item with new movie file name
            item_new_name = QTableWidgetItem(movie.get_renamed_file_name())
            selected_movie = self._ui.table_movies.selectedItems()[0]
            # store first selected movie
            movie_index = selected_movie.row()
            self._ui.table_movies.setItem(movie_index, 1, item_new_name)
            # update labels in movie panel
            self._ui.label_title.setText(movie.get_title())
            self._ui.label_original_title.setText(movie.get_original_title())
            self._ui.label_year.setText(movie.get_year())
            self._ui.label_director.setText(movie.get_directors())
            self._ui.label_duration.setText(movie.get_duration())
            self._ui.label_language.setText(movie.get_language())

    def __search_alternative_movie_run(self, title: str, year: str, language: str):
        """
        thread used for movie title searching
        """

        self.__get_selected_movie().fetch_tmdb_info(title, year, language)

        self.__search_alternative_movie_finished.emit()

    def __on_search_alternative_movie_finished(self):
        """
        used when movie title searching finishes (thread returns)
        """

        # re-enable gui elements
        # TODO
        # self.set_gui_enabled_search_title(True)

        movie = self.__get_selected_movie()
        self.__main_window.set_movie_alternative_titles_model(movie.get_alternative_titles())
        self.__populate_movie_info_panel(movie)

        self.__main_window.set_movie_search_progress_bar_visible(False)

        return
        # TODO
        renaming_rule = preferences.get_renaming_rule()
        # generate new movie name based on renaming rule
        movie = self.__get_selected_movie()
        movie.generate_new_name(renaming_rule)
        # create a table item with new movie file name
        item_new_name = QTableWidgetItem(movie.get_renamed_file_name())
        selected_movie = self._ui.table_movies.selectedItems()[0]
        # store first selected movie
        movie_index = selected_movie.row()
        self._ui.table_movies.setItem(movie_index, 1, item_new_name)
        self.populate_movie_panel()
        self._ui.stack_search_title.setCurrentIndex(0)

    def set_gui_enabled_search_title(self, enabled):
        # set enabled property on actions
        self._ui.action_add_movies.setEnabled(enabled)
        self._ui.action_add_all_movies_in_folder.setEnabled(enabled)
        self._ui.action_add_all_movies_in_folder_subfolders.setEnabled(enabled)
        self._ui.action_remove_selected_movies.setEnabled(enabled)
        self._ui.action_remove_all_movies.setEnabled(enabled)
        self._ui.action_change_renaming_rule.setEnabled(enabled)
        self._ui.action_rename_movies.setEnabled(enabled)
        self._ui.action_preferences.setEnabled(enabled)
        # set enabled property on table
        self._ui.table_movies.setEnabled(enabled)

        self._ui.table_others_info.setEnabled(enabled)

    def __get_selected_movie(self) -> Movie:
        current_row = self.__main_window.get_movies_table_current_row()
        if current_row == -1:
            return None
        selected_movie = self.__movies[current_row]
        return selected_movie
