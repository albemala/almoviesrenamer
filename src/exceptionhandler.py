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
    time_info = time.strftime("%Y-%m-%d, %H:%M:%S")
    architecture_info = platform.architecture()[0]
    os_info = platform.platform()
    locale_info = locale.getdefaultlocale()[0]
    program_info = utils.PROGRAM_VERSION
    python_info = platform.python_version()
    qt_info = str(QT_VERSION_STR)
    pyqt_info = str(PYQT_VERSION_STR)
    try:
        import sipconfig
        sip_info = sipconfig.Configuration().sip_version_str
    except ImportError:
        sip_info = ''
    imdbpy_info = str(imdb.VERSION)
    error_info = traceback.format_exc()

    separator = '-' * 60

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
          separator,
          error_info,
          '\n'
          ]

    info_str = '\n'.join(info)

    save_on_file(info_str)
    send_to_ws(info_str)

def save_on_file(info_str):
    if not os.path.isdir(LOG_PATH): os.mkdir(LOG_PATH)

    log_file_name = time.strftime("%Y-%m-%d") + ".log"
    log_file = os.path.join(LOG_PATH, log_file_name)

    try:
        with open(log_file, "a") as f:
            f.write(info_str)
    except IOError:
        pass

def send_to_ws(info_str):
    url = "http://almoviesrenamer.appspot.com/exceptions"
    values = {
        'exception' : info_str
    }
    data = urllib.urlencode(values)
    # call web service
    f = urllib2.urlopen(url, data)





