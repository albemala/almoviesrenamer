# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QLocale
import difflib
import guess_language as gl
import guessit
import imdb
import locale
import os
import platform
import re
import unicodedata
import enzyme
from fuzzywuzzy import fuzz
import pycountry
import guess

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
            self.path = 'C:\\'
            # original movie title, before renaming
            self.original_name = '[DivX ITA] A really cool movie (2012)'
            # file extension
            self.extension = '.avi'
            # movie new title (after renaming)
            self.new_name = ''
            # current state
            # states are used to show a proper panel in GUI
            self.state = self.STATE_BEFORE_RENAMING

            title = ['A really cool movie', 'Really cool movie, A']
            aka = 'Un film molto figo'
            year = '2012'
            director = 'A. Director'
            duration = ['100m', '1h40m']
            language = ['ITA', 'Italian']
            country = 'Italy'
            part = '1'
            self.info = {
                       'title': title,
                       'aka': aka,
                       'year': year,
                       'director': director,
                       'duration': duration,
                       'language': language,
                       'country': country,
                       'part': part
                       }

        else:
            path, name = os.path.split(filepath)
            name, extension = os.path.splitext(name)
            # file path (only directory)
            self.path = os.path.normpath(unicode(path))
            # original movie title, before renaming
            self.original_name = unicode(name)
            # file extension
            self.extension = unicode(extension)
            # movie new title (after renaming)
            self.new_name = ''
            # current state
            # states are used to show a proper panel in GUI
            self.state = self.STATE_BEFORE_RENAMING
            # error occurred during renaming operation
            self.renaming_error = ''

            print('*' * 30)
            print(name)
            print('*' * 30)
            info = guess.info(name)
            self.update_info(info)
            for k in info['languages_'].keys():
                print(str(k.name) + ': ' + str(info['languages_'][k]))

#            for key in info.keys():
#                print(key + ': ' + str(info[key]))

#                if key == 'language_' or key == 'country_':
#                    print(info[key].name)

            # try to guess new movie name from current name
#            self.get_info()

#            self.guess_info()
#            movie = self.search_title_2() # XXX cosa succede se ritorna None?
#            self.set_movie_info(movie)

#            self.guess_language()
#            self.get_info()

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

    def title(self, index):
        return self.info['title'][index]

