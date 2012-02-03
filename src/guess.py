# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

#from PyQt4.QtCore import QLocale
#import guess_language as gl
import re
import datetime
import pycountry

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

def info(title):
    """
    given a title, tries to guess as much information as possible.
    
    guessed information:
    title, year, language, country, part
    
    language and country are pycountry classes
    """

    # create info dictionary
    info = dict()
    # guess year
    title, year = guess_year(title)
    if year != None:
        info.update({'year': year})
    # guess language
    title, language = guess_language(title)
    if language != None:
        info.update({'language': language})
    # guess part
    title, part = guess_part(title)
    if part != None:
        info.update({'part': part})
    # clean title
    title = clean_title(title)
    info.update({'title': title})
    # return guessed information
    return info

def guess_year(title):
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

def guess_language(title):
    """
    guess movie language, looking for ISO language representation in title
    """

    language = None
    match = re.search('(?:[^A-Z])([A-Z]{3})(?:[^A-Z])', title)
    if match:
        try:
            print(match.group(1))
            language = pycountry.languages.get(terminology = match.group(1).lower())
            print(language.name)
            # remove language from title
            title = title[:match.start() + 1] + title[match.end() - 1:]
        except KeyError:
            pass
    return title, language

#def guess_language_old(title):
#    """
#    guess movie language, looking for ISO language representation in title
#    """
#
#    found_language = None
#    # loop on supported languages
#    for language in pycountry.languages:
#        # search for language terminology (which is the 3-letters language 
#        # representation in ISO 639 form) in title.
#        # match only if is preceded or followed by a symbol, not letters
#        # (that means these three letters are not part of a word)
#        match = re.search('[^a-z0-9]' + language.terminology + '[^a-z0-9]', title.lower())
#        if match:
#            found_language = language
#            # remove language from title
#            title = title[:match.start() + 1] + title[match.end() - 1:]
#            # break loop, so don't look for other languages
#            break
#    return title, found_language

#def guess_language_old_old(title):
#    """
#    guess movie language, looking for ISO language representation in title
#    """
#    #XXX cercare anche usando il nome della lingua in inglese
#    found_language = None
#    country = None
#    # loop on supported languages
#    for language in pycountry.languages:
#        # search for language terminology (which is the 3-letters language 
#        # representation in ISO 639 form) in title.
#        # match only if is preceded or followed by a symbol, not letters
#        # (that means these three letters are not part of a word)
#        match = re.search('[^a-z0-9]' + language.terminology + '[^a-z0-9]', title.lower())
#        if match:
#            found_language = language
#            # retrieve country for that language
#            #XXX ma non ritorna una lista??
##            country = pycountry.countries.get(alpha3 = language.terminology.upper())
#            # remove language from title
#            title = title[:match.start() + 1] + title[match.end() - 1:]
#            # break loop, so don't look for other languages
#            break
#    if not found_language:
#        language_code = gl.guessLanguage(title)
#        if language_code != 'UNKNOWN':
#            found_language = pycountry.languages.get(alpha2 = language_code)
#    return title, found_language, country

def guess_part(title):
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

def clean_title(title):
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

#def guess_language(self):
#    # guessing needs complete name
#    name = self.original_name + self.extension
#    # guess movie info, using guessit module
#    info = guessit.guess_movie_info(name)
#    print(name)
#    print(info.nice_string())
#    print(guess_language.guessLanguageInfo(name))
#    print(guess_language.guessLanguageInfo(info['title']))
#    print('-' * 50)

#def guess_info(self):
#    # guessing needs complete name
#    name = self.original_name + self.extension
#    # guess movie info, using guessit module
#    info = guessit.guess_movie_info(name)
#    # remove everything inside parenthesis
#    # need this because of a problem with guessit module,
#    # which has some problem with parenthesis
#    name = re.sub('[([{].*?[)\]}]', ' ', name)
#    # some titles ends with 1 (example: Alien 1), 
#    # which causes wrong guessing, so remove it
#    if name.endswith(' 1'):
#        print('endswith1')
#        name = name[:-2]
#    # guess name again, this time without parenthesis
#    info2 = guessit.guess_movie_info(name)
#    # get only guessed title from new guess
#    info['title'] = info2['title']
#    # save guessed info in movie attributes
#    if 'title' in info:
#        self.title = info['title']
#    if 'year' in info:
#        self.year = info['year']
#    if 'cdNumber' in info:
#        self.part = info['cdNumber']
#    if 'language' in info:
#        languages = info['language']
#        for language in languages:
#            print(language.lng3())
#    # XXX ci manca da salvare la lingua



#    def get_info(self):
#        """
#        get info from original name
#        """
#
#        ## split name        
#        # lower the name string
#        name = self.original_name.lower()
#        # and split it into words using separators: " ._-()[]{}"
#        name = re.split(r'[ ._\-(){}\[\]]', name)
#        ## guess language
#        self.guess_language(name)
#        ## guess part
#        self.guess_part(name)
#        ## clean name
#        searching_title = self.clean_name()
#        ## search movie name
#        self.search_title(searching_title)

