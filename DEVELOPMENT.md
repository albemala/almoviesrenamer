# Mac OS X

- install [Python 3.5](https://www.python.org/downloads/)
- install [Qt 5.5](http://www.qt.io/)
- install [SIP 4.17](https://www.riverbankcomputing.com/software/sip/download) (from source)
- install [PyQt5 5.5](https://www.riverbankcomputing.com/software/pyqt/download5) (from source)
- install [TMDBsimple 1.x](https://github.com/celiao/tmdbsimple/)
- install [guessit 1.x](https://github.com/wackou/guessit)

## SIP

- `python3 configure.py`
- `make`
- `sudo make install`

## PyQt5

- `python3 configure.py --qmake ~/Qt/5.5/clang_64/bin/qmake --sip /Library/Frameworks/Python.framework/Versions/3.5/bin/sip`
- `make`
- `sudo make install`

## TMDBsimple

- `pip3 install tmdbsimple`

## guessit

- `pip3 install guessit`