#    def get_info(self):
#        # guessing needs complete name
#        name = self.original_name + self.extension
#        print('')
#        print(name)
#
#        #XXX usare invece una funzione clean scritta da me
#        # che prenda spunto da guessit anche
#
#        # guess movie info, using guessit module
#        info = guessit.guess_movie_info(name)
#        # keep guessed title as the alternative title
##        info.update({'alternative_title': info['title']})
#        # remove everything inside parenthesis
#        # need this because of a problem with guessit module,
#        # which has some problem with parenthesis
#        name = re.sub('[([{].*?[)\]}]', ' ', name)
#        # guess name again, this time without parenthesis
#        info2 = guessit.guess_movie_info(name)
#
#        title = info2['title']
#        # remove starting and ending quotation marks and apostrophes
#        title = re.sub('^[\"\']|[\"\']$', '', title)
#        # some titles ends with 1 (example: Alien 1), 
#        # which causes wrong guessing, so remove it
#        title = re.sub('( 1)$', '', title)
#        # get only guessed title from new guess
#        info['title'] = title
#
#        #XXX potrei invece salvare la lingua direttamente in un array
#        # coi due elementi '3-lettters' e 'english name'
#        # cosi faccio prima quando calcolo il nuovo nome
#        # magari nella funzione update_info
#        language_code = guess_language.guessLanguage(name)
#        language = None
#        if 'language' in info:
#            if len(info['language']) > 1 \
#            and language_code != 'UNKNOWN':
#                for lang in info['language']:
#                    if lang.lng2() == language_code:
#                        language = lang
#            elif len(info['language']) == 1:
#                language = info['language'][0]
#        else:
#            if language_code != 'UNKNOWN':
#                language = guessit.Language(language_code)
#
#        if language != None:
#            info.update({'language': language})
#
#        if 'language' in info:
#            country = QLocale(info['language'].lng2())
#            country = QLocale.countryToString(country.country())
#            info.update({'country': country})
#
#        self.update_info(info)
#        print('')
#        print(info['title'])
#        print(info['aka'])
#        print(info['director'])
#        print(info['duration'])


    def search_new_title(self, title):
        #XXX faccio un guess su title per recuperare l'anno
        #XXX faccio anche un guess sulla lingua
        info = {
              'title': title,
              'year': self.info['year'],
              'language': self.info['language'], #XXX se non serve piu, lo tolgo
              'country': self.info['country'],
              }
        self.update_info(info)
        return info

    def update_info(self, info):

        #XXX conversione di tutte le stringhe in unicode
        #XXX aggiornare anche l'anno del film

        # create imdb search engine
        imdb_archive = imdb.IMDb()
        # search for title into IMDB, and returns some candidate movies
        movies = imdb_archive.search_movie(info['title'])
        if len(movies) > 0:
            movie = movies[0]

            info_year = info.get('year')
            # sometimes, with movies with an old version and a new version
            # (e.g. Godzilla: a 1954 version and a 1998 version)
            # imdb search returns the oldest one as the second result.
            # so, keep movie year found on title into consideration as
            # discrimination for the right movie
            if info_year != None \
            and len(movies) > 1:
                movie_year = movies[1].get('year')
                if movie_year != None \
                and info_year == str(movie_year):
                    movie = movies[1]
            # if no year has been found in title, try to use the movie one
            if info_year == None:
                movie_year = movies[0].get('year')
                if movie_year != None:
                    info.update({'year': str(movie_year)})

            original_title = info['title']
            # get more info on this movie
            imdb_archive.update(movie) #XXX , info=None) info is the list of sets of information to retrieve.
            # update title
            title = []
            movie_title = movie.get('title')
            if movie_title != None:
                title.append(movie_title)
                print(movie_title)
            else:
                title.append(info['title'])
            movie_canonical_title = movie.get('canonical title')
            if movie_canonical_title != None:
                title.append(movie_canonical_title)
            else:
                title.append(info['title'])
            info.update({'title': title})
            # add aka
            best_aka = movie['title']
            best_score = 0
            language = ''
            akas = []
            countries = []
            movie_akas = movie.get('akas')
            if movie_akas != None:
                for aka in movie_akas:
#                    aka.encode('utf-8')
#                    aka = unicodedata.normalize('NFKD', aka).encode('ascii', 'ignore')
#                    print(aka.encode('utf-8'))
#                    try: #XXX è proprio necessario? se faccio delle conversioni in unicode?
                    aka = aka.split('::')
                    if len(aka) == 2:
                        akas.append(aka[0])
#                        print(gl.guessLanguageName(aka[0]))
    #                    print(aka[0])
                        raw_aka_countries = aka[1].split(', ')
                        aka_countries = []
                        for country in raw_aka_countries:
                            country = re.sub('[(].*?[)]', '', country).strip()
                            aka_countries.append(country)
                        countries.append(aka_countries)

            akas = dict(zip(akas, countries))
            best_akas = difflib.get_close_matches(original_title, akas.keys(), 1)
            if len(best_akas) > 0:
                best_aka = best_akas[0]

#                language_code = gl.guessLanguage(best_aka)
#                if language_code != 'UNKNOWN':
#                    found_language = pycountry.languages.get(alpha2 = language_code)
#                    if found_language in info['languages_']:
#                        info['languages_'].update({found_language: info['languages_'][found_language] + 1})
#                    else:
#                        info['languages_'].update({found_language: 1})

                countries = akas[best_aka]
                for country in countries:
                    if country in pycountry.countries:
                        found_country = pycountry.countries.get(name = country)
                        found_language = pycountry.languages.get(alpha2 = found_country.alpha2.lower())
                        if found_language in info['languages_']:
                            info['languages_'].update({found_language: info['languages_'][found_language] + 1})
                        else:
                            info['languages_'].update({found_language: 1})

#                    score = difflib.SequenceMatcher(None, aka[0].lower(), original_title.lower()).ratio()
#                    if score > best_score:
#                        best_score = score
#                        best_aka = aka[0]
#                        language = gl.guessLanguageName(aka[0])

