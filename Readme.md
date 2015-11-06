## Important
This program makes an extensive use of [The IMDb API](http://www.imdbapi.com/), which are free, 
but the infrastructure who runs it is not. 
By now, the creator of The IMDb API uses his money to let us rename our movies, 
for free, so please consider donating on his site, The IMDb API.

## About
ALmoviesRenamer cares about automatically rename your movie files, searching for information on the web.

You will have video file names like this:

_A.Really.Cool.Movie.2008.ENG.XviD-Republic.CD1_

renamed into this:

_A really cool movie (2008, A. Director, 90') CD1_

Of course, you decide the rename pattern.

#### Last version: 4

A shiny new version, faster than ever, smarter than ever! 
The IMDb API is now used to retrieve movies information,
which is really fast. Some corrections on movie titles 
detection has been made too, giving a better renaming experience. 
Even the generation of new file name has been improved, 
removing known problems.

- CHG: new algorithm for generating new file name
- ADD: double clicking on a movie opens file manager in containing folder
- ADD: right click on a movie to open containing folder or copy file name
- CHG: now www.imdbapi.com is used to retrieve correct movie from guessed title. this speeds up movies info retrieving time, and information correctness
- CHG: better organization of attributes on renaming rule dialog
- FIX: language detection corrections under Linux


## How to use

Once selected the movies you want to rename, the program will automatically search the web for information like movie titles, year, directors. Than you have to choose the renaming rules, and that's it!

## Development

AlMoviesRenamer? is programmed in Python, using [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) 
as GUI support, and [IMDbPY](http://imdbpy.sourceforge.net/) to get movies information.
