__author__ = "Alberto Malagoli"

# TODO instead of reading from txt file, create a python file with the dictionary already filled?
# TODO in any case, create a different class to handle the language conversions
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
            name, alpha3, countries = str(line).rstrip('\n').rstrip('\r').split('|')
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


# TODO
def send_usage_statistics():
    pass
    # """
    # checks user choice about sending usage statistics and
    # sends usage statistics to a dedicated web service
    # """
    #
    # # get user choice about sending usage statistics
    # send_usage_statistics = utils.preferences.value("stats_agreement").toInt()[0]
    # # if user chose to send usage statistics
    # if send_usage_statistics == PreferencesDialog.STATS_AGREE:
    #     # start sending thread
    #     threading.Thread(target = send_usage_statistics_run).start()


# TODO
def send_usage_statistics_run():
    pass
    # """
    # sends usage statistics to a dedicated web service
    # """
    #
    # # get preferences
    # rule = utils.preferences.value("renaming_rule").toString()
    # duration = utils.preferences.value("duration_representation").toString()
    # language = utils.preferences.value("language_representation").toString()
    # separator = utils.preferences.value("words_separator").toString()
    # # web service url
    # url = "http://almoviesrenamer.appspot.com/stats"
    # # create data
    # values = {
    #     'rule' : rule,
    #     'duration' : duration,
    #     'language' : language,
    #     'separator' : separator
    # }
    # data = urllib.urlencode(values)
    # # POST send data to web service
    # f = urllib2.urlopen(url, data)

    # TODO


def check_connection(self):
    pass


#     """
#     checks if internet connection is up.
#
#     if internet connection is down, notifies the user with a message.
#     """
#
#     try:
#         # try to open a web URL
#         f = urllib2.urlopen("http://www.google.com/")
#     except URLError:
#         # if an error occurs, notify the user with a message
#         msg_box = QMessageBox()
#         msg_box.setWindowTitle( "Internet connection down?")
#         msg_box.setText( """
# <p>It seems your internet connection is down (but maybe I'm wrong).</p>
# <p>That program needs access to the internet, to get information about movies, so please check your connection.</p>
# <p>If I'm wrong, sorry for the interruption...</p>
#             """)
#         icon = QPixmap()
#         icon.load('icons/exclamation.png')
#         msg_box.setIconPixmap(icon)
#         msg_box.exec_()

# TODO
def check_new_version(self):
    pass
    #     """
    #     checks for new program version, and notify in case of
    #     a newer version
    #     """
    #
    #     # create url, with current program version
    #     url = "http://almoviesrenamer.appspot.com/checknewversion"
    #     # call web service
    #     f = urllib2.urlopen(url)
    #     # read the answer (could be "yes" for new version, or "no")
    #     version = f.read().rstrip('\n')
    #     # if there is a new version
    #     if version != utils.PROGRAM_VERSION:
    #         title =  "New version available"
    #         msg =  """
    # <p>A new version of {0} is available: <b>{1}</b></p>
    # <p><a href="http://code.google.com/p/almoviesrenamer/downloads/list">Download it.</a></p>
    #             """.format(utils.PROGRAM_NAME, version)
    #         # show a notification dialog, with link to download page
    #         QMessageBox.information(None, title, msg)
