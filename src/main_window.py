# -*- coding: latin-1 -*-
from preferences_dialog import PreferencesDialog
from renaming_rule_dialog import RenamingRuleDialog

__author__ = "Alberto Malagoli"

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
# import imdb
import utils


# def send_usage_statistics():
#     """
#     checks user choice about sending usage statistics and
#     sends usage statistics to a dedicated web service
#     """
#
#     # get user choice about sending usage statistics
#     send_usage_statistics = utils.preferences.value("stats_agreement").toInt()[0]
#     # if user chose to send usage statistics
#     if send_usage_statistics == PreferencesDialog.STATS_AGREE:
#         # start sending thread
#         threading.Thread(target = send_usage_statistics_run).start()
#
# def send_usage_statistics_run():
#     """
#     sends usage statistics to a dedicated web service
#     """
#
#     # get preferences
#     rule = utils.preferences.value("renaming_rule").toString()
#     duration = utils.preferences.value("duration_representation").toString()
#     language = utils.preferences.value("language_representation").toString()
#     separator = utils.preferences.value("words_separator").toString()
#     # web service url
#     url = "http://almoviesrenamer.appspot.com/stats"
#     # create data
#     values = {
#         'rule' : rule,
#         'duration' : duration,
#         'language' : language,
#         'separator' : separator
#     }
#     data = urllib.urlencode(values)
#     # POST send data to web service
#     f = urllib2.urlopen(url, data)

class GUI(QMainWindow):

#     VIDEO_EXTENSIONS = [".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", \
#                         ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", \
#                         ".rm", ".swf", ".vob", ".wmv"]
#
#     load_movies_finished = pyqtSignal()
#     search_title_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        # TODO
        # # check internet connection
        # self.check_connection()
        # # check for new program version
        # self.check_new_version()

        ## variables
        # get last visited directory from settings
        # TODO
        # self.last_visited_directory = utils.preferences.value("last_visited_directory").toString()
        # stores movies objects
        self.movies = []
        # stores current (selected) movie
        self.current_movie = None

        # TODO
        # # show stats agreement dialog
        # self.show_stats_agreement()

        # load GUI
        self.ui = loadUi("main_window.ui", self)
        # create SettingsDialog
        self.ui.preferences_dialog = PreferencesDialog(self)
        # create RenamingRuleDialog
        self.ui.renaming_rule_dialog = RenamingRuleDialog(self, self.ui.preferences_dialog)
        # set some GUI parameters
        self.setWindowTitle(utils.PROGRAM_NAME)
        self.ui.panel_loading.setVisible(False)
        self.ui.stack_movie.setVisible(False)
        self.ui.table_movies.resizeColumnToContents(0)
        # set window as maximized
        self.ui.setWindowState(Qt.WindowMaximized)

        # ## signals connection
        # # MENU Movies
        # self.ui.action_add_movies.triggered.connect(self.add_movies)
        # self.ui.action_add_all_movies_in_folder.triggered.connect(self.add_movies_in_folder)
        # self.ui.action_add_all_movies_in_folder_subfolders.triggered.connect(self.add_movies_in_folder_subfolders)
        # self.ui.action_remove_selected_movies.triggered.connect(self.remove_selected_movies)
        # self.ui.action_remove_all_movies.triggered.connect(self.remove_all_movies)
        # self.ui.action_change_renaming_rule.triggered.connect(self.change_renaming_rule)
        # self.ui.action_rename_movies.triggered.connect(self.rename_movies)
        # self.load_movies_finished.connect(self.load_movies_end)
        # self.ui.text_search_title.returnPressed.connect(self.search_new_title)
        # self.ui.button_search_title.clicked.connect(self.search_new_title)
        # self.search_title_finished.connect(self.search_title_end)
        # # MENU Program
        # self.ui.action_preferences.triggered.connect(self.show_preferences)
        # self.ui.action_about.triggered.connect(self.show_about)
        # # TABLE movies
        # self.ui.table_movies.itemSelectionChanged.connect(self.movies_selection_changed)
        # self.ui.table_movies.itemDoubleClicked.connect(self.movie_double_clicked)
        # self.ui.table_movies.addAction(self.action_copy_title)
        # self.ui.table_movies.addAction(self.action_open_containing_folder)
        # self.ui.action_copy_title.triggered.connect(self.copy_title)
        # self.ui.action_open_containing_folder.triggered.connect(self.open_containing_folder)
        # # STACK movie
        # self.ui.table_others_info.itemSelectionChanged.connect(self.alternative_movies_selection_changed)
        self.show()

