from PyQt5.QtGui import QWindow

from PyQt5.QtQml import QQmlApplicationEngine
from movie_table_item import MovieTableItem

LOADING_PANEL_VISIBLE_PROPERTY = "loadingPanelVisible"
LOADING_PANEL_MOVIE_TITLE_PROPERTY = "loadingPanelMovieTitle"

MOVIES_TABLE_MODEL_PROPERTY = "moviesTableModel"
MOVIES_TABLE_CURRENT_ROW_PROPERTY = "moviesTableCurrentRow"
MOVIES_TABLE_SELECTION_PROPERTY = "moviesTableSelection"

MOVIE_INFO_PANEL_VISIBLE_PROPERTY = "movieInfoPanelVisible"

MOVIE_ALTERNATIVE_TITLES_MODEL_PROPERTY = "movieAlternativeTitlesModel"
MOVIE_ALTERNATIVE_TITLE_INDEX_PROPERTY = "movieAlternativeTitleIndex"

MOVIE_TITLE_PROPERTY = "movieTitle"
MOVIE_ORIGINAL_TITLE_PROPERTY = "movieOriginalTitle"
MOVIE_YEAR_PROPERTY = "movieYear"
MOVIE_DIRECTORS_PROPERTY = "movieDirectors"
MOVIE_DURATION_PROPERTY = "movieDuration"
MOVIE_LANGUAGE_PROPERTY = "movieLanguage"

MOVIE_SEARCH_PROGRESS_BAR_VISIBLE_PROPERTY = "searchAlternativeMovieProgressBarVisible"
MOVIE_SEARCH_ALTERNATIVE_TITLE_PROPERTY = "searchAlternativeTitle"
MOVIE_SEARCH_ALTERNATIVE_YEAR_PROPERTY = "searchAlternativeYear"
MOVIE_SEARCH_ALTERNATIVE_LANGUAGE_PROPERTY = "searchAlternativeLanguage"

MOVIE_RENAMED_PANEL_VISIBLE_PROPERTY = "movieRenamedPanelVisible"

MOVIE_ERROR_PANEL_VISIBLE_PROPERTY = "movieErrorPanelVisible"
MOVIE_ERROR_PROPERTY = "movieError"


