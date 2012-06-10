
License: GNU General Public License version 3 (GPLv3)

IDE: Eclipse 3.7

Libraries:
    Python 2.7
    PyQt 4.9 - http://www.riverbankcomputing.co.uk/software/pyqt/download
    lxml 2.3 - http://pypi.python.org/pypi/lxml/2.3.3
    IMDbPY 4.8 - http://imdbpy.sourceforge.net/
    enzyme 0.2 - https://github.com/Diaoul/enzyme
    cx_Freeze 4.2 - http://cx-freeze.sourceforge.net/
    
Docs:
	cx_Freeze - http://cx_freeze.readthedocs.org/en/latest/index.html

Programming notes:

	lxml
	    libxml2-dev
	    libxslt-dev
	    
	IMDbPY 
		install lxml first 
        [under Windows] python setup.py --without-cutils install
        
    Packaging:
	    cx_Freeze 4.2
	    python-dev [under Linux]
	    libssl-dev [under Linux]
	    