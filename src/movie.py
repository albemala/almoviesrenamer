# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

import imdb
import locale
import os
import platform
import re
import unicodedata

class Movie:
    """
    class representing a movie

    movies are shown in movies table
    """

    STATE_BEFORE_RENAMING = 0
    STATE_RENAMED = 1
    STATE_RENAMING_ERROR = 2

    LANGUAGES_CODES_INDEXES = {'en':0, 'es':1, 'de':2, 'fr':3, 'it':4}
    LANGUAGES_INDEXES_CODES = {0:'EN', 1:'ES', 2:'DE', 3:'FR', 4:'IT'}

    TITLE = 'title'
    CANONICAL_TITLE = 'canonical_title'
    AKAS = 'akas'
    AKAS_INDEX = 'akas_index'
    YEAR = 'year'
    DIRECTOR = 'directors'
    RUNTIMES = 'runtimes'
    RUNTIMES_INDEX = 'runtimes_index'
    LANGUAGE = 'language'

    def __init__(self, filepath = None):
        """
        constructor.

        takes the complete movie file path, or nothing if you want to create 
        a movie example
        """

        if filepath == None:
            self.create_movie_example()
            
        else:
            path, name = os.path.split(filepath)
            name, extension = os.path.splitext(name)
            # file path (only directory)
            self.path = os.path.normpath(unicode(path))
            # original movie title, before renaming
            self.original_name = unicode(name)
            # file extension
            self.extension = unicode(extension)
            # index used in GUI, representing movie spoken language 
            self.language_index = 0
            # some movies are divided into more parts, represented in 
            # title with words like "disk1" or "cd2".
            # that information is guessed from title
            self.part = '0'
            # movie new title (after renaming)
            self.new_name = ""
            # current state
            # states are used to show a proper panel in GUI
            self.state = self.STATE_BEFORE_RENAMING
            # possible movies corresponding to this one, with information about them
            # (title, director, year, ...)
            self.info = []
            # info index, used to memorize which info is associated with that movie
            self.info_index = 0
            # error occurred during renaming operation
            self.renaming_error = ""

            # try to guess new movie name from current name
            self.get_info()

    def create_movie_example(self):
        """
        creates a movie example by filling info from a fake movie
        """
        
        self.language_index = 0
        self.part = '1'
        self.new_name = ""
        self.info_index = 0
        self.info = []

        keys = []
        values = []

        keys.append(self.TITLE)
        values.append("A really cool movie")

        # not every movie returns a canonical title...
        keys.append(self.CANONICAL_TITLE)
        values.append("Really cool movie, A")

        keys.append(self.AKAS)
        keys.append(self.AKAS_INDEX)
        akas = ['Un film molto figo']
        akas_index = 0
        values.append(akas)
        values.append(akas_index)

        keys.append(self.YEAR)
        values.append("2008")

        keys.append(self.DIRECTOR)
        values.append("A. Director")

        keys.append(self.RUNTIMES)
        keys.append(self.RUNTIMES_INDEX)
        runtimes = ['100']
        runtimes_index = 0
        values.append(runtimes)
        values.append(runtimes_index)

        # populate info with keys and values extracted from candidateMovie
        self.info.append(dict(zip(keys, values)))

    def get_abs_original_name(self):
        """
        return the complete original file name, from the root
        """

        return os.path.join(self.path, self.original_name + self.extension)

    def get_abs_new_name(self):
        """
        return the complete new file name, from the root
        """

        return os.path.join(self.path, self.new_name + self.extension)

    def get_info(self):
        """
        get info from original name
        """
        
        ## split name        
        # lower the name string
        name = self.original_name.lower()
        # and split it into words using separators: " ._-()[]{}"
        name = re.split(r'[ ._\-(){}\[\]]', name)
        ## guess language
        self.guess_language(name)
        ## guess part
        self.guess_part(name)
        ## clean name
        searching_title = self.clean_name()
        ## search movie name
        self.search_title(searching_title)

    def guess_language(self, name):
        """
        tries to guess the movie spoken language from movie title
        """
        
        # scores used to determine most probable language
        # order: EN, ES, DE, FR, IT
        language_scores = [0, 0, 0, 0, 0]
        # name contains splitted original name
        # loop on it
        # when find a word corresponding to a language string,
        # increase score
        for word in name:
            if word in ['en', 'eng']:
                language_scores[0] += 1
            elif word in ['es', 'spa']:
                language_scores[1] += 1
            elif word in ['de', 'ger', 'german']:
                language_scores[2] += 1
            elif word in ['fr', 'fra', 'french']:
                language_scores[3] += 1
            elif word in ['it', 'ita', 'italian']:
                language_scores[4] += 1
        # get maximum score
        max_score = max(language_scores)
        if max_score == 0:
            # if cannot find language in name, use system language
            system_language = locale.getdefaultlocale()[0][:2]
            if system_language in self.LANGUAGES_CODES_INDEXES.keys():
                self.language_index = self.LANGUAGES_CODES_INDEXES[system_language]
        else:
            # return language code matching max score index
            return language_scores.index(max_score)

    def guess_part(self, name):
        """
        tries to guess movie part from movie title
        """
        
        # name contains splitted original name
        # loop on it
        for word in name:
            # if word contains movie part
            if re.match(r'disk[0-9]|cd[0-9]|part[0-9]', word):
                # get part number
                self.part = word[-1:]

    def clean_name(self):
        """
        prepare the original name for a following use in IMDB search
        """

        # lower the name string
        name = self.original_name
        # replace dots, underscores and dashes with spaces
        name = re.sub(r'[._-]', ' ', name)
        # remove everything inside ( )
        name = re.sub(r'\((.+)\)', '', name)
        # remove everything inside [ ]
        name = re.sub(r'\[(.+)\]', '', name)
        # remove everything inside { }
        name = re.sub(r'{(.+)}', '', name)
        # remove brackets
        name = re.sub(r'[(){}\[\]]', '', name)
        # remove disk information
        name = re.sub(r'disk[0-9]|cd[0-9]|part[0-9]', '', name)
        # convert name to lower case so I have no problem with blackwords matching
        name = name.lower()
        # split it using spaces
        name = name.split(' ')

