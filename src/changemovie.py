# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QSettings, pyqtSignal, Qt
from PyQt4.QtGui import QDialog
from PyQt4.uic import loadUi
import threading

class ChangeMovieDialog(QDialog):

    search_title_finished = pyqtSignal()

    def __init__(self, parent):
        QDialog.__init__(self, parent)

        # load UI
        self.ui = loadUi("ui/change_movie_dialog.ui", self)

        ## slots connection
#        self.ui.button_search_alternative_title.clicked.connect(self.search_alternative_title)
        self.ui.text_search_title.returnPressed.connect(self.search_new_title)
        self.ui.button_search_title.clicked.connect(self.search_new_title)
        self.ui.button_keep_new_movie.clicked.connect(self.keep_new_movie)
        self.ui.button_close.clicked.connect(self.close) #XXX uso del signal in designer?

#        self.finished.connect(self.return_result)

        self.search_title_finished.connect(self.search_title_end)

    def exec2(self, movie):
        self.movie = movie
        self.ui.label_file_name.setText(movie.original_name)
        current_movie = \
            unicode(movie.info['title']) + \
            ' / ' + \
            unicode(movie.info['aka']) + \
            ' / ' + \
            unicode(movie.info['year'])
        self.ui.label_current_movie.setText(current_movie)
        self.ui.label_alternative_title.setText(movie.info['alternative_title'])

        self.ui.text_search_title.setText('')
        self.ui.stack_title_search.setVisible(False)
        # adjust wondow size to content
        self.adjustSize()

        return self.exec_()

#    def search_alternative_title(self):
#        """
#        """
#        self.search_title(None)

    def search_new_title(self):
        # get title to look for
        title = unicode(self.ui.text_search_title.text())
        # do not start searching if textTitleSearch is empty
        if title.strip() == '':
            return
        self.search_title(title)

    def search_title(self, title):
        """
        """

        # set gui elements disabled
        self.set_gui_enabled(False)
        # show searching panel
        self.ui.stack_title_search.setCurrentIndex(0)
        self.ui.stack_title_search.setVisible(True)
        # start searching thread
        threading.Thread(target = self.search_title_run, args = (title,)).start()

    def search_title_run(self, title):
        """
        thread used for movie title searching
        """

        if title == None:
            self.movie_info = self.movie.search_alternative_title()
        else:
            self.movie_info = self.movie.search_new_title(title)
        # emit signal
        self.search_title_finished.emit()

    def search_title_end(self):
        """
        used when movie title searching finishes (thread returns)
        """

        # re-enable gui elements
        self.set_gui_enabled(True)
        # no corresponding movie found
        if self.movie_info == None:
            # set failed search_title_run panel
            self.ui.stack_title_search.setCurrentIndex(2)
            # select all text in searching text field
            self.ui.text_search_title.selectAll()
            # set focus on searching text field
            self.ui.text_search_title.setFocus()
        else:
            info = self.movie_info
            # populate movie panel
            #XXX qui devo usare gli indici scelti nelle preferenze
            self.ui.label_title.setText(info['title'][0])
            self.ui.label_aka.setText(info['aka'])
            self.ui.label_year.setText(info['year'])
            self.ui.label_director.setText(info['director'])
            self.ui.label_duration.setText(info['duration'][0])
            #XXX per la lingua dovrei creare un'altra chiave per memorizzare 
            # la versione di guessit, e nella chiave language ci metto le due versioni
            # in formato stringa
#            self.ui.label_language.setText(info['language'][0])
            self.ui.stack_title_search.setCurrentIndex(1)

    def set_gui_enabled(self, enabled):
        self.ui.button_search_alternative_title.setEnabled(enabled)
        self.ui.text_search_title.setEnabled(enabled)
        self.ui.button_search_title.setEnabled(enabled)

    def keep_new_movie(self):
        """
        """

        self.accept()

    def close(self):
        """
        """

        self.reject()

    def keyPressEvent(self, e):
        pass

#    def return_result(self, result):
#        print(self.movie_info)