#                    print(score)
#                    print(language_code)
#                    if 'country' in info \
#                    and len(aka) == 2:
#                        country = re.sub('[(].*?[)]', '', aka[1])
#                        country = country.strip()
#                        if country == info['country']:
#                            best_aka = aka[0]
#                    except UnicodeEncodeError:
#                        pass

#            print('*' * 20)
#            print(best_aka)
#            print(best_score)
#            print(language)
            info.update({'aka': best_aka})
            # add director(s)            
            directors = ''
            movie_directors = movie.get('director')
            if movie_directors != None:
                directors = []
                for director in movie_directors:
                    directors.append(director['name'])
                directors = ', '.join(directors)
            info.update({'director': directors})
        # no movies found
        else:
            info.update({'title': [info['title'], info['title']]})
            info.update({'aka': info['title']})
            info.update({'director': ''})
        # add duration
        duration = 0
        try:
            video_info = enzyme.parse(self.get_abs_original_name())
        except ValueError:
            pass
        else:
            if video_info.length != None:
                duration = int(video_info.length / 60)
            elif video_info.video[0].length != None:
                duration = int(video_info.video[0].length / 60)
        if duration == 0 \
        and len(movies) > 0:
            runtimes = movie.get('runtimes')
            if runtimes != None:
                #XXX per adesso tengo solo il primo runtime,
                # ma sarebbe interessante considerare le info di ciascun runtime sulla
                # country associata (es: [u'92', u'South Korea:97::(uncut version)', u'Japan:98'])
                runtime = runtimes[0]
                match = re.search('\d+', runtime)
                if match:
                    runtime = match.group(0)
                    duration = int(runtime)
        if duration != 0:
            duration1 = str(duration) + 'm'
            hours = int(duration / 60)
            minutes = int(duration % 60)
            duration2 = str(hours) + 'h'
            if minutes != 0:
                duration2 = duration2 + str(minutes) + 'm'
            duration = [duration1, duration2]
        else:
            duration = ['', '']
        info.update({'duration': duration})

    def update_info_old(self, info):

        #XXX conversione di tutte le stringhe in unicode
        #XXX aggiornare anche l'anno del film

        # create imdb search engine
        imdb_archive = imdb.IMDb()
        # search for title into IMDB, and returns some candidate movies
        movies = imdb_archive.search_movie(info['title'])
        if len(movies) > 0:
            movie = movies[0]

            info_year = info.get('year')
            if info_year != None:
                movie_year = movies[1].get('year')
                if movie_year != None \
                and info_year == movie_year:
                    movie = movies[1]

            # get more info on this movie
            imdb_archive.update(movie)
            # update title
            info.update({'title': [movie['title'], movie['canonical title']]})
            # add aka
            best_aka = movie['title']
            akas = movie.get('akas')
            if akas != None:
                for aka in akas:
                    try: #XXX è proprio necessario? se faccio delle conversioni in unicode?
                        aka = aka.split('::')
                        if 'country' in info \
                        and len(aka) == 2:
                            country = re.sub('[(].*?[)]', '', aka[1])
                            country = country.strip()
                            if country == info['country']:
                                best_aka = aka[0]
                    except UnicodeEncodeError:
                        pass
            info.update({'aka': best_aka})
            # add director(s)            
            directors = ''
            movie_directors = movie.get('director')
            if movie_directors != None:
                directors = []
                for director in movie_directors:
                    directors.append(director['name'])
                directors = ', '.join(directors)
            info.update({'director': directors})
        else:
            info.update({'title': [info['title'], info['title']]})
            info.update({'aka': ''})
            info.update({'director': ''})
        # add duration
        duration = 0
        try:
            video_info = enzyme.parse(self.get_abs_original_name())
        except ValueError:
            pass
        else:
            if video_info.length != None:
                duration = int(video_info.length / 60)
            elif video_info.video[0].length != None:
                duration = int(video_info.video[0].length / 60)
        if duration != 0 \
        and len(movies) > 0:
            runtimes = movie.get('runtimes')
            if runtimes != None:
                #XXX per adesso tengo solo il primo runtime,
                # ma sarebbe interessante considerare le info di ciascun runtime sulla
                # country associata (es: [u'92', u'South Korea:97::(uncut version)', u'Japan:98'])
                runtime = runtimes[0]
                match = re.search('\d+', runtime)
                if match:
                    runtime = runtime[match.start():match.end()]
                    duration = int(runtime)
        if duration != 0:
            duration1 = str(duration) + 'm'
            hours = int(duration / 60)
            minutes = int(duration % 60)
            duration2 = str(hours) + 'h'
            if minutes != 0:
                duration2 = duration2 + str(minutes) + 'm'
            duration = [duration1, duration2]
        else:
            duration = ['', '']
        info.update({'duration': duration})