#     def check_connection(self):
#         """
#         checks if internet connection is up.
#
#         if internet connection is down, notifies the user with a message.
#         """
#
#         try:
#             # try to open a web URL
#             f = urllib2.urlopen("http://www.google.com/")
#         except URLError:
#             # if an error occurs, notify the user with a message
#             msg_box = QMessageBox()
#             msg_box.setWindowTitle(QApplication.translate('GUI', "Internet connection down?"))
#             msg_box.setText(QApplication.translate('GUI', """
# <p>It seems your internet connection is down (but maybe I'm wrong).</p>
# <p>That program needs access to the internet, to get information about movies, so please check your connection.</p>
# <p>If I'm wrong, sorry for the interruption...</p>
#             """))
#             icon = QPixmap()
#             icon.load('icons/exclamation.png')
#             msg_box.setIconPixmap(icon)
#             msg_box.exec_()
#
#     def check_new_version(self):
#         """
#         checks for new program version, and notify in case of
#         a newer version
#         """
#
#         # create url, with current program version
#         url = "http://almoviesrenamer.appspot.com/checknewversion"
#         # call web service
#         f = urllib2.urlopen(url)
#         # read the answer (could be "yes" for new version, or "no")
#         version = f.read().rstrip('\n')
#         # if there is a new version
#         if version != utils.PROGRAM_VERSION:
#             title = QApplication.translate('GUI', "New version available")
#             msg = QApplication.translate('GUI', """
# <p>A new version of {0} is available: <b>{1}</b></p>
# <p><a href="http://code.google.com/p/almoviesrenamer/downloads/list">Download it.</a></p>
#             """).format(utils.PROGRAM_NAME, version)
#             # show a notification dialog, with link to download page
#             QMessageBox.information(None, title, msg)
#
#     def show_stats_agreement(self):
#         """
#         shows usage statistics agreement dialog
#         """
#
#         # get if this is the first time user opens the program
#         first_time = utils.preferences.value("first_time").toBool()
#         if first_time:
#             # create agreement dialog
#             stats_agreement_dialog = StatsAgreementDialog(self)
#             # show it
#             stats_agreement_dialog.exec_()
#             # nex time user will open the program, don't show that dialog
#             utils.preferences.setValue("first_time", False)
#
#     #--------------------------------- SLOTS ----------------------------------
#
#     # MENU Movies
#
#     def add_movies(self):
#         """
#         select video files from file system using a FileDialog,
#         then creates corresponding movie objects
#
#         these movies will populate movie table
#
#         get information from selected files
#         """
#
#         # create a filter, only video files can be selected
#         video_filter = QApplication.translate('GUI', "Video (*") + ' *'.join(self.VIDEO_EXTENSIONS) + ')'
#         # dialog title
#         title = QApplication.translate('GUI', "Select movies you want to rename...")
#         # select video files from file system
#         filepaths = QFileDialog.getOpenFileNames(self, title, self.last_visited_directory, video_filter)
#         # if at least one file has been selected
#         if len(filepaths) > 0:
#             self.load_movies(filepaths)
#
#     def add_movies_in_folder(self):
#         """
#         select all video files from a selected folder using a FileDialog,
#         then creates corresponding movie objects
#
#         these movies will populate movie table
#
#         get information from selected files
#         """
#
#         # dialog title
#         title = QApplication.translate('GUI', "Select a folder containing movies...")
#         # select folder from file system
#         dirpath = QFileDialog.getExistingDirectory(self, title, self.last_visited_directory)
#         # if a directory has been selected
#         if dirpath != '':
#             filepaths = []
#             # for each entry (files + folders) in selected folder
#             for entry in os.listdir(dirpath):
#                 entry = os.path.join(dirpath, entry)
#                 # select only video files
#                 extension = os.path.splitext(entry)[1].lower()
#                 if os.path.isfile(entry) and extension in self.VIDEO_EXTENSIONS:
#                     # save entry with path
#                     filepaths.append(entry)
#
#             self.load_movies(filepaths)
#
#     def add_movies_in_folder_subfolders(self):
#         """
#         select all video files from a selected folder and subfolders using a FileDialog,
#         then creates corresponding movie objects
#
#         these movies will populate movie table
#
#         get information from selected files
#         """
#
#         # dialog title
#         title = QApplication.translate('GUI', "Select a folder containing movies...")
#         # select folder from file system
#         dirpath = QFileDialog.getExistingDirectory(self, title, self.last_visited_directory)
#         # if a directory has been selected
#         if dirpath != '':
#             filepaths = []
#             # walk on chosen directory, and loop on files and directories
#             for root, dirs, files in os.walk(dirpath):
#                 # for each file
#                 for name in files:
#                     entry = os.path.join(root, name)
#                     # select only video files
#                     extension = os.path.splitext(name)[1].lower()
#                     if extension in self.VIDEO_EXTENSIONS:
#                         # save entry with path
#                         filepaths.append(entry)
#
#             self.load_movies(filepaths)
#
#     def load_movies(self, filepaths):
#         """
#         given a list of file paths, creates a movie object for each
#         file, get info from it, and populate movies table
#         """
#
#         # takes first selected file and get the file path, use it as the last visited directory
#         self.last_visited_directory = os.path.normpath(os.path.split(filepaths[0])[0])
#         # save it in settings
#         utils.preferences.setValue("last_visited_directory", self.last_visited_directory)
#         # disable gui elements which cannot be used during loading
#         self.set_gui_enabled_load_movies(False)
#         # show loading panel
#         self.ui.panel_loading.setVisible(True)
#         # start loading thread
#         threading.Thread(target = self.load_movies_run, args = (filepaths,)).start()
#
#     def load_movies_run(self, filepaths):
#         renaming_rule = utils.preferences.value("renaming_rule").toString()
#         # loop on file paths
#         for filepath in filepaths:
#             # set loading label text, show current file name
#             self.ui.label_loading.setText(QApplication.translate('GUI', "Getting information from ")\
#                                            + os.path.split(filepath)[1])
#             # create a new movie object
#             movie = Movie(filepath)
#             # generate new movie name based on renaming rule
#             movie.generate_new_name(renaming_rule)
#             # add movie to list
#             self.movies.append(movie)
#             # insert a new row in movie table
#             self.ui.table_movies.insertRow(self.ui.table_movies.rowCount())
#             # create a table item with original movie file name
#             item_original_name = QTableWidgetItem(movie.original_file_name())
#             item_original_name.setForeground(QBrush(Qt.black))
#             self.ui.table_movies.setItem(self.ui.table_movies.rowCount() - 1, 0, item_original_name)
#             # create a table item with new movie file name
#             item_new_name = QTableWidgetItem(movie.new_file_name())
#             item_new_name.setForeground(QBrush(Qt.black))
#             self.ui.table_movies.setItem(self.ui.table_movies.rowCount() - 1, 1, item_new_name)
#         self.load_movies_finished.emit()
#
#     def load_movies_end(self):
#         # re-enable gui elements
#         self.set_gui_enabled_load_movies(True)
#         # auto resize table columns
#         self.ui.table_movies.resizeColumnToContents(0)
#         # hide loading panel
#         self.ui.panel_loading.setVisible(False)
#         # play a sound
#         QApplication.beep()
#
#     def set_gui_enabled_load_movies(self, enabled):
#         # set enabled property on actions
#         self.ui.action_add_movies.setEnabled(enabled)
#         self.ui.action_add_all_movies_in_folder.setEnabled(enabled)
#         self.ui.action_add_all_movies_in_folder_subfolders.setEnabled(enabled)
#         self.ui.action_remove_selected_movies.setEnabled(enabled)
#         self.ui.action_remove_all_movies.setEnabled(enabled)
#         self.ui.action_change_renaming_rule.setEnabled(enabled)
#         self.ui.action_rename_movies.setEnabled(enabled)
#         self.ui.action_preferences.setEnabled(enabled)
#         if enabled == False:
#             # clear table selection (and hide movie panel, if visible)
#             self.ui.table_movies.selectionModel().clear()
#         # set enabled property on table
#         self.ui.table_movies.setEnabled(enabled)
#
#     def remove_selected_movies(self):
#         """
#         removes selected movies from movies table
#         """
#
#         # get selected items
#         selected_items = self.ui.table_movies.selectionModel().selectedRows()
#         # loop on items
#         for item in reversed(selected_items):
#             # get item row
#             row = item.row()
#             # first remove items from table
#             self.ui.table_movies.takeItem(row, 0)
#             self.ui.table_movies.takeItem(row, 1)
#             # them remove corresponding row
#             self.ui.table_movies.removeRow(row)
#             # delete movie item
#             del self.movies[row]
#
#     def remove_all_movies(self):
#         """
#         removes all movies from movies table
#         """
#
#         del self.movies[:]
#         # clear table contents
#         self.ui.table_movies.clearContents()
#         # remove all rows
#         self.ui.table_movies.setRowCount(0)
#
#     def change_renaming_rule(self):
#         """
#         show renaming rule dialog
#         """
#
#         self.ui.table_movies.clearSelection()
#         #show renaming rule dialog
#         self.ui.renaming_rule_dialog.exec_()
#         renaming_rule = utils.preferences.value("renaming_rule").toString()
#         # loop on movies
#         for i in range(len(self.movies)):
#             movie = self.movies[i]
#             # generate new movie name based on new renaming rule
#             movie.generate_new_name(renaming_rule)
#             # set "before renaming state", because after renaming a movie
#             # can be renamed a second time, after having changed the rule
#             movie.set_state(Movie.STATE_BEFORE_RENAMING)
#             self.ui.table_movies.item(i, 1).setForeground(QBrush(Qt.black))
#             self.ui.table_movies.item(i, 1).setText(movie.new_file_name())
#
#     def rename_movies(self):
#         """
#         rename files with new name
#         """
#
#         self.ui.table_movies.clearSelection()
#         # loop on movies
#         for i in range(len(self.movies)):
#             movie = self.movies[i]
#             # check if new title is a valid file name
#             if movie.check_and_clean_new_name():
#                 # set "new name" table item with new movie name
#                 self.ui.table_movies.item(i, 1).setText(movie.new_file_name())
#                 try:
#                     # rename file
#                     os.rename(movie.abs_original_file_name(), movie.abs_new_file_name())
#                 except OSError as e:
#                     # set state and renaming error
#                     movie.set_state(Movie.STATE_RENAMING_ERROR, e.strerror)
#                     # paint "new name" table item with red
#                     self.ui.table_movies.item(i, 1).setForeground(QBrush(Qt.red))
#                 else:
#                     # correctly renamed
#                     movie.set_state(Movie.STATE_RENAMED)
#                     # set "original name" table item with new movie name
#                     self.ui.table_movies.item(i, 0).setText(movie.new_file_name())
#                     # paint "new name" table item with green
#                     self.ui.table_movies.item(i, 1).setForeground(QBrush(Qt.darkGreen))
#
#     # MENU Program
#
#     def show_preferences(self):
#         #show renaming rule dialog
#         self.ui.preferences_dialog.exec_()
#         renaming_rule = utils.preferences.value("renaming_rule").toString()
#         # loop on movies
#         for i in range(len(self.movies)):
#             movie = self.movies[i]
#             # generate new movie name based on new renaming rule
#             movie.generate_new_name(renaming_rule)
#             # set "before renaming state", because after renaming a movie
#             # can be renamed a second time, after having changed the rule
#             movie.set_state(Movie.STATE_BEFORE_RENAMING)
#             self.ui.table_movies.item(i, 1).setForeground(QBrush(Qt.black))
#             self.ui.table_movies.item(i, 1).setText(movie.new_file_name())
#
#     def show_about(self):
#         """
#         shows an about dialog, with info on program
#         """
#
#         # message shown on about dialog
#         msg = QApplication.translate('GUI', """
# <p>
#     <b>{0}</b>
# </p>
# <p>
#     Version: {1}<br />
#     License: GNU General Public License version 3 (GPLv3)
# </p>
# <p>
#     Programmed by: Alberto Malagoli<br />
#     Email: <a href="mailto:albemala@gmail.com">albemala@gmail.com</a>
# </p>
# <p>
#     Libraries:
#     <ul>
#         <li>
#             <a href="http://www.python.org/">Python</a>: {2}
#         </li>
#         <li>
#             <a href="http://www.riverbankcomputing.co.uk/software/pyqt/download">PyQt</a>: {3}
#         </li>
#         <li>
#             <a href="http://imdbpy.sourceforge.net/">IMDbPY</a>: {4}
#         </li>
#         <li>
#             <a href="https://github.com/Diaoul/enzyme">enzyme</a>: 0.2
#         </li>
#         <li>
#             <a href="http://cx-freeze.sourceforge.net/">cx-Freeze</a>: 4.2.3
#         </li>
#     </ul>
# </p>
# <p>
#     Thanks to:
#     <ul>
#         <li>
#             <a href="http://www.imdbapi.com/">The IMDb API</a>, which is used to retrieve movies information<br>
#             <b>Please donate to support this service!</b>
#         </li>
#         <li>
#             <a href="http://file-folder-ren.sourceforge.net/">M\xe9tamorphose</a> for some stolen code :)
#         </li>
#         <li>
#         <a href="http://p.yusukekamiyamane.com/">Yusuke Kamiyamane</a> for Fugue Icons
#         </li>
#     </ul>
# </p>
#         """).format(utils.PROGRAM_NAME, utils.PROGRAM_VERSION, platform.python_version(), PYQT_VERSION_STR, imdb.VERSION)
#         # show the about dialog
#         QMessageBox.about(self, QApplication.translate('GUI', "About {0}").format(utils.PROGRAM_NAME), msg)
#
#     # TABLE movies
#
#     def movies_selection_changed(self):
#         """
#         called when selection in table_movies changes, i.e. user selects
#         different movies from previously selected ones.
#         """
#
#         selected_items = self.ui.table_movies.selectedItems()
#         # no movies selected
#         if len(selected_items) == 0:
#             self.current_movie = None
#             # hide movie panel
#             self.ui.stack_movie.setVisible(False)
#         else:
#             # store first selected movie
#             index = selected_items[0].row()
#             self.current_movie = self.movies[index]
#             movie = self.current_movie
#
#             # set movie panel based on movie state (
#             self.ui.stack_movie.setCurrentIndex(movie.state())
#             # populate movie panel
#             if movie.state() == Movie.STATE_RENAMING_ERROR:
#                 self.ui.label_error.setText("""
#                 <html><head/><body><p><span style="font-size:11pt; font-weight:400; color:#ff0000;">
#                 """
#                 + movie.renaming_error() +
#                 """
#                 </span></p></body></html>
#                 """)
#             elif movie.state() == Movie.STATE_BEFORE_RENAMING:
#                 self.populate_movie_panel()
#                 self.ui.stack_search_title.setCurrentIndex(0)
#                 self.ui.text_search_title.clear()
#
#             # set panel visible
#             self.ui.stack_movie.setVisible(True)
#
#     def movie_double_clicked(self, item):
#         """
#         when a movie item is double clicked in table,
#         it opens operative system file manager
#         with file location on disk
#         """
#
#         movie = self.movies[item.row()]
#         path = movie.abs_original_file_path()
#         self.open_path(path)
#
#     def open_containing_folder(self):
#         movie = self.current_movie
#         if movie != None:
#             path = movie.abs_original_file_path()
#             self.open_path(path)
#
#     def open_path(self, path):
#         """
#         opens a path using the operative system file manager/explorer
#         """
#         QDesktopServices.openUrl(QUrl('file:///' + path))
#
#     def copy_title(self):
#         """
#         copy selected movie title in movie table
#         into clipboard
#         """
#
#         movie = self.current_movie
#         if movie != None:
#             clipboard = QApplication.clipboard()
#             clipboard.setText(movie.original_file_name())
#
#     def populate_movie_panel(self):
#         movie = self.current_movie
#
#         self.ui.label_title.setText(movie.title())
#         self.ui.label_original_title.setText(movie.original_title())
#         self.ui.label_year.setText(movie.year())
#         self.ui.label_director.setText(movie.director())
#         self.ui.label_duration.setText(movie.duration())
#         language = movie.language()
#         if movie.subtitles() != '':
#             language += " (subtitled " + movie.subtitles() + ")"
#         self.ui.label_language.setText(language)
#
#         # clear table contents
#         self.ui.table_others_info.clearContents()
#         # remove all rows
#         self.ui.table_others_info.setRowCount(0)
#         for other_info in movie.others_info():
#             title = other_info[0]
#             language = other_info[1]
#             # insert a new row in movie table
#             self.ui.table_others_info.insertRow(self.ui.table_others_info.rowCount())
#             # create a table item with original movie file name
#             item_title = QTableWidgetItem(title)
#             self.ui.table_others_info.setItem(self.ui.table_others_info.rowCount() - 1, 0, item_title)
#             item_language = QTableWidgetItem(language)
#             self.ui.table_others_info.setItem(self.ui.table_others_info.rowCount() - 1, 1, item_language)
#         # auto resize table columns
#         self.ui.table_others_info.resizeColumnToContents(0)
#
#     # PANEL movie
#
#     def alternative_movies_selection_changed(self):
#         selected_info = self.ui.table_others_info.selectedItems()
#         if len(selected_info) > 0:
#             info_index = selected_info[0].row()
#             movie = self.current_movie
#             movie.set_movie(info_index)
#             renaming_rule = utils.preferences.value("renaming_rule").toString()
#             # generate new movie name based on renaming rule
#             movie.generate_new_name(renaming_rule)
#             # create a table item with new movie file name
#             item_new_name = QTableWidgetItem(movie.new_file_name())
#             selected_movie = self.ui.table_movies.selectedItems()[0]
#             # store first selected movie
#             movie_index = selected_movie.row()
#             self.ui.table_movies.setItem(movie_index, 1, item_new_name)
#             # update labels in movie panel
#             self.ui.label_title.setText(movie.title())
#             self.ui.label_original_title.setText(movie.original_title())
#             self.ui.label_year.setText(movie.year())
#             self.ui.label_director.setText(movie.director())
#             self.ui.label_duration.setText(movie.duration())
#             self.ui.label_language.setText(movie.language())
#
#     def search_new_title(self):
#         # get title to look for
#         title = unicode(self.ui.text_search_title.text())
#         # do not start searching if textTitleSearch is empty
#         if title.strip() == '':
#             return
#         # set gui elements disabled
#         self.set_gui_enabled_search_title(False)
#         self.ui.label_searching.setText(QApplication.translate('GUI', "Searching ") + title + "...")
#         # show searching panel
#         self.ui.stack_search_title.setCurrentIndex(1)
#         # start searching thread
#         threading.Thread(target = self.search_title_run, args = (title,)).start()
#
#     def search_title_run(self, title):
#         """
#         thread used for movie title searching
#         """
#
#         self.current_movie.search_new_title(title)
#         # emit signal
#         self.search_title_finished.emit()
#
#     def search_title_end(self):
#         """
#         used when movie title searching finishes (thread returns)
#         """
#
#         # re-enable gui elements
#         self.set_gui_enabled_search_title(True)
#         renaming_rule = utils.preferences.value("renaming_rule").toString()
#         # generate new movie name based on renaming rule
#         movie = self.current_movie
#         movie.generate_new_name(renaming_rule)
#         # create a table item with new movie file name
#         item_new_name = QTableWidgetItem(movie.new_file_name())
#         selected_movie = self.ui.table_movies.selectedItems()[0]
#         # store first selected movie
#         movie_index = selected_movie.row()
#         self.ui.table_movies.setItem(movie_index, 1, item_new_name)
#         self.populate_movie_panel()
#         self.ui.stack_search_title.setCurrentIndex(0)
#
#     def set_gui_enabled_search_title(self, enabled):
#         # set enabled property on actions
#         self.ui.action_add_movies.setEnabled(enabled)
#         self.ui.action_add_all_movies_in_folder.setEnabled(enabled)
#         self.ui.action_add_all_movies_in_folder_subfolders.setEnabled(enabled)
#         self.ui.action_remove_selected_movies.setEnabled(enabled)
#         self.ui.action_remove_all_movies.setEnabled(enabled)
#         self.ui.action_change_renaming_rule.setEnabled(enabled)
#         self.ui.action_rename_movies.setEnabled(enabled)
#         self.ui.action_preferences.setEnabled(enabled)
#         # set enabled property on table
#         self.ui.table_movies.setEnabled(enabled)
#
#         self.ui.table_others_info.setEnabled(enabled)

