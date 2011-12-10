
License: GNU General Public License version 3 (GPLv3)

Libraries:
    Python 2.7
    PyQt 4.8 (http://www.riverbankcomputing.co.uk/software/pyqt/download)
    IMDbPY 4.8 (http://imdbpy.sourceforge.net/)
    guessit 0.2 (http://gitorious.org/smewt/guessit) (http://pypi.python.org/pypi/guessit/0.2)
    cx_Freeze 4.2

IDE: Eclipse 3.7

Programming notes:

	IMDbPY 
		[under Windows] install first lxml (http://pypi.python.org/pypi/lxml/)
        python setup.py --without-cutils install
        
    Packaging:
	    cx_Freeze 4.2
	    python-dev [under Linux]
	    libsssl-dev [under Linux]