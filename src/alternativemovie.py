# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

class AlternativeMovie:
    """    
    """

    def __init__(self, title, countries, year, movie):
        """
        constructor.
        """
        self.title = title
        self.countries = countries
        self.year = year
        self.movie = movie

    def title(self):
        return self.title

    def countries(self):
        return self.countries

    def year(self):
        return self.year

    def movie(self):
        return self.movie
