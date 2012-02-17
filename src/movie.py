# -*- coding: latin-1 -*-

import difflib
import enzyme
import imdb
import os
import platform
import re
import unicodedata
import datetime
import utils

__author__ = "Alberto Malagoli"

blackwords = [
              # video type
              'DVDRip', 'HD-DVD', 'HDDVD', 'HDDVDRip', 'BluRay', 'Blu-ray', 'BDRip', 'BRRip',
              'HDRip', 'DVD', 'DVDivX', 'HDTV', 'DVB', 'DVBRip', 'PDTV', 'WEBRip', 'DVDSCR',
              'Screener', 'VHS', 'VIDEO_TS',
              # screen
              '720p', '720',
              # video codec
              'XviD', 'DivX', 'x264', 'h264', 'Rv10',
              # audio codec
              'AC3', 'DTS', 'He-AAC', 'AAC-He', 'AAC', '5.1',
              # ripper teams
              'ESiR', 'WAF', 'SEPTiC', '[XCT]', 'iNT', 'PUKKA', 'CHD', 'ViTE', 'TLF',
              'DEiTY', 'FLAiTE', 'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS', ' FiNaLe',
              'UnSeeN', 'aXXo', 'KLAXXON', 'NoTV', 'ZeaL', 'LOL', 'iTALiAN'
              ]

def guess_info(title):
    """
    given a title, tries to guess as much information as possible.
    
    guessed information:
    title, year, language, country, part
    
    language and country are pycountry classes
    """

    # create info dictionary
    info = dict()
    # guess year
    title, year = guess_year_(title)
    if year != None:
        info.update({'year': year})
    # guess language
    title, language = guess_language_(title)
    if language != None:
        info.update({'language': language})
    # guess part
    title, part = guess_part_(title)
    if part != None:
        info.update({'part': part})
    # clean title
    title = clean_title_(title)
    info.update({'title': title})
    # return guessed information
    return info

def guess_year_(title):
    """
    looks for year patterns, and return found year
    
    note this only looks for valid production years, that is between 1920
    and now + 5 years, so for instance 2000 would be returned as a valid
    year but 1492 would not
    """

    year = None
    # search for year pattern (4 consequent digit)
    match = re.search(r'[0-9]{4}', title)
    # if found, check if year is between 1920 and now + 5 years
    if match \
    and 1920 < int(match.group(0)) < datetime.date.today().year + 5:
        year = match.group(0)
        # remove year from title
        title = title[:match.start()] + title[match.end():]
    return title, year

def guess_language_(title):
    """
    guess movie language, looking for ISO language representation in title
    """

    language = None
    match = re.search('(?:[^a-zA-Z])([a-zA-Z]{3})(?:[^a-zA-Z])', title)
    if match:
        try:
            language = utils.alpha3_to_language(match.group(1))
            # remove language from title
            title = title[:match.start() + 1] + title[match.end() - 1:]
        except KeyError:
            pass
    return title, language

def guess_part_(title):
    """
    guess movie part, i.e. CD1
    """

    part = None
    # search part, which can be like, for example, disk1 or disk 1
    match = re.search('(cd|disk|part)[ ]?[0-9]', title.lower(), re.IGNORECASE)
    if match:
        # get part number
        part = match.group(0)[-1:]
        # remove part from title
        title = title[:match.start()] + title[match.end():]
    return title, part

