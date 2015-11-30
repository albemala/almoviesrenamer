import os
import platform
import re
import tmdbsimple as tmdb
from movie_file_info import MovieFileInfo
from movie_guessed_info import MovieGuessedInfo
from movie_info import MovieInfo
from movie_tmdb_info import MovieTMDBInfo
from preferences import preferences, Preferences

__author__ = "Alberto Malagoli"


class Movie:
    """
    class representing a movie

    movies are shown in movies table
    """

    STATE_BEFORE_RENAMING = 0
    STATE_RENAMED = 1
    STATE_RENAMING_ERROR = 2

    def __init__(self, absolute_file_path=None):
        """
        constructor.

        takes the complete movie file path, or nothing if you want to create
        a movie example
        """

        self.__file_info = MovieFileInfo()
        # current state
        # states are used to show a proper panel in GUI
        self.__renaming_state = self.STATE_BEFORE_RENAMING
        # used to store guessed information from file name
        self.__guessed_info = MovieGuessedInfo()
        # error occurred during renaming operation
        self.__renaming_error = ""
        # movie information fetched from The Movie DB
        self.__tmdb_info = [MovieTMDBInfo()]
        self.__current_info_index = 0

    def fill_with_file(self, absolute_file_path):
        self.__file_info.fill_with_absolute_file_path(absolute_file_path)
        self.__guessed_info.fill_with_absolute_file_path(absolute_file_path)

    def fill_with_example_data(self):
        # TODO if possible, get rid of movie example
        absolute_file_path = "C:/[DivX ITA] A really cool movie (2012).avi"
        self.__file_info.fill_with_absolute_file_path(absolute_file_path)
        self.__guessed_info.fill_with_absolute_file_path(absolute_file_path)
        # self._guessed_info = {
        #     self.SUBTITLES: ["Italian", "ITA"],
        #     self.PART: "1"}
        info = {
            self.TITLE: "Un film molto figo",
            self.ORIGINAL_TITLE: "A really cool movie",
            self.YEAR: "2012",
            self.DIRECTOR: "A. Director",
            self.DURATION: ["100m", '1h40m'],
            self.LANGUAGE: ["Italian", 'ITA'],
            self.SCORE: 1}

    def get_original_name(self) -> str:
        return self.__file_info.get_original_file_name()

    def get_new_name(self) -> str:
        return self.__file_info.get_renamed_file_name()

    def __get_tmdb_info(self) -> MovieTMDBInfo:
        return self.__tmdb_info[self.__current_info_index]

    def get_guessed_info(self) -> MovieGuessedInfo:
        return self.__guessed_info

    def set_current_info_index(self, current_info_index: int):
        self.__current_info_index = current_info_index

    def get_alternative_titles(self) -> []:
        alternative_titles = []
        for tmdb_info in self.__tmdb_info:
            alternative_titles.append(tmdb_info.get_title())
        return alternative_titles

    def get_title(self) -> str:
        title = self.__get_tmdb_info().get_title()
        if title != "":
            return title
        return self.get_guessed_info().get_title()

    def get_original_title(self) -> str:
        """
        return the original movie title, in the original language

        e.g.: the original movie title for Deep Red from Dario Argento, in italian
        language, is Profondo Rosso
        """
        return self.__get_tmdb_info().get_original_title()

    def get_year(self) -> str:
        year = self.__get_tmdb_info().get_year()
        if year != "":
            return year
        return self.get_guessed_info().get_year()

    def get_director(self) -> str:
        return self.__get_tmdb_info().get_director()

    def get_duration(self) -> str:
        """
        duration have 2 representations:
         - minutes only (e.g.: 100m)
         - hours and minutes (e.g.: 1h40m)
        """

        duration_representation = preferences.get_duration_representation()
        duration = self.__get_tmdb_info().get_duration()
        if duration != "":
            if duration_representation == Preferences.DURATION_REPRESENTATION_MINUTES:
                duration += "m"
            elif duration_representation == Preferences.DURATION_REPRESENTATION_HOURS_MINUTES:
                duration_total = int(duration)
                duration_hours = int(duration_total / 60)
                duration_minutes = duration_total % 60
                duration = "{}h{}m".format(duration_hours, duration_minutes)
        return duration

    def get_language(self) -> str:
        # TODO if this is emty, return original language from tmdb info?
        return self.get_guessed_info().get_language()

    def get_subtitle_language(self) -> str:
        return self.get_guessed_info().get_subtitle_language()

    def get_part(self) -> str:
        return self.get_guessed_info().get_cd_number()

    def get_renaming_state(self):
        """
        return current renaming state

        state is one of STATE_BEFORE_RENAMING, STATE_RENAMED, STATE_RENAMING_ERROR
        """

        return self.__renaming_state

    def set_renaming_state(self, state, error=""):
        """
        set state

        state must be one of STATE_BEFORE_RENAMING, STATE_RENAMED, STATE_RENAMING_ERROR

        error could be an error message, used with STATE_RENAMING_ERROR
        """

        self.__renaming_state = state
        self.__renaming_error = error
        # when a file has been renamed, put new name as the original one 
        if state == Movie.STATE_RENAMED:
            self._original_file_name = self._renamed_file_name

    def get_renaming_error(self):
        return self.__renaming_error

    # def set_movie(self, index):
    #     """
    #     set currently associated info, from list of others information
    #     """
    #
    #     self.__info = self.__others_info[index]

    def fetch_tmdb_info(self, query: str, year: str = "", language: str = ""):
        # TODO
        tmdb.API_KEY = "25be8b4eb94ac1d6a4991b76947327ca"
        search = tmdb.Search()
        print(query, year, language)
        search_results = search.movie(query=query, year=year, language=language)
        print(search_results)
        self.__tmdb_info.clear()
        for result in search_results["results"]:
            tmdb_info = MovieTMDBInfo()
            tmdb_info.fill_with_search_result(result)
            self.__tmdb_info.append(tmdb_info)
        if len(self.__tmdb_info) == 0:
            self.__tmdb_info.append(MovieTMDBInfo())

    # TODO
    def get_info_(self):
        pass

    #     """
    #     search on imdb for a movie title, and store results as others information.
    #
    #     also, select best movie and set it as current information
    #     """
    #
    #     # web service url
    #     url = "http://www.imdbapi.com/"
    #     # create data
    #     values = {
    #         't' : self.guessed_info_['title']
    #     }
    #
    #     if self.YEAR in self.guessed_info_:
    #         values.update({
    #                        'y': self.guessed_info_[self.YEAR]
    #                        })
    #
    #     data = urllib.urlencode(values)
    #     # POST send data to web service
    #     f = urllib2.urlopen(url + "?" + data)
    #
    #     response = json.loads(f.read())
    #
    #     if 'imdbID' in response:
    #         # create imdb search engine
    #         imdb_archive = imdb.IMDb()
    #         # search for title into IMDB, and returns some candidate movies
    #         movie = imdb_archive.get_movie(response['imdbID'][2:])
    #     else:
    #         movie = None
    #
    #     self.others_info_ = []
    #     self.info_ = None
    #
    #     ## construct the others information list
    #     # save title and original title
    #     if movie != None:
    #         # take them from movie info
    #         title = movie['title']
    #         original_title = movie['title']
    #     else:
    #         # take them from guessed info
    #         title = self.guessed_info_[self.TITLE]
    #         original_title = self.guessed_info_[self.TITLE]
    #     # save the year
    #     year = ''
    #     if movie != None:
    #         movie_year = movie.get('year')
    #         if movie_year != None:
    #             year = unicode(movie_year)
    #     elif self.YEAR in self.guessed_info_:
    #         year = unicode(self.guessed_info_[self.YEAR])
    #     # save the director(s)
    #     director = ''
    #     if movie != None:
    #         movie_directors = movie.get('director')
    #         if movie_directors != None:
    #             directors = []
    #             for director in movie_directors:
    #                 directors.append(director['name'])
    #             directors = ', '.join(directors)
    #             director = directors
    #     # save the duration
    #     # minutes only representation
    #     duration1 = ''
    #     # hours-minutes representation
    #     duration2 = ''
    #     duration = None
    #     if movie != None:
    #         runtimes = movie.get('runtimes')
    #         if runtimes != None:
    #             #XXX by now, I only keep the first runtime,
    #             # but it would be interesting to consider also the associated
    #             # country (e.g.: [u'92', u'South Korea:97::(uncut version)', u'Japan:98'])
    #             runtime = runtimes[0]
    #             match = re.search('\d+', runtime)
    #             if match:
    #                 duration = int(match.group(0))
    #     elif self.video_duration_ != None:
    #         duration = self.video_duration_
    #     if duration != None:
    #         duration1 = str(duration) + 'm'
    #         hours = int(duration / 60)
    #         minutes = int(duration % 60)
    #         duration2 = str(hours) + 'h'
    #         if minutes != 0:
    #             duration2 = duration2 + str(minutes) + 'm'
    #     duration = [duration1, duration2]
    #     # save language
    #     language = ['', '']
    #     if movie != None:
    #         language = movie.guessLanguage()
    #         if language != None:
    #             language = utils.name_to_language(language)
    #     elif self.LANGUAGE in self.guessed_info_:
    #         language = self.guessed_info_[self.LANGUAGE]
    #
    #     score = 0
    #     if movie != None:
    #         # calculate string distance from current title and guessed title
    #         title1 = movie['title'].lower()
    #         title2 = self.guessed_info_[self.TITLE].lower()
    #         score = difflib.SequenceMatcher(None, title1, title2).ratio()
    #         # if title language is the same as the guessed language, add 1 to score
    #         if self.LANGUAGE in self.guessed_info_ \
    #         and self.guessed_info_[self.LANGUAGE] == language:
    #             score += 1
    #         best_score = score
    #     # creates the info dictionary, to store the movie information
    #     info = {
    #             self.TITLE: title,
    #             self.ORIGINAL_TITLE: original_title,
    #             self.YEAR: year,
    #             self.DIRECTOR: director,
    #             self.DURATION: duration,
    #             self.LANGUAGE: language,
    #             self.SCORE: score}
    #     # keep these info
    #     self.others_info_.append(info)
    #     # keep info as the current one
    #     self.info_ = info
    #
    #     if movie != None:
    #         # for each aka
    #         akas = movie.get('akas')
    #         if akas != None:
    #             for aka in akas:
    #                 # split aka (title::countries)
    #                 aka = aka.split('::')
    #                 language = None
    #                 # sometimes there is no countries indication, so skip it
    #                 if len(aka) == 2:
    #                     countries = aka[1]
    #                     # search for language indication
    #                     possible_language = re.search('(?:[(])([a-zA-Z]+?)(?: title[)])', countries)
    #                     if possible_language:
    #                         language = utils.name_to_language(possible_language.group(1))
    #                     # if not found
    #                     if language == None:
    #                         # search for countries (keep only the first one)
    #                         country = countries.split(',')[0]
    #                         country = re.sub('\(.*?\)', '', country).strip()
    #                         # get language corresponding to found country
    #                         language = utils.country_to_language(country)
    #                 if language == None:
    #                     language = ['', '']
    #                 # calculate string distance from current title and guessed title
    #                 title1 = aka[0].lower()
    #                 title2 = self.guessed_info_[self.TITLE].lower()
    #                 score = difflib.SequenceMatcher(None, title1, title2).ratio()
    #                 # if title language is the same as the guessed language, add 1 to score
    #                 if self.LANGUAGE in self.guessed_info_ \
    #                 and self.guessed_info_[self.LANGUAGE] == language:
    #                     score += 1
    #                 # creates the info dictionary, to store the movie information
    #                 info = {
    #                         self.TITLE: aka[0],
    #                         self.ORIGINAL_TITLE: movie['title'],
    #                         self.YEAR: year,
    #                         self.DIRECTOR: director,
    #                         self.DURATION: duration,
    #                         self.LANGUAGE: language,
    #                         self.SCORE: score}
    #                 # keep these info
    #                 self.others_info_.append(info)
    #                 # if this is the best movie
    #                 if score > best_score:
    #                     # keep info as the current one
    #                     self.info_ = info
    #                     best_score = score
    #
    #     # sort others information from best one to worst one, using calculated score
    #     self.others_info_ = sorted(self.others_info_, cmp = lambda x, y: cmp(x[self.SCORE], y[self.SCORE]), reverse = True)

    # TODO
    def search_new_title(self, title):
        pass
        """
        search for a new title, and replace current information
        """

        # guess info from given title
        guessed_info = guess_info(title)
        self.__guessed_info[self.TITLE] = guessed_info[self.TITLE]
        if self.YEAR in guessed_info:
            self.__guessed_info[self.YEAR] = guessed_info[self.YEAR]
        self.get_info_()

    def generate_new_name(self, renaming_rule):
        """
        generates new file name based on given renaming rule
        """

        pass

        # from preferences_dialog import PreferencesDialog as Preferences
        # from renaming_rule_dialog import RenamingRuleDialog as RenamingRule
        #
        # if len(renaming_rule) == 0:
        #     self._renamed_file_name = ''
        # else:
        #     duration_index = preferences.get_duration_representation()
        #     language_index = preferences.get_language_representation()
        #     words_separator_index = preferences.get_words_separator()
        #     separator = Preferences.WORDS_SEPARATORS[words_separator_index]
        #     opened_brackets = [
        #         RenamingRule.OPENED_ROUND_BRACKET,
        #         RenamingRule.OPENED_SQUARE_BRACKET,
        #         RenamingRule.OPENED_CURLY_BRACKET]
        #     closed_brackets = [
        #         RenamingRule.CLOSED_ROUND_BRACKET,
        #         RenamingRule.CLOSED_SQUARE_BRACKET,
        #         RenamingRule.CLOSED_CURLY_BRACKET]
        #     # split renaming rule
        #     rules = renaming_rule.split('.')
        #
        #     ## 1st round: replace attributes with corresponding values and remove empty ones
        #     new_name_items = []
        #     # loop on renaming rule
        #     for rule in rules:
        #         # title
        #         if rule == self.TITLE \
        #                 and self.get_title() != '':
        #             new_name_items.append(self.get_title())
        #         # original title
        #         elif rule == self.ORIGINAL_TITLE \
        #                 and self.get_original_title() != '':
        #             new_name_items.append(self.get_original_title())
        #         # year
        #         elif rule == self.YEAR \
        #                 and self.get_year() != '':
        #             new_name_items.append(self.get_year())
        #         # director
        #         elif rule == self.DIRECTOR \
        #                 and self.get_directors() != '':
        #             new_name_items.append(self.get_directors())
        #         # duration
        #         elif rule == self.DURATION \
        #                 and self.get_duration() != '':
        #             new_name_items.append(self.get_duration(duration_index))
        #         # language
        #         elif rule == self.LANGUAGE \
        #                 and self.get_language() != '':
        #             language = self.get_language(language_index)
        #             if self.get_subtitles() != '':
        #                 language += ' sub ' + self.get_subtitles(language_index)
        #             new_name_items.append(language)
        #         # opened and closed brackets
        #         elif rule in opened_brackets \
        #                 or rule in closed_brackets:
        #             new_name_items.append(rule)
        #
        #     ## 2nd round: remove empty brackets
        #     cleaned_new_name = []
        #     # loop on new name
        #     for i in range(len(new_name_items)):
        #         item = new_name_items[i]
        #         if (  # current item is an opened bracket and next one is a closed bracket
        #                             item in opened_brackets
        #                     and i + 1 < len(new_name_items)
        #                 and new_name_items[i + 1]
        #                 not in closed_brackets) \
        #                 or (  # current item is a closed bracket and previous one is not an opened bracket
        #                                     item in closed_brackets
        #                             and i - 1 > 0
        #                         and new_name_items[i - 1] not in opened_brackets) \
        #                 or (  # current item is neither an opened bracket nor a closed bracket
        #                                 item not in opened_brackets and item not in closed_brackets):
        #             # if previous clauses are true, keep the item
        #             cleaned_new_name.append(item)
        #
        #     ## 3rd round: generate new name, adding separators between items
        #     new_name = ""
        #     # loop on cleaned new name
        #     for i in range(len(cleaned_new_name)):
        #         item = cleaned_new_name[i]
        #         # append current item to new name
        #         new_name += item
        #         # if current item is not the last one
        #         if i + 1 < len(cleaned_new_name):
        #             # separate closed brackets and next items with a space
        #             if item in closed_brackets:
        #                 new_name += ' '
        #             elif item not in opened_brackets:  # is an attribute
        #                 # separate attributes and opened brackets with a space
        #                 if cleaned_new_name[i + 1] in opened_brackets:
        #                     new_name += ' '
        #                 elif cleaned_new_name[i + 1] not in closed_brackets:  # is an attribute
        #                     new_name += separator
        #
        #     # if current movie is divided into parts
        #     if self.get_part() != '':
        #         # last item is a closed bracket
        #         if cleaned_new_name[-1:] in closed_brackets:
        #             # append a space
        #             new_name += ' '
        #         # last item is an attribute
        #         else:
        #             new_name += separator
        #         # add part to new name
        #         new_name += "Part " + self.get_part()
        #     # set file new name
        #     self._renamed_file_name = new_name
        #
        # return self._renamed_file_name

    def check_and_clean_new_name(self):
        """
        check new file name for errors and prepares it for renaming

        Thanks to <a href="http://file-folder-ren.sourceforge.net/">Metamorphose</a>
        for this code.
        """

        # if new name is empty or equal to old one,
        # don't rename the file
        if self._renamed_file_name.strip() == '' \
                or self._original_file_name == self._renamed_file_name:
            return False
        # char used to replace bad characters in name
        replace_with = ''
        # get operative system
        sysname = platform.system()
        # copy new name to a temp variable
        name = self._renamed_file_name

        # If the filename starts with a . prepend it with an underscore, so it
        # doesn't become hidden.
        # This is done before calling splitext to handle filename of "."
        # splitext acts differently in python 2.5 and 2.6 - 2.5 returns ('', '.')
        # and 2.6 returns ('.', ''), so rather than special case '.', this
        # special-cases all files starting with "." equally (since dotfiles have)
        if name.startswith("."):
            name = "_" + name
        # Remove any null bytes
        name = name.replace("\0", "")
        # Blacklist of characters
        if sysname == 'Darwin':
            # : is technically allowed, but Finder will treat it as / and will
            # generally cause weird behaviour, so treat it as invalid.
            blacklist = r'/:'
        elif sysname == 'Linux':
            blacklist = r'/'
        else:
            # platform.system docs say it could also return "Windows" or "Java".
            # Failsafe and use Windows sanitisation for Java, as it could be any
            # operating system.
            blacklist = r'\/:*?"<>|'
        # Replace every blacklisted character with a underscore
        name = re.sub("[{0}]".format(re.escape(blacklist)), replace_with, name)
        # Remove any trailing whitespace
        name = name.strip()
        # There are a bunch of filenames that are not allowed on Windows.
        # As with character blacklist, treat non Darwin/Linux platforms as Windows
        if sysname not in ['Darwin', 'Linux']:
            invalid_filenames = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2",
                                 "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1",
                                 "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
            if name in invalid_filenames:
                name = "_" + name
                # Replace accented characters with ASCII equivalent
                #        name = unicode(name) # cast data to unicode
                #        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        # Treat extension seperatly
        extension = self._file_extension
        # Truncate filenames to valid/sane length.
        # NTFS is limited to 255 characters, HFS+ and EXT3 don't seem to have
        # limits, FAT32 is 254. I doubt anyone will take issue with losing that
        # one possible character, and files over 254 are pointlessly unweidly
        max_len = 254
        # check length
        if len(name + extension) > max_len:
            if len(extension) > len(name):
                # Truncate extension instead of filename, no extension should be
                # this long..
                new_length = max_len - len(name)
                extension = extension[:new_length]
            else:
                new_length = max_len - len(extension)
                name = name[:new_length]

        # if a file with current new name already exists
        if os.path.isfile(os.path.join(self._directory_path, name + extension)):
            # create a counter
            counter = 1
            # files with same name will have a counter appended at their name's end,
            # with pattern "file name (<counter>)
            # increase counter until it doesn't find highest counter 
            while os.path.isfile(os.path.join(self._directory_path, name + ' (' + str(counter) + ')' + extension)):
                counter += 1
            name = name + ' (' + str(counter) + ')'

        # set cleaned new name and extension
        self._renamed_file_name = str(name)
        self._file_extension = extension
        # ok, file can be renamed
        return True
