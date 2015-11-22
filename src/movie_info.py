from movie_guessed_info import MovieGuessedInfo

__author__ = "Alberto Malagoli"


class MovieInfo:
    def __init__(self):
        self._title = ""
        self._original_title = ""
        self._year = ""
        self._director = ""
        self._duration = ""
        self._languages = [""]
        self._subtitle_languages = [""]
        self._part = ""
        self._score = ""

    def get_title(self):
        return self._title

    def get_original_title(self):
        """
        return the original movie title, in the original language

        e.g.: the original movie title for Deep Red from Dario Argento, in italian
        language, is Profondo Rosso
        """
        return self._original_title

    def get_year(self):
        return self._year

    def get_directors(self):
        return self._director

    def get_duration(self):
        return self._duration

    def get_language(self, index: int = 0):
        return self._languages[index]

    def get_subtitle_language(self, index: int = 0):
        return self._subtitle_languages[index]

    def get_part(self):
        return self._part

    def get_score(self):
        return self._score

    def fill_with_guessed_info(self, guessed_info: MovieGuessedInfo):
        self._title = guessed_info.get_title()
        self._original_title = self._title
        self._year = guessed_info.get_year()
        self._languages = guessed_info.get_languages()
        self._subtitle_languages = guessed_info.get_subtitle_languages()
        self._part = guessed_info.get_cd_number()
