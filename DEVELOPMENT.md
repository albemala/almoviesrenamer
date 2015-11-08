Reference guide to set up development environment.

# Requirements

- [Python 3.5](https://www.python.org/downloads/)
- [Qt 5.5](http://www.qt.io/) (required only if compiling from source)
- [SIP 4.17](https://www.riverbankcomputing.com/software/sip/download) (from source)
- [PyQt5 5.5](https://www.riverbankcomputing.com/software/pyqt/download5) (from source)
- [TMDBsimple 1.x](https://github.com/celiao/tmdbsimple/)
- [guessit 1.x](https://github.com/wackou/guessit)

# Mac OS X

## Install modules and tools

- install [Brew](http://brew.sh/):

`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

- install PyQt5 (this will also install Python 3.5 and SIP, if necessary):

`brew install pyqt5`

- install TMDBsimple

`pip3 install tmdbsimple`

- install guessit

`pip3 install guessit`

## Setup PyCharm

- Settings > Project Interpreter > Add local...
- Select Python interpreter from:

`/usr/local/Cellar/python3/3.5.0/Frameworks/Python.framework/Versions/3.5/bin/python3.5`