#    def search_title_3(self, info):
#        """
#        search given title on IMDB, and get corresponding movies info
#        """
#
#        # XXX e se invece questa funzione aggiornasse solo il diz info,
#        # quando lo score è maggiore di, diciamo, 0.8?
#        # altrimenti c'è il problema di recuperare o meno l'aka,
#        # nel senso che se ritorno solo il movie più simile,
#        # non so se e quale aka devo tenere come migliore...
#
#        #XXX attenzione! in realtà ci sono dei titoli, vedi The Grudge, che
#        # hanno lo stesso titolo sia nella versione americana che
#        # nella versione giapponese.. come faccio a distinguerli?
#
#        #XXX da indagare meglio:
#        # Amer: 5o titolo [si anno]
#        # quelli di Dario Argento: titolo trovato da guessit: Dario Argento, invece del titolo vero
#        # quelli di Michael Moor: titolo trovato da guessit: Michael Moor, invece del titolo vero
#        # ET l'extraterrestre: 3o titolo [no anno]
#        # Fahrenheit 9: 5o titolo [no anno]
#        # FBI protezione testimoni II: 2o titolo [no anno]
#        # Forrest Gump: 11o titolo?? [no anno]
#        # Gran Torino: 2o titolo [si anno]
#        # Il buio: 4o titolo [no anno]
#        # Il Buono, Il Brutto e Il Cattivo: 3o titolo [no anno]
#        # Il Magico Mondo Di Amelie: 5o titolo [no anno]
#        # L' Ultima Casa a Sinistra: 2o titolo [si anno] > giusto
#        # La fortezza: 2o titolo [si anno] > giusto
#        # The Amityville Horror: 2o titolo [si anno] > giusto
#        # The Day After: 2o titolo [si anno] > giusto
#        # Ombre dal passato: 3o titolo [si anno] 
#        # ricky 6: 5o titolo [si anno]
#        # Zombie: 8o titolo [si anno]
#        # Lupin: 2o titolo [no anno]
#        # Wargames: 2o titolo [no anno]
#        # Porco rosso di Hayao Miyazaki: 2o titolo [no anno]
#        # Un uomo: 20o posto (che cavolo è??)
#        # controllare anno 
#
#        #XXX guessit considera gli articoli italiani tipo 'lo' come lingue,
#        # cosa che in realtà è sbagliata. contattare gli autori!
#
#        # create imdb search engine
#        imdb_archive = imdb.IMDb()
#        # search for title into IMDB, and returns some candidate movies
#        candidate_movies = imdb_archive.search_movie(info['title'])
#        best_movie = None
#        best_score = 0
#
##        print('*' * 5 + info['title'] + '*' * 5)
#
#        for movie in candidate_movies:
##        for i in range(len(candidate_movies)):
##            movie = candidate_movies[i]
#
##            for item in movie.items():
##                print(str(item))
##            print('*' * 5 + movie['title'])
#
#            info_year = info.get('year')
#            movie_year = movie.get('year')
#            same_year = False
#            if info_year != None \
#            and movie_year != None \
#            and info_year == movie_year:
#                same_year = True
#
#            string1 = unicode(info['title'].lower())
#            string2 = unicode(movie['title'].lower())
#            score = difflib.SequenceMatcher(None, string1 , string2).ratio()
#
#            if same_year:
#                score += 1
#
#            if score > best_score:
#                best_score = score
#                best_movie = movie
#
#            akas = movie.get('akas')
#            if akas != None:
#                for aka in akas:
#                    try:
##                        print(aka)
#                        aka = aka.split('::')
#
#                        string1 = unicode(info['title'].lower())
#                        string2 = unicode(aka[0].lower())
#                        score = difflib.SequenceMatcher(None, string1 , string2).ratio()
#
#                        if same_year:
#                            score += 1
#
#                        if 'country' in info:
#                            country = re.sub('[(].*?[)]', '', aka[1])
#                            country = country.strip()
#                            if country == info['country']:
#                                score += 2
#
#                        if score > best_score:
#                            best_score = score
#                            best_movie = movie
#                    except UnicodeEncodeError:
#                        pass
#
##        print('')
##        print('best movie\t' + '-' * 30 + '> ' + unicode(best_movie['title']))
###        print('best movie index\t' + '-' * 30 + '> ' + str(best_movie_index))
##        print('best aka\t' + '-' * 30 + '> ' + unicode(best_aka))
##        print('best score\t' + '-' * 30 + '> ' + unicode(best_score))
##        print('')
#
##        print(best_score)
#        #XXX da ripristinare il valore di confronto
#        if best_score > 0.0:
#            movie = best_movie
#            title = info['title']
#            # get more info on this movie
#            imdb_archive.update(movie)
#            # update title
#            info['title'] = movie['title']
#            # add aka
#            best_aka = ''
#            best_aka_score = 0
#            akas = movie.get('akas')
#            if akas != None:
#                for aka in akas:
#                    try:
#                        aka = aka.split('::')
#                        string1 = unicode(title.lower())
#                        string2 = unicode(aka[0].lower())
#                        score = difflib.SequenceMatcher(None, string1 , string2).ratio()
#                        if 'country' in info \
#                        and len(aka) == 2:
#                            country = re.sub('[(].*?[)]', '', aka[1])
#                            country = country.strip()
#                            if country == info['country']:
#                                score += 1
#                        if score > best_aka_score:
#                            best_aka_score = score
#                            best_aka = aka[0]
#                    except UnicodeEncodeError:
#                        pass
#            info.update({'aka': best_aka})
#            # add director(s)            
#            directors = ""
#            movie_directors = movie.get('director')
#            if movie_directors != None:
#                directors = []
#                for director in movie_directors:
#                    directors.append(director['name'])
#                directors = ', '.join(directors)
#            info.update({'director': directors})
#            # add duration
#            video_info = enzyme.parse(self.get_abs_original_name())
#            duration = 0
#            if video_info.length != None:
#                duration = int(video_info.length / 60)
#            elif video_info.video[0].length != None:
#                duration = int(video_info.video[0].length / 60)
#            else:
#                runtimes = movie.get('runtimes')
#                if runtimes != None:
#                    #XXX per adesso tengo solo il primo runtime,
#                    # ma sarebbe interessante considerare le info di ciascun runtime sulla
#                    # country associata (es: [u'92', u'South Korea:97::(uncut version)', u'Japan:98'])
#                    runtime = runtimes[0]
#                    match = re.search('\d+', runtime)
#                    if match:
#                        runtime = runtime[match.start():match.end()]
#                        duration = int(runtime)
#            info.update({'duration': duration})
#        else:
#            # add aka
#            info.update({'aka': ''})
#            # add director(s)
#            info.update({'director': ''})
#            # add duration
#            info.update({'duration': ''})