def clean_title_(title):
    # remove everything inside parenthesis
    title = re.sub('[([{].*?[)\]}]', '', title)
    # replace dots, underscores and dashes with spaces
    title = re.sub('[\._\-\'"]', ' ', title)
    stitle = title.split()
    title = []
    # loop on name
    for word in stitle:
        is_not_a_blackword = True
        for blackword in blackwords:
            if word.lower() == blackword.lower():
                is_not_a_blackword = False
                break
        if is_not_a_blackword:
            title.append(word)
        else:
            break
    title = ' '.join(title)
    return title

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
            # file path (only directory)
            self.path_ = 'C:\\'
            # original movie title, before renaming
            self.original_name_ = '[DivX ITA] A really cool movie (2012)'
            # file extension
            self.extension_ = '.avi'
            # movie new title (after renaming)
            self.new_name_ = ''
            # current state
            # states are used to show a proper panel in GUI
            self.state_ = self.STATE_BEFORE_RENAMING

            self.guessed_info_ = {'part': '1'}

            info = {
                    'title': 'Un film molto figo',
                    'original_title': 'A really cool movie',
                    'year': '2012',
                    'director': 'A. Director',
                    'duration': ['100m', '1h40m'],
                    'language': ['Italian', 'ITA'],
                    'score': 1}

            self.others_info_ = [info]
            self.info_ = info

        else:
            path, name = os.path.split(filepath)
            name, extension = os.path.splitext(name)
            # file path (only directory)
            self.path_ = os.path.normpath(unicode(path))
            # original movie title, before renaming
            self.original_name_ = unicode(name)
            # file extension
            self.extension_ = unicode(extension)
            # movie new title (after renaming)
            self.new_name_ = ''
            # current state
            # states are used to show a proper panel in GUI
            self.state_ = self.STATE_BEFORE_RENAMING
            # error occurred during renaming operation
            self.renaming_error_ = ''

            print('*' * 30)
            print(name)
            print('*' * 30)
            # get video duration
            self.video_duration_ = None
            try:
                video_info = enzyme.parse(self.abs_original_file_name())
            except ValueError:
                pass
            else:
                if video_info.length != None:
                    self.video_duration_ = int(video_info.length / 60)
                elif video_info.video[0].length != None:
                    self.video_duration_ = int(video_info.video[0].length / 60)
            self.guessed_info_ = guess_info(name)
            self.get_info_()

    def original_file_name(self):
        return self.original_name_

    def new_file_name(self):
        return self.new_name_

    def abs_original_file_name(self):
        """
        return the complete original file name, from the root
        """

        return os.path.join(self.path_, self.original_name_ + self.extension_)

    def abs_new_file_name(self):
        """
        return the complete new file name, from the root
        """

        return os.path.join(self.path_, self.new_name_ + self.extension_)

    def title(self):
        if self.info_ != None:
            return self.info_['title']
        return self.guessed_info_['title']

    def original_title(self):
        if self.info_ != None:
            return self.info_['original_title']
        return ''

    def year(self):
        if self.info_ != None:
            return self.info_['year']
        if self.guessed_info_ != None \
        and 'year' in self.guessed_info_:
            return self.guessed_info_['year']
        return ''

    def director(self):
        if self.info_ != None:
            return self.info_['director']
        return ''

    def duration(self, index = 0):
        if self.info_ != None:
            return self.info_['duration'][index]
        return ''

    def language(self, index = 0):
        if self.info_ != None:
            return self.info_['language'][index]
        if self.guessed_info_ != None \
        and 'language' in self.guessed_info_:
            return self.guessed_info_['language'][index]
        return ''

    def part(self):
        if self.guessed_info_ != None \
        and 'part' in self.guessed_info_:
            return self.guessed_info_['part']
        return ''

    def others_info(self):
        others_info = []
        for other_info in self.others_info_:
            info = [other_info['title'], other_info['year'], other_info['language'][0]]
            others_info.append(info)
        return others_info

    def state(self):
        return self.state_

    def set_state(self, state, error = ""):
        """
        set state
        
        state must be one of STATE_BEFORE_RENAMING, STATE_RENAMED, STATE_RENAMING_ERROR
        
        error could be an error message, used with STATE_RENAMING_ERROR
        """

        self.state_ = state
        self.renaming_error_ = error

        if state == Movie.STATE_RENAMED:
            self.original_name_ = self.new_name_

    def set_movie(self, index):
        self.info_ = self.others_info_[index]

    def get_info_(self):

        # create imdb search engine
        imdb_archive = imdb.IMDb()
        # search for title into IMDB, and returns some candidate movies
        movies = imdb_archive.search_movie(self.guessed_info_['title'])

        keep_index = 0
        if len(movies) > 0:
            # sometimes, with movies with an old version and a new version
            # (e.g. Godzilla: a 1954 version and a 1998 version)
            # imdb search returns the oldest one as the second result.
            # so, keep movie year found on title into consideration as
            # discrimination for the right movie
            if 'year' in self.guessed_info_ \
            and len(movies) > 1:
                movie_year = movies[1].get('year')
                if movie_year != None \
                and self.guessed_info_['year'] == str(movie_year):
                    keep_index = 1

        self.others_info_ = []
        self.info_ = None
        for index in range(len(movies)):
            movie = movies[index]

            # get more info on this movie
            imdb_archive.update(movie)

            year = ''
            movie_year = movie.get('year')
            if movie_year != None:
                year = unicode(movie_year)
            elif self.guessed_info_ != None \
            and 'year' in self.guessed_info_:
                year = unicode(self.guessed_info_['year'])

            director = ''
            movie_directors = movie.get('director')
            if movie_directors != None:
                directors = []
                for director in movie_directors:
                    directors.append(director['name'])
                directors = ', '.join(directors)
                director = directors

            duration1 = ''
            duration2 = ''
            duration = None
            runtimes = movie.get('runtimes')
            if runtimes != None:
                #XXX by now, I only keep the first runtime,
                # but it would be interesting to consider also the associated
                # country (e.g.: [u'92', u'South Korea:97::(uncut version)', u'Japan:98'])
                runtime = runtimes[0]
                match = re.search('\d+', runtime)
                if match:
                    duration = int(match.group(0))
            elif self.video_duration_ != None:
                duration = self.video_duration_
            if duration != None:
                duration1 = str(duration) + 'm'
                hours = int(duration / 60)
                minutes = int(duration % 60)
                duration2 = str(hours) + 'h'
                if minutes != 0:
                    duration2 = duration2 + str(minutes) + 'm'
            duration = [duration1, duration2]

            language = None
            if self.guessed_info_ != None \
            and 'language' in self.guessed_info_:
                language = self.guessed_info_['language']
            else:
                language = movie.guessLanguage()
                if language != None:
                    language = utils.name_to_language(language)
            if language == None:
                language = ['', '']

            title1 = movie['title'].lower()
            title2 = self.guessed_info_['title'].lower()
            score = difflib.SequenceMatcher(None, title1, title2).ratio()
            if movie_year != None \
            and self.guessed_info_ != None \
            and 'year' in self.guessed_info_ \
            and self.guessed_info_['year'] == movie_year:
                score += 1
