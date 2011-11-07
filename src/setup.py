# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

buildOptions = dict(
	include_files = [
                     "icons",
                     "main_window.ui",
                     "renaming_rule_dialog.ui",
                     "settings.ini",
                     "app_de.qm",
                     "app_es.qm",
                     "app_fr.qm",
                     "app_it.qm"
                     ],
	compressed = True,
	optimize = 2,
)

setup(
    name = "ALmoviesRenamer",
    version = "2.0",
	options = dict(build_exe = buildOptions),
    executables = [Executable("main.py", base = base)]
)

