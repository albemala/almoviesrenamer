# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

import sys
import os.path
import subprocess

python = sys.executable
subprocess.call([sys.executable, 'setup.py', 'bdist_dumb'], shell = True)
