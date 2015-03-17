**It is with my great sorrow that I have to declare this project as discontinued. Unfortunately I have no more time to keep it growing, nor to support it, due to some recent changes in my life. On Mercurial repository there are still some new changes made to the code after release 4, and prepared for a 5th release, but I cannot do a new release by now...**

**Of course, everything is open, and everyone is free to contribute on it, make changes, copy the code and start a new project, or something else!**

**I hope this program helped some of you in some way. Don't forget that every piece of code has been thought, written and tested with love, thinking about you, dear user, to make you have the best experience ever on renaming a file.**

_Take care :)_


---


# Important #

_This program makes an extensive use of [The IMDb API](http://www.imdbapi.com/), which are free, but the infrastructure who runs it is not. By now, the creator of [The IMDb API](http://www.imdbapi.com/) uses his money to let us rename our movies, for free, so please consider donating on his site, [The IMDb API](http://www.imdbapi.com/)._

# About #

ALmoviesRenamer cares about automatically rename your movie files, searching for information on the web.

You will have video file names like this:

_A.Really.Cool.Movie.2008.ENG.XviD-Republic.CD1_

renamed into this:

_A really cool movie (2008, A. Director, 90') CD1_

Of course, you decide the rename pattern.

![https://lh3.googleusercontent.com/-EE5hKACQvW8/T5m-AGrBYUI/AAAAAAAAA0s/wR6JKUKhddA/s0/Immagine%205.png](https://lh3.googleusercontent.com/-EE5hKACQvW8/T5m-AGrBYUI/AAAAAAAAA0s/wR6JKUKhddA/s0/Immagine%205.png)

![https://lh3.googleusercontent.com/-BQ2IUZUbl6Q/T5m-D8CCYtI/AAAAAAAAA00/gqeNHOR8SkI/s512/Immagine%25206.png](https://lh3.googleusercontent.com/-BQ2IUZUbl6Q/T5m-D8CCYtI/AAAAAAAAA00/gqeNHOR8SkI/s512/Immagine%25206.png)

![https://lh5.googleusercontent.com/-nqv6ZqENRk0/T5m-EmZNVEI/AAAAAAAAA08/xq7sIAhvN2k/s380/Immagine%25207.png](https://lh5.googleusercontent.com/-nqv6ZqENRk0/T5m-EmZNVEI/AAAAAAAAA08/xq7sIAhvN2k/s380/Immagine%25207.png)

### Last version ###

A shiny new version, faster than ever, smarter than ever!
[The IMDb API](http://www.imdbapi.com/) is now used to retrieve movies information, which is really fast. Some corrections on movie titles detection has been made too, giving a better renaming experience.
Even the generation of new file name has been improved, removing known problems.

**4**

  * CHG: new algorithm for generating new file name
  * ADD: double clicking on a movie opens file manager in containing folder
  * ADD: right click on a movie to open containing folder or copy file name
  * CHG: now www.imdbapi.com is used to retrieve correct movie from guessed title. this speeds up movies info retrieving time, and information correctness
  * CHG: better organization of attributes on renaming rule dialog
  * FIX: language detection corrections under Linux

# How to use #

Once selected the movies you want to rename, the program will automatically search the web for information like movie titles, year, directors. Than you have to choose the renaming rules, and that's it!

# Development #

AlMoviesRenamer is programmed in Python, using [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro) as GUI support, and [IMDbPY](http://imdbpy.sourceforge.net/) to get movies information.

### We're hiring :) ###

I'm looking for someone who helps me in:
  * translations
  * testing
  * packaging (using cx\_Freeze)
  * develop the application!

# Polls #

Please answer a few questions about your satisfaction with ALmoviesRenamer:
https://docs.google.com/spreadsheet/gform?key=0Au2mzMTLeYCydHJRb3BBb21rdHZ3eV9pSnVKWTV3b1E&hl=it#edit