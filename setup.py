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
settings.setValue("last_visited_directory", "")
settings.setValue("renaming_rule", "title.(.year.duration.language.)")
settings.sync()

if os.path.isdir('build'):
    print("removing build path...")
    shutil.rmtree('build')
if os.path.isdir('src/log'):
    print("removing log path...")
    shutil.rmtree('src/log')

includes = [
            'enzyme',
            ]

excludes = [
            'email',
            'unittest',
            '_hashlib',
            '_ssl',
            '_sqlite3',
            'sqlite3',
            'sqlobject',
            'bz2',
            'select',
            '_codecs_cn',
            '_codecs_hk',
            '_codecs_iso2022',
            '_codecs_jp',
            '_codecs_kr',
            '_codecs_tw',
            '_ctypes',
            '_heapq',
            'sqlalchemy.cprocessors',
            'sqlalchemy.cresultproxy',
            'PyQt4._qt',
            '_json',
            '_multibytecodec',
            'termios'
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
                 "README.txt",
                 ]

exclude_files = [
                 "QtNetwork4.dll",
                 "QtWebKit4.dll",
                 "libphonon.so.4",
                 "libQtDBus.so.4",
                 "libQtDeclarative.so.4",
                 "libQtMultimedia.so.4",
                 "libQtScript.so.4",
                 "libQtScriptTools.so.4",
                 "libQtSql.so.4",
                 "libQtSvg.so.4",
                 "libQtTest.so.4",
                 "libQtWebKit.so.4",
                 "libQtNetwork.so.4",
                 "libQtXml.so.4",
                 "libQtXml.so.4",
                 "libQtXmlPatterns.so.4",
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
                                  "bin_excludes": exclude_files,
                                  "optimize": 2,
                                  "compressed": True, # Compress library.zip
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

shutil.rmtree(glob("build/exe*")[0] + '/PyQt4.uic.widget-plugins')

archive_name = "dist/{0}-{1}-{2}" \
    .format(utils.PROGRAM_NAME, utils.PROGRAM_VERSION, platform.system())
archive_file_name = glob("{0}*".format(archive_name))[0]
if os.path.isfile(archive_file_name):
    print("remove previously created archive")
    os.remove(archive_file_name)
root_dir = glob("build/exe*")[0]
print("create " + archive_format + " " + archive_name)
shutil.make_archive(archive_name, archive_format, root_dir)

print("END")


