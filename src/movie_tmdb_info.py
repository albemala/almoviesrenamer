import tmdbsimple as tmdb

__author__ = "Alberto Malagoli"


class MovieTMDBInfo:
    # TODO delete this comment
    # {
    # 'total_pages': 1,
    #  'page': 1,
    # 'results': [
    # {'genre_ids': [18, 10749],
    #  'overview': "At Princeton University, John Nash struggles to make a worthwhile contribution to serve as his legacy to the world of mathematics. He finally makes a revolutionary breakthrough that will eventually earn him the Nobel Prize. After graduate school he turns to teaching, becoming romantically involved with his student Alicia. Meanwhile the government asks his help with breaking Soviet codes, which soon gets him involved in a terrifying conspiracy plot. Nash grows more and more paranoid until a discovery that turns his entire world upside down. Now it is only with Alicia's help that he will be able to recover his mental strength and regain his status as the great mathematician we know him as today..",
    # 'backdrop_path': '/5YF6MwuuKBRKLUE2dz3wetkgxAE.jpg',
    # 'original_language': 'en',
    # 'adult': False,
    # 'release_date': '2001-12-12',
    # 'original_title': 'A Beautiful Mind',
    # 'video': False,
    # 'vote_average': 7.27,
    # 'popularity': 2.245206,
    # 'poster_path': '/4SFqHDZ1NvWdysucWbgnYlobdxC.jpg',
    # 'id': 453,
    #  'vote_count': 1024,
    #  'title': 'A Beautiful Mind'}
    # ],
    #  'total_results': 1}

    def __init__(self):
        self._id = 0
        self._title = ""
        self._original_title = ""
        self._year = ""
        self._original_language = ""
        self._poster_path = ""
        self._director = ""
        self._duration = ""

    def get_title(self):
        return self._title

    def get_original_title(self):
        return self._original_title

    def get_year(self):
        return self._year

    def get_original_language(self):
        return self._original_language

    def get_poster_path(self):
        return self._poster_path

    def get_director(self):
        return self._director

    def get_duration(self):
        return self._duration

    def fill_with_search_result(self, result):
        self._id = result["id"]
        self._title = result["title"]
        self._original_title = result["original_title"]
        # release date is like 2001-12-12
        self._year = result["release_date"].split("-")[0]
        self._original_language = result["original_language"]
        self._poster_path = result["poster_path"]
        movie = tmdb.Movies(self._id)
        movie_info = movie.info()
        self._duration = movie_info["runtime"]
        movie_credits = movie.credits()
        for person in movie_credits["crew"]:
            if person["job"] == "Director":
                if self._director != "":
                    self._director += ", "
                self._director += person["name"]
        print(self._director)