#    def search_title_2(self):
#        """
#        search given title on IMDB, and get corresponding movies info
#        """
#
#        # create imdb search engine
#        imdb_archive = imdb.IMDb()
#        # search for title into IMDB, and returns some candidate movies
#        candidate_movies = imdb_archive.search_movie(self.title)
#        best_movie = None
#        best_score = 0
#        best_title = "" # XXX da togliere
#        best_aka = "" # XXX da togliere
#        print(self.title)
#        for movie in candidate_movies:
##            for item in movie.items():
##                print(str(item))
#            print(movie['title'])
#            year = 0
#            if 'year' in movie:
#                year = movie['year']
#            score = self.get_title_ratio(movie['title'], year)
#            if score > best_score:
#                best_score = score
#                best_movie = movie
#                best_title = movie['title'] # XXX da togliere
#                best_aka = "" # XXX da togliere
#            if 'akas' in movie:
#                akas = movie['akas']
#                for aka in akas:
#                    try:
#                        # sometimes the AKAs list ends with a u'\xbb', so I remove it
##                        if aka != u'\xbb':                            
#                        aka = aka.split('::')
##                        if len(splitted_aka) > 1:
##                            akas.append(splitted_aka[0])
#                        print(aka[0])
#                        score = self.get_title_ratio(aka[0], year)
#                        if score > best_score:
#                            best_score = score
#                            best_movie = movie
#                            best_title = movie['title'] # XXX da togliere
#                            best_aka = aka[0] # XXX da togliere
#                    except UnicodeEncodeError:
#                        pass
#        print('best movie ' + '-' * 30 + '> ' + best_title)
#        print('best aka ' + '-' * 30 + '> ' + best_aka)
#        print('best score ' + '-' * 30 + '> ' + str(best_score))
#        print('')
#        return best_movie
#
#    def get_title_ratio(self, title, year):
#        # XXX usare anche la lingua per comparare l'aka?
#        sm = difflib.SequenceMatcher(None, self.title, title)
#        score = sm.ratio()
#        if self.year != 0 \
#        and year != 0 \
#        and self.year == year:
#            score += 1
#        print(score)
#        return score