#            if self.guessed_info_ != None \
#            and 'language' in self.guessed_info_ \
#            and self.guessed_info_['language'] == language:
#                score += 1

            info = {
                    'title': movie['title'],
                    'original_title': movie['title'],
                    'year': year,
                    'director': director,
                    'duration': duration,
                    'language': language,
                    'score': score}
            if score > 0.3:
                self.others_info_.append(info)

            if index == keep_index:
                self.info_ = info
                best_score = score

            akas = movie.get('akas')
            if akas != None:
                for aka in akas:

                    aka = aka.split('::')
                    language = None
                    if len(aka) == 2:
                        countries = aka[1]
                        possible_language = re.search('(?:[(])([a-zA-Z]+?)(?: title[)])', countries)
                        if possible_language:
                            language = utils.name_to_language(possible_language.group(1))
                        if language == None:
                            country = countries.split(',')[0]
                            country = re.sub('\(.*?\)', '', country).strip()
                            language = utils.country_to_language(country)
                        print(countries + ' --> ' + str(language))
                    if language == None:
                        language = ['', '']

                    title1 = aka[0].lower()
                    title2 = self.guessed_info_['title'].lower()
                    score = difflib.SequenceMatcher(None, title1, title2).ratio()
                    if movie_year != None \
                    and self.guessed_info_ != None \
                    and 'year' in self.guessed_info_ \
                    and self.guessed_info_['year'] == movie_year:
                        score += 1
                    if self.guessed_info_ != None \
                    and 'language' in self.guessed_info_ \
                    and self.guessed_info_['language'] == language:
                        score += 1

                    info = {
                            'title': aka[0],
                            'original_title': movie['title'],
                            'year': year,
                            'director': director,
                            'duration': duration,
                            'language': language,
                            'score': score}
                    if score > 0.3:
                        self.others_info_.append(info)

                    if index == keep_index \
                    and score > best_score:
                        self.info_ = info
                        best_score = score

        self.others_info_ = sorted(self.others_info_, cmp = lambda x, y: cmp(x['score'], y['score']), reverse = True)

    def search_new_title(self, title):
        guessed_info = guess_info(title)
        self.guessed_info_['title'] = guessed_info['title']
        if 'year' in guessed_info:
            self.guessed_info_['year'] = guessed_info['year']
        self.get_info_()

    def generate_new_name(self, renaming_rule):
        """
        generates new file name based on given renaming rule
        """

        if len(renaming_rule) == 0:
            self.new_name_ = ''
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
                try:
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
                except KeyError:
                    pass
                except IndexError:
                    pass
            # if current movie is divided into parts 
            if self.part != '0':
                # if next rule is not an opened or closed bracket 
                if rules[-1] not in opened_brackets and \
                rules[-1] not in closed_brackets:
                     # separate info with a comma
                    new_name.append(', ')
                # add part to new name
                new_name.append(self.tr("Part ") + self.part)
            # join new name (was a list) and set it as the new name for that movie
            self.new_name_ = unicode(''.join(new_file_name).strip())

        return self.new_name_

    def generate_new_name_old(self, renaming_rule):
        """
        generates new file name based on given renaming rule
        """

        if len(self.info) == 0 or len(renaming_rule) == 0:
            self.new_name_ = ''
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
                try:
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
                except KeyError:
                    pass
                except IndexError:
                    pass
            # if current movie is divided into parts 
            if self.part != '0':
                # if next rule is not an opened or closed bracket 
                if rules[-1] not in opened_brackets and \
                rules[-1] not in closed_brackets:
                     # separate info with a comma
                    new_name.append(', ')
                # add part to new name
                new_name.append(self.tr("Part ") + self.part)
            # join new name (was a list) and set it as the new name for that movie
            self.new_name_ = unicode(''.join(new_file_name).strip())

        return self.new_name_

    def check_and_clean_new_name(self):
        """
        check new file name for errors and prepares it for renaming

        Thanks to <a href="http://file-folder-ren.sourceforge.net/">Métamorphose</a>
        for this code.
        """

        # if new name is empty or equal to old one,
        # don't rename the file
        if self.new_name_.strip() == '' \
        or self.original_name_ == self.new_name_:
            return False
        # char used to replace bad characters in name
        replace_with = ""
        # get operative system
        sysname = platform.system()
        # copy new name to a temp variable
        name = self.new_name_

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
        name = unicode(name) # cast data to unicode
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        # Treat extension seperatly
        extension = self.extension_
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
        self.new_name_ = unicode(name)
        self.extension_ = extension
        # ok, file can be renamed
        return True



