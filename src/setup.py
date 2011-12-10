# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from cx_Freeze import setup, Executable
import sys
import os.path
import utils

## change setting first_time before building
from PyQt4.QtCore import QSettings
# load settings
settings = QSettings("settings.ini", QSettings.IniFormat)
# save value on settings file
settings.setValue("first_time", True)
settings.sync()

includes = []

excludes = [
#            '_gtkagg',
#            '_tkagg',
#            'bsddb',
#            'curses',
#            'email',
#            'pywin.debugger',
#            'pywin.debugger.dbgcon',
#            'pywin.dialogs',
#            'tcl',
#            'Tkconstants',
#            'Tkinter',
#            'win32api',
#            '_ssl',
#            '_sqlite3'
            ]

include_files = [
                 "ui",
                 "settings.ini",
                 "tr/app_de.qm",
                 "tr/app_es.qm",
                 "tr/app_fr.qm",
                 "tr/app_it.qm",
                 ("../CHANGELOG.txt", "CHANGELOG.txt",),
                 ("../gpl-3.0.txt", "gpl-3.0.txt",),
                 ("../README.txt", "README.txt",)
                 ]

buildOptions = dict(
                    includes = includes,
                    excludes = excludes,
                    include_files = include_files,
                    optimize = 2,
                    )

base = None
targetName = "ALmoviesRenamer"
if sys.platform == "win32":
    base = "Win32GUI"
    targetName += ".exe"

main_exe = Executable(
                      script = "main.py",
                      base = base,
                      targetName = targetName,
                      compress = True,
                      )

setup(
      name = utils.PROGRAM_NAME,
      version = utils.PROGRAM_VERSION,
      author = "Alberto Malagoli",
      author_email = 'albemala@gmail.com',
      url = 'https://code.google.com/p/almoviesrenamer/',
      options = dict(build_exe = buildOptions),
      executables = [main_exe]
      )