#    def set_movie_info(self, movie):
#        # create imdb search engine
#        imdb_archive = imdb.IMDb()
#        # get other information from IMDB
#        imdb_archive.update(movie)
#        # store only some information returned by IMDB (most useful ones)
#        # I also clean these information and store them in a useful format.
#        # set title
#        self.title = movie['title']
#        # set canonical title        
#        # not every movie returns a canonical title...
#        if 'canonical title' in movie:
#            self.canonical_title = movie['canonical title']
#        # set akas
#        self.akas = []
#        # first aka is the original title
#        self.akas.append(movie['title'])
#        self.akas_index = 0
#        if 'akas' in movie:
#            # select AKAS index based on most probable language.
#            # loop on akas
#            akas = movie['akas']
#            for i in range(len(akas)):
#                aka = akas[i]
##                try:
#                aka = aka.split('::')
#                self.akas.append(aka[0])
##                except UnicodeEncodeError:
##                    pass
#
#                # if spanish language is the most probable one and if current AKAS
#                # is the spanish one...
#                if self.language_index == 1 and re.search(r'Spain', aka[1]):
#                    # ... select it.
#                    akas_index = i + 1
#                # the same for other languages
#                elif self.language_index == 2 and re.search(r'Germany', aka[1]):
#                    akas_index = i + 1
#                elif self.language_index == 3 and re.search(r'France', aka[1]):
#                    akas_index = i + 1
#                elif self.language_index == 4 and re.search(r'Italy', aka[1]):
#                    akas_index = i + 1
#
#        if 'year' in movie:
#            self.year = movie['year']
#
#        if 'director' in movie:
#            directors = []
#            for director in movie['director']:
#                directors.append(director['name'])
#            self.director = ', '.join(directors)
#
#        run_times = []
#        run_times_index = 0
#        if 'runtimes' in movie:
#            for run_time in movie['runtimes']:
#                # from runtimes, get only numbers representing time
#                match = re.search('\d+', run_time)
#                if match:
#                    run_times.append(run_time[match.start():match.end()])

