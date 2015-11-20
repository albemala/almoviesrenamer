from movie_guessed_info import MovieGuessedInfo

__author__ = "Alberto Malagoli"


class MovieInfo:
    def __init__(self):
        self._title = ""
        self._original_title = ""
        self._year = ""
        self._directors = ""
        self._duration = ""
        self._language = []
        self._subtitles = []
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
        return self._directors

    def get_duration(self):
        return self._duration

    def get_language(self):
        if len(self._language) == 0:
            return ""
        return self._language[0]

    def get_subtitles(self):
        if len(self._subtitles) == 0:
            return ""
        return self._subtitles[0]

    def get_part(self):
        return self._part

    def get_score(self):
        return self._score

    def fill_with_guessed_info(self, guessed_info: MovieGuessedInfo):
        self._title = guessed_info.get_title()
        self._original_title = self._title
        self._year = guessed_info.get_year()
        self._language = guessed_info.get_language()
        self._subtitles = guessed_info.get_subtitle_language()
        self._part = guessed_info.get_cd_number()