#        title = []
        # creates a blacklist of unwanted words 
        blacklist = ['dvdrip', 'dvix', 'xvid', 'brrip']
        # that index represents first occurrence of a 
        # black word (word in blacklist)
        first_blackword_index = -1
        # loop on name
        for i in range(len(name)):
            word = name[i]
            if word in blacklist:
                # found a blackword, memorize index and break loop
                first_blackword_index = i
                break
            # remove black words
#            if word not in blacklist:
#                title.append(word)
        if first_blackword_index != -1:
            # remove all words from name after first blackword occurrence
            # does that because successives words are probably other unwanted words
            name = name[:first_blackword_index]
        # return new cleaned name
        return ' '.join(name)

    def search_title(self, title):
        """
        search given title on IMDB, and get corresponding movies info
        """

        # reset current movies and indexes
        self.info_index = 0
        self.info = []
        # create imdb search engine
        imdb_archive = imdb.IMDb()
        # search for title into IMDB, and returns some candidate movies
        candidate_movies = imdb_archive.search_movie(title)
        # if no movies corresponding to that title are found
        if len(candidate_movies) == 0:
            return
        # keep only the first three returned results
        movies = candidate_movies[:3]
        # for each found movie..
        for movie in movies:
            # get other information from IMDB
            imdb_archive.update(movie)
            # creates new pairs of keys and values because I don't want to store all
            # the information returned by IMDB, but only the most useful ones.
            # I also clean these information and stores them in a useful format.
            keys = []
            values = []
            # get title
            keys.append(self.TITLE)
            values.append(movie[self.TITLE])
            # get canonical title
            keys.append(self.CANONICAL_TITLE)
            canonical_title = ""
            # not every movie returns a canonical title...
            try:
                canonical_title = movie['canonical title']
            except KeyError:
                pass
            values.append(canonical_title)
            # get akas
            keys.append(self.AKAS)
            keys.append(self.AKAS_INDEX)
            akas = []
            akas_index = 0
            try:
                # example of AKAs for "Near Dark" movie:
                # u'"Cuando cae la oscuridad" - Argentina, Mexico',
                # u'"Agria nyhta" - Greece',
                # u'"Aux fronti\xe8res de l\'aube" - France'
                # u'"Blisko ciemnosci" - Poland'
                # u'"Depois do Anoitecer" - Portugal'
                # u'"Il buio si avvicina" - Italy'
                # u'"Los viajeros de la noche" - Spain'
                # u'"Natten har sitt pris" - Sweden'
                # u'"Near Dark - Die Nacht hat ihren Preis" - West Germany'
                # u'"Pimeyden l\xe4heisyys" - Finland'
                # u'"Quando Chega a Escurid\xe3o" - Brazil'

                # select AKAS index based on most probable language.
                # for each AKAS in candidateMovie
                for i in range(len(movie[self.AKAS])):
                    # get AKAS
                    aka = movie[self.AKAS][i]
                    # if spanish language is the most probable one and if current AKAS
                    # is the spanish one...
                    if self.language_index == 1 and re.search(r'Spain', aka):
                        # ... select it.
                        akas_index = i
                    # the same for other languages
                    elif self.language_index == 2 and re.search(r'Germany', aka):
                        akas_index = i
                    elif self.language_index == 3 and re.search(r'France', aka):
                        akas_index = i
                    elif self.language_index == 4 and re.search(r'Italy', aka):
                        akas_index = i

                for aka in movie[self.AKAS]:
                    # sometimes the AKAs list ends with a u'\xbb', so I remove it
                    if unicode(aka) != u'\xbb':
                        # takes only the AKAS title
                        # under Linux
                        if aka.startswith('"'):
                            splitted_aka = aka.split('"')
                            if len(splitted_aka) > 1:
                                akas.append(splitted_aka[1])
                        # or under Windows
                        else:
                            splitted_aka = aka.split('::')
                            if len(splitted_aka) > 1:
                                akas.append(splitted_aka[0])
            except KeyError:
                pass
            values.append(akas)
            values.append(akas_index)

            keys.append(self.YEAR)
            year = ""
            try:
                year = unicode(movie[self.YEAR])
            except KeyError:
                pass
            values.append(year)

            keys.append(self.DIRECTOR)
            directors = []
            try:
                for director in movie['director']:
                    directors.append(director['name'])
            except KeyError:
                pass
            values.append(', '.join(directors))

            keys.append(self.RUNTIMES)
            keys.append(self.RUNTIMES_INDEX)
            runtimes = []
            runtimes_index = 0
            try:
                for runtime in movie[self.RUNTIMES]:
                    # from runtimes, get only numbers representing time
                    match = re.search(r"(\d+)", runtime)
                    if match:
                        runtimes.append("{0}".format(runtime[match.start():match.end()]))
            except KeyError:
                pass
            values.append(runtimes)
            values.append(runtimes_index)
            # populate info with keys and values extracted from candidateMovie
            self.info.append(dict(zip(keys, values)))

    def generate_new_name(self, renaming_rule):
        """
        generates new file name based on given renaming rule
        """

        if len(self.info) == 0 or len(renaming_rule) == 0:
            self.new_name = ''
        else:
            new_name = []
            # split renaming rule
            rules = renaming_rule.split('.')
            # creates a list of rules, so it's easier to look for them
            info_keys = [self.TITLE, self.CANONICAL_TITLE, self.AKAS, self.YEAR, self.DIRECTOR, self.RUNTIMES]
            opened_brackets = ['(', '[', '{']
            closed_brackets = [')', ']', '}']
            # loop on rules
            for i in range(len(rules)):
                rule = rules[i]
