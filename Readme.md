# About

ALMoviesRenamer cares about automatically rename your movie files, searching for information on the web.

You will have video file names like this:

_A.Really.Cool.Movie.2008.ENG.XviD-Republic.CD1_

renamed into this:

_A really cool movie (2008, A. Director, 90') CD1_

Of course, you decide the rename pattern.

# How to use

Once selected the movies you want to rename, the program will automatically search the web for information like movie titles, year, directors. Than you have to choose the renaming rules, and that's it!

# Development

ALMoviesRenamer is programmed in Python, using [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) 
as GUI support, and [IMDbPY](http://imdbpy.sourceforge.net/) to get movies information.

## Libraries

-  Python 2.7
-  PyQt 4.9 - http://www.riverbankcomputing.co.uk/software/pyqt/download
-  lxml 2.3 - http://pypi.python.org/pypi/lxml/2.3.3
-  IMDbPY 4.8 - http://imdbpy.sourceforge.net/
-  enzyme 0.2 - https://github.com/Diaoul/enzyme
-  cx_Freeze 4.2 - http://cx-freeze.sourceforge.net/

## License

GNU General Public License version 3 (GPLv3)
