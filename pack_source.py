# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

from PyQt4.QtCore import QSettings
from cx_Freeze import setup, Executable
from glob import glob
import os.path
import os
import shutil
import sys
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

if os.path.isdir('src/log'):
    shutil.rmtree('src/log')

if os.path.isdir('tmp'):
    print("remove previously created tmp folder")
    shutil.rmtree('tmp')
print("create tmp folder")
os.mkdir("tmp")
print("copying source files on it...")
shutil.copytree("src", "tmp/src")
shutil.copytree("libs", "tmp/libs")
for f in glob("*.py"):
    shutil.copy2(f, "tmp")
for f in glob("*.txt"):
    shutil.copy2(f, "tmp")
print("files copied")

archive_name = "dist/{0}-{1}-src" \
    .format(utils.PROGRAM_NAME, utils.PROGRAM_VERSION)
if os.path.isfile(archive_name):
    print("remove previously created archive")
    os.remove(archive_name)
root_dir = "tmp" #os.path.abspath("tmp")
print("create gztar " + archive_name)
#XXX c'è un problema qui, dentro l'archivio viene ricreato il path assoluto della cartella "tmp"
shutil.make_archive(archive_name, "gztar", root_dir = root_dir)
print("remove tmp folder")
shutil.rmtree("tmp")

print("END")