#                try:
                if rule in info_keys:
                    # get corresponding info, based on info index also
                    info = self.info[self.info_index][rule]
                    # if rule is AKAS or RUNTIMES, get corresponding rule based 
                    # on selected index
                    if rule == self.AKAS:
                        index = self.info[self.info_index][self.AKAS_INDEX]
                        info = info[index]
                    elif rule == self.RUNTIMES:
                        index = self.info[self.info_index][self.RUNTIMES_INDEX]
                        info = info[index]
                    # append info to new name
                    new_name.append(info)
                    if i + 1 < len(rules):
                        # if next rule is not an opened or closed bracket 
                        if rules[i + 1] not in opened_brackets and \
                        rules[i + 1] not in closed_brackets:
                            # separate info with a comma
                            new_name.append(', ')
                elif rule in opened_brackets:
                    new_name.append(' ' + rule)
                elif rule in closed_brackets:
                    new_name.append(rule + ' ')
                elif rule == self.LANGUAGE:
                    # append selected language to new name
                    new_name.append(self.LANGUAGES_INDEXES_CODES[self.language_index])
                    if i + 1 < len(rules):
                        # if next rule is not an opened or closed bracket 
                        if rules[i + 1] not in opened_brackets and \
                        rules[i + 1] not in closed_brackets:
                            # separate info with a comma
                            new_name.append(', ')
#                except KeyError:
#                    pass
#                except IndexError:
#                    pass
            # if current movie is divided into parts 
            if self.part != '0':
                # if next rule is not an opened or closed bracket 
                if rules[-1] not in opened_brackets and \
                rules[-1] not in closed_brackets:
                     # separate info with a comma
                    new_name.append(', ')
                # add part to new name
                new_name.append("Part " + self.part)
            # join new name (was a list) and set it as the new name for that movie
            self.new_name = unicode(''.join(new_name).strip())

        return self.new_name

    def check_and_clean_new_name(self):
        """
        check new file name for errors and prepares it for renaming

        Thanks to <a href="http://file-folder-ren.sourceforge.net/">Métamorphose</a>
        for this code.
        """

        # if new name is empty or equal to old one,
        # don't rename the file
        if self.new_name.strip() == '' \
        or self.original_name == self.new_name:
            return False
        # char used to replace bad characters in name
        replace_with = "_"
        # get operative system
        sysname = platform.system()
        # copy new name to a temp variable
        name = self.new_name

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
            blacklist = r'\/:*?\"<>|'
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
        name = unicode(name) # cast data to unicode
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        # Treat extension seperatly
        extension = self.extension
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

        # if a file with current new name already exists, don't rename it
#        if os.path.isfile(os.path.join(self.path, name + extension)):
#            return False
        
        # set cleaned new name and extension
        self.new_name = unicode(name)
        self.extension = extension
        # ok, file can be renamed
        return True

    def set_state(self, state, error = ""):
        """
        set state
        
        state must be one of STATE_BEFORE_RENAMING, STATE_RENAMED, STATE_RENAMING_ERROR
        
        error could be an error message, used with STATE_RENAMING_ERROR
        """

        self.state = state
        self.renaming_error = error

        if state == Movie.STATE_RENAMED:
            self.original_name = self.new_name



