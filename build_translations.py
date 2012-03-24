# -*- coding: latin-1 -*-

__author__ = "Alberto Malagoli"

import platform
import subprocess
from glob import glob
import os
import shutil

pylupdate4 = ''
lrelease = ''

os = platform.system()
if os == 'Windows':
    import os.path
    import PyQt4
    pylupdate4 = os.path.join(PyQt4.__path__[0], 'pylupdate4.exe')
    lrelease = os.path.join(PyQt4.__path__[0], 'lrelease.exe')
elif os == 'Linux':
    pylupdate4 = 'pylupdate4'
    lrelease = 'lrelease'

subprocess.call([pylupdate4, 'src/translations.pro'], shell = True)
subprocess.call([lrelease, 'src/translations.pro'], shell = True)

for qm_file in glob('src/qm/*'):
    os.remove(qm_file)

for qm_file in glob('src/*.qm'):
    shutil.move(qm_file, 'src/qm')
