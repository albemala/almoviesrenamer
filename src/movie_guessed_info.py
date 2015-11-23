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
        # TODO expose other properties: country, bonus title, cd number total, edition
        self.__title = ""
        self.__year = ""
        # Country(ies) of content. [<babelfish.Country>] (This class equals name and iso code)
        self.__country = ""
        # Language(s) of the audio soundtrack. [<babelfish.Language>] (This class equals name and iso code)
        self.__language = ""
        # Language(s) of the subtitles. [<babelfish.Language>] (This class equals name and iso code)
        self.__subtitle_language = ""
        self.__bonus_title = ""
        self.__cd_number = ""
        self.__cd_number_total = ""
        # Special Edition, Collector Edition, Director's cut, Criterion Edition, Deluxe Edition
        self.__edition = ""

    def get_title(self) -> str:
        return self.__title

    def get_year(self) -> str:
        return self.__year

    def get_country(self) -> str:
        return self.__country

    def get_language(self) -> str:
        return self.__language

    def get_subtitle_language(self) -> str:
        return self.__subtitle_language

    def get_bonus_title(self) -> str:
        return self.__bonus_title

    def get_cd_number(self) -> str:
        return self.__cd_number

    def get_cd_number_total(self) -> str:
        return self.__cd_number_total

    def get_edition(self) -> str:
        return self.__edition

    def fill_with_absolute_file_path(self, absolute_file_path: str) -> None:
        info = guessit.guess_movie_info(absolute_file_path)
        # print(info)

        if MovieGuessedInfo.TITLE in info:
            self.__title = info[MovieGuessedInfo.TITLE]
        if MovieGuessedInfo.YEAR in info:
            self.__year = str(info[MovieGuessedInfo.YEAR])
        if MovieGuessedInfo.COUNTRY in info:
            self.__country = info[MovieGuessedInfo.COUNTRY][0]
        if MovieGuessedInfo.LANGUAGE in info:
            self.__language = info[MovieGuessedInfo.LANGUAGE][0]
        if MovieGuessedInfo.SUBTITLE_LANGUAGE in info:
            self.__subtitle_language = info[MovieGuessedInfo.SUBTITLE_LANGUAGE][0]
        if MovieGuessedInfo.BONUS_TITLE in info:
            self.__bonus_title = info[MovieGuessedInfo.BONUS_TITLE]
        if MovieGuessedInfo.CD_NUMBER in info:
            self.__cd_number = str(info[MovieGuessedInfo.CD_NUMBER])
        if MovieGuessedInfo.CD_NUMBER_TOTAL in info:
            self.__cd_number_total = str(info[MovieGuessedInfo.CD_NUMBER_TOTAL])
        if MovieGuessedInfo.EDITION in info:
            self.__edition = info[MovieGuessedInfo.EDITION]
