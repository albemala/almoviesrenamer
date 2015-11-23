import guessit

__author__ = "Alberto Malagoli"


class MovieGuessedInfo:
    TITLE = "title"
    YEAR = "year"
    COUNTRY = "country"
    LANGUAGE = "language"
    SUBTITLE_LANGUAGE = "subtitleLanguage"
    BONUS_TITLE = "bonusTitle"
    CD_NUMBER = "cdNumber"
    CD_NUMBER_TOTAL = "cdNumberTotal"
    EDITION = "edition"

    def __init__(self):
        # TODO expose other properties: country, bonus title, cd nuber title, edition
        self._title = ""
        self._year = ""
        # Country(ies) of content. [<babelfish.Country>] (This class equals name and iso code)
        self._countries = [""]
        # Language(s) of the audio soundtrack. [<babelfish.Language>] (This class equals name and iso code)
        self._languages = [""]
        # Language(s) of the subtitles. [<babelfish.Language>] (This class equals name and iso code)
        self._subtitle_languages = [""]
        self._bonus_title = ""
        self._cd_number = ""
        self._cd_number_total = ""
        # Special Edition, Collector Edition, Director's cut, Criterion Edition, Deluxe Edition
        self._edition = ""

    def get_title(self):
        return self._title

    def get_year(self):
        return self._year

    def get_countries(self):
        return self._countries

    def get_languages(self):
        return self._languages

    def get_subtitle_languages(self):
        return self._subtitle_languages

    def get_bonus_title(self):
        return self._bonus_title

    def get_cd_number(self):
        return self._cd_number

    def get_cd_number_total(self):
        return self._cd_number_total

    def get_edition(self):
        return self._edition

    def fill_with_absolute_file_path(self, absolute_file_path):
        info = guessit.guess_movie_info(absolute_file_path)
        print(info)

        if MovieGuessedInfo.TITLE in info:
            self._title = info[MovieGuessedInfo.TITLE]
        if MovieGuessedInfo.YEAR in info:
            self._year = str(info[MovieGuessedInfo.YEAR])
        if MovieGuessedInfo.COUNTRY in info:
            self._countries = info[MovieGuessedInfo.COUNTRY]
        if MovieGuessedInfo.LANGUAGE in info:
            self._languages = info[MovieGuessedInfo.LANGUAGE]
        if MovieGuessedInfo.SUBTITLE_LANGUAGE in info:
            self._subtitle_languages = info[MovieGuessedInfo.SUBTITLE_LANGUAGE]
        if MovieGuessedInfo.BONUS_TITLE in info:
            self._bonus_title = info[MovieGuessedInfo.BONUS_TITLE]
        if MovieGuessedInfo.CD_NUMBER in info:
            self._cd_number = str(info[MovieGuessedInfo.CD_NUMBER])
        if MovieGuessedInfo.CD_NUMBER_TOTAL in info:
            self._cd_number_total = str(info[MovieGuessedInfo.CD_NUMBER_TOTAL])
        if MovieGuessedInfo.EDITION in info:
            self._edition = info[MovieGuessedInfo.EDITION]
