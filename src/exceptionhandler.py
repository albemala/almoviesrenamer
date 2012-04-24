# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
import imdb
import locale
import os.path
import time
import traceback
import platform
import urllib
import urllib2
import utils

# directory used to store logs
LOG_PATH = os.path.abspath("log")

def save_exception():
    """
    collect data on exceptions, and save them on file and to a web service
    """

    # current time
    time_info = time.strftime("%Y-%m-%d, %H:%M:%S")
    # x86 or x64
    architecture_info = platform.architecture()[0]
    # OS
    os_info = platform.platform()
    # language
    locale_info = locale.getdefaultlocale()[0]
    # program version
    program_info = utils.PROGRAM_VERSION
    # python version
    python_info = platform.python_version()
    # qt version
    qt_info = str(QT_VERSION_STR)
    # pyqt version
    pyqt_info = str(PYQT_VERSION_STR)
    try:
        import sipconfig
        # sip version
        sip_info = sipconfig.Configuration().sip_version_str
    except ImportError:
        sip_info = ''
    # imdbpy version
    imdbpy_info = str(imdb.VERSION)
    # enzyme version
    enzyme_info = "0.2"
    # error data
    error_info = traceback.format_exc()
    # separator 
    separator = '-' * 60
    # create info list
    info = [
          separator,
          time_info,
          separator,
          "Architecture: " + architecture_info,
          "Operative System: " + os_info,
          "Locale: " + locale_info,
          utils.PROGRAM_NAME + ": " + program_info,
          "Python: " + python_info,
          "Qt: " + qt_info,
          "PyQt: " + pyqt_info,
          "sip: " + sip_info,
          "IMDbPY: " + imdbpy_info,
          "enzyme: " + enzyme_info,
          separator,
          error_info,
          '\n'
          ]
    # create a string
    info_str = '\n'.join(info)

    save_on_file_(info_str)
    send_to_ws_(info_str)

def save_on_file_(info_str):
    """
    save collected exceptions data on file
    """

    if not os.path.isdir(LOG_PATH): os.mkdir(LOG_PATH)

    log_file_name = time.strftime("%Y-%m-%d") + ".log"
    log_file = os.path.join(LOG_PATH, log_file_name)

    try:
        with open(log_file, "a") as f:
            f.write(info_str)
    except IOError:
        pass

def send_to_ws_(info_str):
    """
    send collected exceptions data to a web service
    """

    url = "http://almoviesrenamer.appspot.com/exceptions"
    values = {
        'exception' : info_str
    }
    data = urllib.urlencode(values)
    # call web service
    f = urllib2.urlopen(url, data)





