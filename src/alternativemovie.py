# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

class AlternativeMovie:
    """    
    """

    def __init__(self, title, movie):
        """
        constructor.
        """

#        aka = unicodedata.normalize('NFKD', aka).encode('ascii', 'ignore')
        title, countries = title.split('::')

#        contries = ''
#        if len(aka) == 2:
#            contries = re.sub(' [(].*?[)]', '', aka[1])

        self.title_ = title
        self.countries_ = countries

        self.movie_ = movie

    def title(self):
        return self.title_

    def countries(self):
        return self.countries_

    def year(self):
        if self.movie_.get('year') != None:
            return unicode(self.movie_.get('year'))
        return ''

    def movie(self):
        return self.movie_
