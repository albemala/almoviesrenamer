from PyQt5.QtGui import QWindow
from PyQt5.QtQml import QQmlApplicationEngine

from movie_table_item import MovieTableItem


class MainWindowView:
    def __init__(self):
        self.__loading_info = ""
        self.__loading_panel_visible = False
        self.__movies_table_view_model = []
        self.__movie_info_panel_visible = False
        self.__movie_renamed_panel_visible = False
        self.__movie_error_panel_visible = False
        self.__movie_title = ""
        self.__movie_original_title = ""
        self.__movie_year = ""
        self.__movie_alternative_titles_model = []
        self.__movie_alternative_title_index = 0
        self.__movie_error = ""
        self.__search_alternative_movie_progress_bar_visible = False

        self.__engine = QQmlApplicationEngine()

        self.set_loading_info(self.__loading_info)
        self.set_loading_panel_visible(self.__loading_panel_visible)
        self.set_movie_info_panel_visible(self.__movie_info_panel_visible)
        self.set_movie_renamed_panel_visible(self.__movie_renamed_panel_visible)
        self.set_movie_error_panel_visible(self.__movie_error_panel_visible)
        self.set_search_alternative_movie_progress_bar_visible(self.__search_alternative_movie_progress_bar_visible)
        self.set_movie_title(self.__movie_title)
        self.set_movie_original_title(self.__movie_original_title)
        self.set_movie_year(self.__movie_year)
        self.set_movie_error(self.__movie_error)
        self.set_movie_alternative_titles_model(self.__movie_alternative_titles_model)
        self.set_movie_alternative_title_index(self.__movie_alternative_title_index)
        self.__set_context_property("moviesTableViewModel", self.__movies_table_view_model)

        self.__engine.load("ui/main_window.qml")

    def __set_context_property(self, name, value):
        self.__engine.rootContext().setContextProperty(name, value)

    def __get_root_window(self) -> QWindow:
        return self.__engine.rootObjects()[0]

    def get_movies_table_current_row(self) -> int:
        return self.__get_root_window().property("moviesTableCurrentRow").toInt()

    def set_loading_info(self, loading_info: str) -> None:
        self.__loading_info = loading_info
        self.__set_context_property("loadingInfo", self.__loading_info)

    def set_loading_panel_visible(self, visible: bool) -> None:
        self.__loading_panel_visible = visible
        self.__set_context_property("loadingPanelVisible", self.__loading_panel_visible)

    def set_movie_info_panel_visible(self, visible: bool) -> None:
        self.__movie_info_panel_visible = visible
        self.__set_context_property("movieInfoPanelVisible", self.__movie_info_panel_visible)

    def set_movie_renamed_panel_visible(self, visible: bool) -> None:
        self.__movie_renamed_panel_visible = visible
        self.__set_context_property("movieRenamedPanelVisible", self.__movie_renamed_panel_visible)

    def set_movie_error_panel_visible(self, visible: bool) -> None:
        self.__movie_error_panel_visible = visible
        self.__set_context_property("movieErrorPanelVisible", self.__movie_error_panel_visible)

    def set_search_alternative_movie_progress_bar_visible(self, visible: bool) -> None:
        self.__search_alternative_movie_progress_bar_visible = visible
        self.__set_context_property("searchAlternativeMovieProgressBarVisible",
                                    self.__search_alternative_movie_progress_bar_visible)

    def add_movie_table_item(self, original_name: str, new_name: str) -> None:
        movie_table_item = MovieTableItem(original_name, new_name)
        self.__movies_table_view_model.append(movie_table_item)
        # From Qt Documentation:
        # Note: There is no way for the view to know that the contents of a QList has changed.
        # If the QList changes, it is necessary to reset the model by calling QQmlContext::setContextProperty() again.
        self.__set_context_property("moviesTableViewModel", self.__movies_table_view_model)

    def set_movie_alternative_titles_model(self, model: []) -> None:
        self.__movie_alternative_titles_model = model
        self.__set_context_property("movieAlternativeTitlesModel", self.__movie_alternative_titles_model)

    def set_movie_title(self, movie_title: str) -> None:
        self.__movie_title = movie_title
        self.__set_context_property("movieTitle", self.__movie_title)

    def set_movie_original_title(self, movie_original_title: str) -> None:
        self.__movie_original_title = movie_original_title
        self.__set_context_property("movieOriginalTitle", self.__movie_original_title)

    def set_movie_year(self, movie_year: str) -> None:
        self.__movie_year = movie_year
        self.__set_context_property("movieYear", self.__movie_year)

    def set_movie_alternative_title_index(self, index: int) -> None:
        self.__movie_alternative_title_index = index
        self.__set_context_property("movieAlternativeTitleIndex", self.__movie_alternative_title_index)

    def set_movie_error(self, movie_error: str) -> None:
        self.__movie_error = movie_error
        self.__set_context_property("movieError", self.__movie_error)

    def get_add_movie_button_clicked_signal(self):
        """
        :return: signal addMovieButtonClicked()
        """
        return self.__get_root_window().addMovieButtonClicked

    def get_movie_item_selected_signal(self):
        """
        :return: signal movieItemSelected(row)
        """
        return self.__get_root_window().movieItemSelected

    def get_movie_alternative_title_changed_signal(self):
        """
        :return: signal movieAlternativeTitleChanged(index)
        """
        return self.__get_root_window().movieAlternativeTitleChanged

    def get_search_movie_button_clicked_signal(self):
        """
        :return: signal searchMovieButtonClicked()
        """
        return self.__get_root_window().searchMovieButtonClicked