#    def search_title(self, title):
#        """
#        search given title on IMDB, and get corresponding movies info
#        """
#
#        # reset current movies and indexes
#        self.info_index = 0
#        self.info = []
#        # create imdb search engine
#        imdb_archive = imdb.IMDb()
#        # search for title into IMDB, and returns some candidate movies
#        candidate_movies = imdb_archive.search_movie(title)
#        # if no movies corresponding to that title are found
#        if len(candidate_movies) == 0:
#            return
#        # keep only the first three returned results
#        movies = candidate_movies[:3]
#        # for each found movie..
#        for movie in movies:
#            # get other information from IMDB
#            imdb_archive.update(movie)
#            # creates new pairs of keys and values because I don't want to store all
#            # the information returned by IMDB, but only the most useful ones.
#            # I also clean these information and stores them in a useful format.
#            keys = []
#            values = []
#            # get title
#            keys.append(self.TITLE)
#            values.append(movie[self.TITLE])
#            # get canonical title
#            keys.append(self.CANONICAL_TITLE)
#            canonical_title = ""
#            # not every movie returns a canonical title...
#            try:
#                canonical_title = movie['canonical title']
#            except KeyError:
#                pass
#            values.append(canonical_title)
#            # get akas
#            keys.append(self.AKAS)
#            keys.append(self.AKAS_INDEX)
#            akas = []
#            # first aka is the original title
#            akas.append(movie[self.TITLE])
#            akas_index = 0
#            try:
#                # example of AKAs for "Near Dark" movie:
#                # u'"Cuando cae la oscuridad" - Argentina, Mexico',
#                # u'"Agria nyhta" - Greece',
#                # u'"Aux fronti\xe8res de l\'aube" - France'
#                # u'"Blisko ciemnosci" - Poland'
#                # u'"Depois do Anoitecer" - Portugal'
#                # u'"Il buio si avvicina" - Italy'
#                # u'"Los viajeros de la noche" - Spain'
#                # u'"Natten har sitt pris" - Sweden'
#                # u'"Near Dark - Die Nacht hat ihren Preis" - West Germany'
#                # u'"Pimeyden l\xe4heisyys" - Finland'
#                # u'"Quando Chega a Escurid\xe3o" - Brazil'
#
#                # select AKAS index based on most probable language.
#                # loop on akas
#                akas_original = movie[self.AKAS]
#                for i in range(len(akas_original)):
#                    # get AKAS
#                    try:
#                        aka = unicode(akas_original[i])
#                    except UnicodeEncodeError:
#                        pass
#
#                    # if spanish language is the most probable one and if current AKAS
#                    # is the spanish one...
#                    if self.language_index == 1 and re.search(r'Spain', aka):
#                        # ... select it.
#                        akas_index = i
#                    # the same for other languages
#                    elif self.language_index == 2 and re.search(r'Germany', aka):
#                        akas_index = i
#                    elif self.language_index == 3 and re.search(r'France', aka):
#                        akas_index = i
#                    elif self.language_index == 4 and re.search(r'Italy', aka):
#                        akas_index = i
#
#                    # sometimes the AKAs list ends with a u'\xbb', so I remove it
#                    if aka != u'\xbb':
#                        # takes only the AKAS title
#                        # under Linux
#                        if aka.startswith('"'):
#                            splitted_aka = aka.split('"')
#                            if len(splitted_aka) > 1:
#                                akas.append(splitted_aka[1])
#                        # or under Windows
#                        else:
#                            splitted_aka = aka.split('::')
#                            if len(splitted_aka) > 1:
#                                akas.append(splitted_aka[0])
#            except KeyError:
#                pass
#            values.append(akas)
#            values.append(akas_index)
#
#            keys.append(self.YEAR)
#            year = ""
#            try:
#                year = unicode(movie[self.YEAR])
#            except KeyError:
#                pass
#            values.append(year)
#
#            keys.append(self.DIRECTOR)
#            directors = []
#            try:
#                for director in movie['director']:
#                    directors.append(director['name'])
#            except KeyError:
#                pass
#            values.append(', '.join(directors))
#
#            keys.append(self.RUNTIMES)
#            keys.append(self.RUNTIMES_INDEX)
#            runtimes = []
#            runtimes_index = 0
#            try:
#                for runtime in movie[self.RUNTIMES]:
#                    # from runtimes, get only numbers representing time
#                    match = re.search(r"(\d+)", runtime)
#                    if match:
#                        runtimes.append("{0}".format(runtime[match.start():match.end()]))
#            except KeyError:
#                pass
#            values.append(runtimes)
#            values.append(runtimes_index)
#            # populate info with keys and values extracted from candidateMovie
#            self.info.append(dict(zip(keys, values)))

    def generate_new_name(self, renaming_rule):
        """
        generates new file name based on given renaming rule
        """

        if len(renaming_rule) == 0:
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
            self.new_name = unicode(''.join(new_name).strip())

        return self.new_name

    def generate_new_name_old(self, renaming_rule):
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
        replace_with = ""
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