class MainWindowView:
    def __init__(self):
        self.__movies_table_view_model = []

        self.__engine = QQmlApplicationEngine()
        self.__engine.load("ui/main_window.qml")

    def __get_root_window(self) -> QWindow:
        return self.__engine.rootObjects()[0]

    def __get_property(self, property_name: str):
        return self.__get_root_window().property(property_name)

    def __set_property(self, property_name: str, property_value):
        return self.__get_root_window().setProperty(property_name, property_value)

    def get_movies_table_current_row(self) -> int:
        return self.__get_property(MOVIES_TABLE_CURRENT_ROW_PROPERTY)

    def get_movies_table_selection(self) -> [int]:
        selection = self.__get_property(MOVIES_TABLE_SELECTION_PROPERTY)
        # QJSValue to QVariant
        variant = selection.toVariant()
        # with a multiple selection, variant is a list of float
        indices = []
        for i in variant:
            # float to int
            indices.append(int(i))
        return indices

    def get_movie_search_alternative_title(self) -> str:
        return self.__get_property(MOVIE_SEARCH_ALTERNATIVE_TITLE_PROPERTY)

    def get_movie_search_alternative_year(self) -> str:
        return self.__get_property(MOVIE_SEARCH_ALTERNATIVE_YEAR_PROPERTY)

    def get_movie_search_alternative_language(self) -> str:
        return self.__get_property(MOVIE_SEARCH_ALTERNATIVE_LANGUAGE_PROPERTY)

    def set_loading_panel_movie_title(self, loading_info: str) -> None:
        self.__set_property(LOADING_PANEL_MOVIE_TITLE_PROPERTY, loading_info)

    def set_loading_panel_visible(self, visible: bool) -> None:
        self.__set_property(LOADING_PANEL_VISIBLE_PROPERTY, visible)

    def set_movie_info_panel_visible(self, visible: bool) -> None:
        self.__set_property(MOVIE_INFO_PANEL_VISIBLE_PROPERTY, visible)

    def set_movie_renamed_panel_visible(self, visible: bool) -> None:
        self.__set_property(MOVIE_RENAMED_PANEL_VISIBLE_PROPERTY, visible)

    def set_movie_error_panel_visible(self, visible: bool) -> None:
        self.__set_property(MOVIE_ERROR_PANEL_VISIBLE_PROPERTY, visible)

    def set_movie_search_progress_bar_visible(self, visible: bool) -> None:
        self.__set_property(MOVIE_SEARCH_PROGRESS_BAR_VISIBLE_PROPERTY, visible)

    def add_movie_table_item(self, original_name: str, new_name: str) -> None:
        movie_table_item = MovieTableItem(original_name, new_name)
        self.__movies_table_view_model.append(movie_table_item)
        # From Qt Documentation:
        # Note: There is no way for the view to know that the contents of a QList has changed.
        # If the QList changes, it is necessary to reset the model by calling QQmlContext::setContextProperty() again.
        self.__set_property(MOVIES_TABLE_MODEL_PROPERTY, self.__movies_table_view_model)

    def remove_movie_table_item(self, index: int) -> None:
        del self.__movies_table_view_model[index]
        self.__set_property(MOVIES_TABLE_MODEL_PROPERTY, self.__movies_table_view_model)

    def remove_all_movie_table_items(self) -> None:
        del self.__movies_table_view_model[:]
        self.__set_property(MOVIES_TABLE_MODEL_PROPERTY, self.__movies_table_view_model)

    def set_movie_alternative_titles_model(self, model: []) -> None:
        self.__set_property(MOVIE_ALTERNATIVE_TITLES_MODEL_PROPERTY, model)

    def set_movie_title(self, movie_title: str) -> None:
        self.__set_property(MOVIE_TITLE_PROPERTY, movie_title)

    def set_movie_original_title(self, movie_original_title: str) -> None:
        self.__set_property(MOVIE_ORIGINAL_TITLE_PROPERTY, movie_original_title)

    def set_movie_year(self, movie_year: str) -> None:
        self.__set_property(MOVIE_YEAR_PROPERTY, movie_year)

    def set_movie_directors(self, movie_directors) -> None:
        self.__set_property(MOVIE_DIRECTORS_PROPERTY, movie_directors)

    def set_movie_duration(self, movie_duration) -> None:
        self.__set_property(MOVIE_DURATION_PROPERTY, movie_duration)

    def set_movie_language(self, movie_language) -> None:
        self.__set_property(MOVIE_LANGUAGE_PROPERTY, movie_language)

    def set_movie_alternative_title_index(self, index: int) -> None:
        self.__set_property(MOVIE_ALTERNATIVE_TITLE_INDEX_PROPERTY, index)

    def set_movie_error(self, movie_error: str) -> None:
        self.__set_property(MOVIE_ERROR_PROPERTY, movie_error)

    def get_add_movies_clicked_signal(self):
        return self.__get_root_window().addMoviesClicked

    def get_add_movies_in_folder_clicked_signal(self):
        return self.__get_root_window().addMoviesInFolderClicked

    def get_add_movies_in_folder_and_subfolders_clicked_signal(self):
        return self.__get_root_window().addMoviesInFolderAndSubfoldersClicked

    def get_remove_selected_movies_clicked_signal(self):
        return self.__get_root_window().removeSelectedMoviesClicked

    def get_remove_all_movies_clicked_signal(self):
        return self.__get_root_window().removeAllMoviesClicked

    def get_show_renaming_rule_dialog_clicked_signal(self):
        return self.__get_root_window().showRenamingRuleDialogClicked

    def get_rename_movies_clicked_signal(self):
        return self.__get_root_window().renameMoviesClicked

    def get_movie_item_selected_signal(self):
        return self.__get_root_window().movieSelected

    def get_movie_alternative_title_changed_signal(self):
        return self.__get_root_window().movieAlternativeTitleChanged

    def get_search_movie_clicked_signal(self):
        return self.__get_root_window().searchMovieClicked

    def get_movies_selection_changed_signal(self):
        return self.__get_root_window().moviesSelectionChanged
