# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QSettings
from cx_Freeze import setup, Executable
from glob import glob
import os.path
import os
import shutil
import sys
import platform
sys.path.append('src')
import utils

## change setting first_time before building
# load settings
settings = QSettings("src/preferences.ini", QSettings.IniFormat)
# save value on settings file
settings.setValue("first_time", True)
settings.setValue("stats_agreement", 1)
settings.setValue("duration_representation", 0)
settings.setValue("language_representation", 1)
settings.setValue("words_separator", 0)
settings.sync()

if os.path.isdir('build'):
    shutil.rmtree('build')
if os.path.isdir('src/log'):
    shutil.rmtree('src/log')

includes = [
            'enzyme'
            ]

excludes = [
            '_gtkagg',
            '_tkagg',
            'bsddb',
            'curses',
            'email',
            'pywin.debugger',
            'pywin.debugger.dbgcon',
            'pywin.dialogs',
            'tcl',
            'Tkconstants',
            'Tkinter',
            ]

include_files = [
                 ("src/enzyme", "enzyme"),
                 ("src/icons", "icons"),
                 ("src/qm", "qm"),
                 ("src/main_window.ui", "main_window.ui"),
                 ("src/preferences_dialog.ui", "preferences_dialog.ui"),
                 ("src/renaming_rule_dialog.ui", "renaming_rule_dialog.ui"),
                 ("src/stats_agreement_dialog.ui", "stats_agreement_dialog.ui"),
                 ("src/preferences.ini", "preferences.ini"),
                 ("src/languages.txt", "languages.txt"),
                 "CHANGELOG.txt",
                 "gpl-3.0.txt",
                 "README.txt"
                 ]

base = None
target_name = utils.PROGRAM_NAME
archive_format = "gztar"
if sys.platform == "win32":
    base = "Win32GUI"
    target_name += ".exe"
    archive_format = "zip"

setup(
      name = utils.PROGRAM_NAME,
      version = utils.PROGRAM_VERSION,
      author = "Alberto Malagoli",
      author_email = 'albemala@gmail.com',
      url = 'https://code.google.com/p/almoviesrenamer/',
      options = dict(
                     build_exe = {"includes": includes,
                                  "excludes": excludes,
                                  "include_files": include_files,
                                  "optimize": 2,
                                  "create_shared_zip": True
                                  }),
      executables = [Executable(
                                script = "src/main.py",
                                base = base,
                                targetName = target_name,
                                icon = "src/icons/brand.ico",
                                compress = True,
                                )]
      )

archive_name = "dist/{0}-{1}-{2}" \
    .format(utils.PROGRAM_NAME, utils.PROGRAM_VERSION, sys.platform)
if os.path.isfile(archive_name):
    os.remove(archive_name)
python_version = platform.python_version_tuple()
root_dir = os.path.abspath("build/exe.{0}-{1}.{2}" \
    .format(sys.platform, python_version[0], python_version[1]))
print("create " + archive_format + " " + archive_name)
shutil.make_archive(archive_name, archive_format, root_dir)

print("END")


