import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from movie_table_item import MovieTableItem


class MainWindowView:
    __MOVIES_TABLE_VIEW_MODEL_CONTEXT_PROPERTY = "moviesTableViewModel"
    __ERROR_PANEL_VISIBLE_CONTEXT_PROPERTY = "movieErrorPanelVisible"
    __RENAMED_PANEL_VISIBLE_CONTEXT_PROPERTY = "movieRenamedPanelVisible"
    __MOVIE_INFO_PANEL_VISIBLE_CONTEXT_PROPERTY = "movieInfoPanelVisible"
    __LOADING_PANEL_VISIBLE_CONTEXT_PROPERTY = "loadingPanelVisible"
    __LOADING_FILE_NAME_CONTEXT_PROPERTY = "loadingFileName"

    def __init__(self):
        self.__loading_file_name = ""
        self.__loading_panel_visible = True
        self.__movies_table_view_model = []
        self.__movie_info_panel_visible = True
        self.__movie_renamed_panel_visible = True
        self.__movie_error_panel_visible = True

        self.__engine = QQmlApplicationEngine()

        self.__set_context_property(MainWindowView.__LOADING_FILE_NAME_CONTEXT_PROPERTY,
                                    self.__loading_file_name)
        self.__set_context_property(MainWindowView.__LOADING_PANEL_VISIBLE_CONTEXT_PROPERTY,
                                    self.__loading_panel_visible)
        self.__set_context_property(MainWindowView.__MOVIE_INFO_PANEL_VISIBLE_CONTEXT_PROPERTY,
                                    self.__movie_info_panel_visible)
        self.__set_context_property(MainWindowView.__RENAMED_PANEL_VISIBLE_CONTEXT_PROPERTY,
                                    self.__movie_renamed_panel_visible)
        self.__set_context_property(MainWindowView.__ERROR_PANEL_VISIBLE_CONTEXT_PROPERTY,
                                    self.__movie_error_panel_visible)
        self.__set_context_property(MainWindowView.__MOVIES_TABLE_VIEW_MODEL_CONTEXT_PROPERTY,
                                    self.__movies_table_view_model)

        self.__engine.load("main_window.qml")

    def __set_context_property(self, name, value):
        self.__engine.rootContext().setContextProperty(name, value)

    def set_loading_file_name(self, loading_file_name: str) -> None:
        self.__loading_file_name = loading_file_name
        self.__set_context_property(MainWindowView.__LOADING_FILE_NAME_CONTEXT_PROPERTY,
                                    self.__loading_file_name)

    def set_loading_panel_visible(self, loading_panel_visible: bool) -> None:
        self.__loading_panel_visible = loading_panel_visible
        self.__set_context_property(MainWindowView.__LOADING_PANEL_VISIBLE_CONTEXT_PROPERTY,
                                    self.__loading_panel_visible)

    def set_movie_info_panel_visible(self, movie_info_panel_visible: bool) -> None:
        self.__movie_info_panel_visible = movie_info_panel_visible
        self.__set_context_property(MainWindowView.__MOVIE_INFO_PANEL_VISIBLE_CONTEXT_PROPERTY,
                                    self.__movie_info_panel_visible)

    def set_movie_renamed_panel_visible(self, movie_renamed_panel_visible: bool) -> None:
        self.__movie_renamed_panel_visible = movie_renamed_panel_visible
        self.__set_context_property(MainWindowView.__RENAMED_PANEL_VISIBLE_CONTEXT_PROPERTY,
                                    self.__movie_renamed_panel_visible)

    def set_movie_error_panel_visible(self, movie_error_panel_visible: bool) -> None:
        self.__movie_error_panel_visible = movie_error_panel_visible
        self.__set_context_property(MainWindowView.__ERROR_PANEL_VISIBLE_CONTEXT_PROPERTY,
                                    self.__movie_error_panel_visible)

    def add_movie_table_item(self, original_name: str, new_name: str) -> None:
        movie_table_item = MovieTableItem(original_name, new_name)
        self.__movies_table_view_model.append(movie_table_item)
        # From Qt Documentation:
        # Note: There is no way for the view to know that the contents of a QList has changed.
        # If the QList changes, it is necessary to reset the model by calling QQmlContext::setContextProperty() again.
        self.__set_context_property(MainWindowView.__MOVIES_TABLE_VIEW_MODEL_CONTEXT_PROPERTY,
                                    self.__movies_table_view_model)


app = QGuiApplication(sys.argv)

main_window_view = MainWindowView()
main_window_view.set_loading_file_name("aaaaaaaa")
main_window_view.add_movie_table_item("Item 1", "red")
main_window_view.add_movie_table_item("Item 2", "green")
main_window_view.add_movie_table_item("Item 3", "blue")
main_window_view.add_movie_table_item("Item 4", "yellow")

sys.exit(app.exec_())
