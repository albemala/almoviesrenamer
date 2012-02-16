# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

# program name and version, used in excepthook
PROGRAM_NAME = "ALmoviesRenamer"
PROGRAM_VERSION = "3.0"

def load_languages():
    global name_to_language_
    name_to_language_ = dict()
    global alpha3_to_language_
    alpha3_to_language_ = dict()
    global country_to_language_
    country_to_language_ = dict()
    languages = []
    with open('languages.txt', 'r') as f:
        for line in f:
            name, alpha3, countries = line.rstrip('\n').split('|')
            language = [name, alpha3]
            name_to_language_.update({name: language})
            alpha3_to_language_.update({alpha3: language})
            countries = countries.split(';')
            for country in countries:
                country_to_language_.update({country: language})

def alpha3_to_language(given_alpha3):
    try:
        return alpha3_to_language_[given_alpha3]
    except KeyError:
        return None

def name_to_language(given_name):
    try:
        return name_to_language_[given_name]
    except KeyError:
        return None

def country_to_language(given_country):
    try:
        return country_to_language_[given_country]
    except KeyError:
        return None

