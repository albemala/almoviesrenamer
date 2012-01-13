#!/usr/bin/env python
# -*- coding: utf-8 -*-
# enzyme - Video metadata parser
# Copyright (c) 2011 Antoine Bertin <diaoulael@gmail.com>
#
# This file is part of enzyme.
#
# enzyme is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# enzyme is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from enzyme import infos
from setuptools import setup

setup(name=infos.__title__,
    version=infos.__version__,
    license=infos.__license__,
    description=infos.__description__,
    long_description=open('README').read() + '\n\n' +
                     open('NEWS').read(),
    classifiers=['Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Video'],
    keywords='video parse metadata library',
    author=infos.__author__,
    author_email=infos.__email__,
    url='https://github.com/Diaoul/enzyme',
    packages=['enzyme'])
