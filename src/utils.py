# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QSettings

# program name and version, used in excepthook
PROGRAM_NAME = "ALmoviesRenamer"
PROGRAM_VERSION = "4"

def load_preferences():
    """
    loads preferences file, and keep it into the 'preferences' global variable
    """

    global preferences
    preferences = QSettings("preferences.ini", QSettings.IniFormat)

def load_languages():
    """
    creates 3 dictionaries, used to convert a language name, a 3-letters ISO 
    representation of a language, and a country name, into a language
    (with the representation used in movie class)
    """

    global name_to_language_
    name_to_language_ = dict()
    global alpha3_to_language_
    alpha3_to_language_ = dict()
    global country_to_language_
    country_to_language_ = dict()
    with open('languages.txt', 'r') as f:
        for line in f:
            name, alpha3, countries = unicode(line).rstrip('\n').rstrip('\r').split('|')
            language = [name, alpha3.upper()]
            name_to_language_.update({name: language})
            alpha3_to_language_.update({alpha3: language})
            countries = countries.split(';')
            for country in countries:
                country_to_language_.update({country: language})

def alpha3_to_language(given_alpha3):
    """
    given a 3-letters ISO representation of a language, returns 
    corresponding language
    """

    try:
        return alpha3_to_language_[given_alpha3.lower()]
    except KeyError:
        return None

def name_to_language(given_name):
    """
    given a language English name, returns 
    corresponding language
    """

    try:
        return name_to_language_[given_name]
    except KeyError:
        return None

def country_to_language(given_country):
    """
    given a country name, returns corresponding language
    """

    try:
        return country_to_language_[given_country]
    except KeyError:
        return None