#    def guess_language(self, name):
#        """
#        tries to guess the movie spoken language from movie title
#        """
#
#        # scores used to determine most probable language
#        # order: EN, ES, DE, FR, IT
#        language_scores = [0, 0, 0, 0, 0]
#        # name contains splitted original name
#        # loop on it
#        # when find a word corresponding to a language string,
#        # increase score
#        for word in name:
#            if word in ['en', 'eng']:
#                language_scores[0] += 1
#            elif word in ['es', 'spa']:
#                language_scores[1] += 1
#            elif word in ['de', 'ger', 'german']:
#                language_scores[2] += 1
#            elif word in ['fr', 'fra', 'french']:
#                language_scores[3] += 1
#            elif word in ['it', 'ita', 'italian']:
#                language_scores[4] += 1
#        # get maximum score
#        max_score = max(language_scores)
#        if max_score == 0:
#            # if cannot find language in name, use system language
#            system_language = locale.getdefaultlocale()[0][:2]
#            if system_language in self.LANGUAGES_CODES_INDEXES.keys():
#                self.language_index = self.LANGUAGES_CODES_INDEXES[system_language]
#        else:
#            # return language code matching max score index
#            return language_scores.index(max_score)

#    def guess_part(self, name):
#        """
#        tries to guess movie part from movie title
#        """
#
#        # name contains splitted original name
#        # loop on it
#        for word in name:
#            # if word contains movie part
#            if re.match(r'disk[0-9]|cd[0-9]|part[0-9]', word):
#                # get part number
#                self.part = word[-1:]

#def clean_name_2(self):
#    """
#    prepare the original name for a following use in IMDB search
#    """
#
#    # lower the original name
##        print(self.original_name)
#    name = self.original_name.lower()
##        print(name)
#    # replace dots, underscores and dashes with spaces
#    name = re.sub('[\._\'"]|( - )', ' ', name)
##        print(name)
#    # remove everything inside (), [], {}
#    name = re.sub('[([{].*?[)\]}]', ' ', name)
##        # remove everything inside ( )
##        name = re.sub(r'\((.+)\)', '', name)
##        print(name)
##        # remove everything inside [ ]
##        name = re.sub(r'\[(.+)\]', '', name)
##        print(name)
##        # remove everything inside { }
##        name = re.sub(r'{(.+)}', '', name)
##        print(name)
##        # remove brackets
##        name = re.sub('\(\)|{}|\[\]', '', name)
##        print(name)
#    # remove year
#    name = re.sub(r'\d\d\d\d', '', name)
##        print(name)
#    # remove disk information
#    name = re.sub(r'disk[0-9]|cd[0-9]|part[0-9]', '', name)
##        print(name)
#    # split it using spaces
#    name = name.split()
##        print(name)
#
#    # creates a blacklist of unwanted words 
#    blacklist = ['dvdrip', 'divx', 'xvid', 'brrip']
#    # that index represents first occurrence of a 
#    # black word (word in blacklist)
##        first_blackword_index = -1
#    title = []
#    # loop on name
#    for word in name:
##            word = name[i]
#        if word not in blacklist:
#            title.append(word)
#        else:
#            # found a blackword, memorize index and break loop
##                first_blackword_index = i
#            break
#        # remove black words
##        if first_blackword_index != -1:
#        # remove all words from name after first blackword occurrence
#        # does that because successives words are probably other unwanted words
##            name = name[:first_blackword_index]
##        print(title)
#    # return new cleaned name
#    return ' '.join(title)

#def clean_name(self):
#    """
#    prepare the original name for a following use in IMDB search
#    """
#
#    # lower the name string
#    name = self.original_name
#    # replace dots, underscores and dashes with spaces
#    name = re.sub(r'[._-]', ' ', name)
#    # remove everything inside ( )
#    name = re.sub(r'\((.+)\)', '', name)
#    # remove everything inside [ ]
#    name = re.sub(r'\[(.+)\]', '', name)
#    # remove everything inside { }
#    name = re.sub(r'{(.+)}', '', name)
#    # remove brackets
#    name = re.sub(r'[(){}\[\]]', '', name)
#    # remove disk information
#    name = re.sub(r'disk[0-9]|cd[0-9]|part[0-9]', '', name)
#    # convert name to lower case so I have no problem with blackwords matching
#    name = name.lower()
#    # split it using spaces
#    name = name.split(' ')
#
##        title = []
#    # creates a blacklist of unwanted words 
#    blacklist = ['dvdrip', 'dvix', 'xvid', 'brrip']
#    # that index represents first occurrence of a 
#    # black word (word in blacklist)
#    first_blackword_index = -1
#    # loop on name
#    for i in range(len(name)):
#        word = name[i]
#        if word in blacklist:
#            # found a blackword, memorize index and break loop
#            first_blackword_index = i
#            break
#        # remove black words
##            if word not in blacklist:
##                title.append(word)
#    if first_blackword_index != -1:
#        # remove all words from name after first blackword occurrence
#        # does that because successives words are probably other unwanted words
#        name = name[:first_blackword_index]
#    # return new cleaned name
#    return ' '.join(name)
