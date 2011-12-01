# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

# Python version: 2.6
#
# Revision: 11
#
# TODO
# - i dati di log dovrebbero essere inviati in automatico tramite email o ftp o
# altro senza chiedere niente all'utente, e senza visualizzare nessuna dialog.
# guardare eric ide per questa feature.

from PyQt4.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
import cStringIO
import imdb
import locale
import os.path
import sys
import time
import traceback

# directory used to store logs
LOG_PATH = os.path.abspath("log")

def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.

    Thanks to <a href="http://eric-ide.python-projects.org/">Eric IDE</a>
    for this code.

    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """

    separator = '-' * 80
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    versionInfo = "Version Numbers:\n"

    versionInfo += "Python: {0}\n".format(sys.version.split()[0])

    versionInfo += "Qt: {0}\n".format(str(QT_VERSION_STR))
    versionInfo += "PyQt4: {0}\n".format(str(PYQT_VERSION_STR))
    try:
        import sipconfig
        sip_version_str = sipconfig.Configuration().sip_version_str
    except ImportError:
        sip_version_str = "version not available"
    versionInfo += "sip: {0}\n".format(str(sip_version_str))

    versionInfo += "IMDbPY: {0}\n".format(str(imdb.VERSION))

    versionInfo += "{0}: {1}\n".format(utils.PROGRAM_NAME, utils.PROGRAM_VERSION)

    versionInfo += "\nPlatform:\n{0}\n{1}\n{2}".format(sys.platform, sys.version, locale.getdefaultlocale()[0])

    errmsg = '{0}: \n{1}'.format(str(excType), str(excValue))

    tbinfofile = cStringIO.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()

    sections = [separator, timeString, separator, versionInfo, separator, tbinfo, separator, errmsg]
    msg = '\n'.join(sections) + '\n' * 3

    if not os.path.isdir(LOG_PATH): os.mkdir(LOG_PATH)

    logFileName = time.strftime("%Y-%m-%d") + "_errors.log"
    logFile = os.path.join(LOG_PATH, logFileName)

    try:
        with open(logFile, "a") as f:
            f.write(msg)
    except IOError:
        pass


if __name__ == "__main__":

    sys.excepthook = excepthook

    a = 10
    b = a / 0
