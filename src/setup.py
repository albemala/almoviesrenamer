# -*- coding: latin-1 -*-
__author__ = "Alberto Malagoli"

from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

buildOptions = dict(
	include_files = ["icons", "blacklist", "main_window.ui"],
	compressed = True,
	optimize = 2,
)

setup(
        name = "AlMoviesRenamer",
        version = "1.1.0",
	options = dict(build_exe = buildOptions),
        executables = [Executable("main.py", base = base)]
)

