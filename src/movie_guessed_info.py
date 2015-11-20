import guessit

__author__ = "Alberto Malagoli"


class MovieGuessedInfo:
    TITLE = "title"
    YEAR = "year"
    COUNTRY = "Country"
    LANGUAGE = "Language"
    SUBTITLE_LANGUAGE = "subtitleLanguage"
    BONUS_TITLE = "bonusTitle"
    CD_NUMBER = "cdNumber"
    CD_NUMBER_TOTAL = "cdNumberTotal"
    EDITION = "edition"

    def __init__(self, absolute_file_path):
        self._title = None
        self._year = None
        # Country(ies) of content. [<babelfish.Country>] (This class equals name and iso code)
        self._country = None
        # Language(s) of the audio soundtrack. [<babelfish.Language>] (This class equals name and iso code)
        self._language = None
        # Language(s) of the subtitles. [<babelfish.Language>] (This class equals name and iso code)
        self._subtitle_language = None
        self._bonus_title = None
        self._cd_number = None
        self._cd_number_total = None
        # Special Edition, Collector Edition, Director's cut, Criterion Edition, Deluxe Edition
        self._edition = None

        info = guessit.guess_movie_info(absolute_file_path)
        print(info)

        if MovieGuessedInfo.TITLE in info:
            self._title = info[MovieGuessedInfo.TITLE]
        if MovieGuessedInfo.YEAR in info:
            self._year = info[MovieGuessedInfo.YEAR]
        if MovieGuessedInfo.COUNTRY in info:
            self._country = info[MovieGuessedInfo.COUNTRY]
        if MovieGuessedInfo.LANGUAGE in info:
            self._language = info[MovieGuessedInfo.LANGUAGE]
        if MovieGuessedInfo.SUBTITLE_LANGUAGE in info:
            self._subtitle_language = info[MovieGuessedInfo.SUBTITLE_LANGUAGE]
        if MovieGuessedInfo.BONUS_TITLE in info:
            self._bonus_title = info[MovieGuessedInfo.BONUS_TITLE]
        if MovieGuessedInfo.CD_NUMBER in info:
            self._cd_number = info[MovieGuessedInfo.CD_NUMBER]
        if MovieGuessedInfo.CD_NUMBER_TOTAL in info:
            self._cd_number_total = info[MovieGuessedInfo.CD_NUMBER_TOTAL]
        if MovieGuessedInfo.EDITION in info:
            self._edition = info[MovieGuessedInfo.EDITION]

    def get_title(self):
        if self._title is None:
            return ""
        return self._title

    def get_year(self):
        if self._year is None:
            return ""
        return self._year

    def get_country(self):
        if self._country is None:
            return ""
        return self._country

    def get_language(self):
        if self._language is None:
            return ""
        return self._language

    def get_subtitle_language(self):
        if self._subtitle_language is None:
            return ""
        return self._subtitle_language

    def get_bonus_title(self):
        if self._bonus_title is None:
            return ""
        return self._bonus_title

    def get_cd_number(self):
        if self._cd_number is None:
            return ""
        return self._cd_number

    def get_cd_number_total(self):
        if self._cd_number_total is None:
            return ""
        return self._cd_number_total

    def get_edition(self):
        if self._edition is None:
            return ""
        return self._edition
