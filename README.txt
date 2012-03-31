
License: GNU General Public License version 3 (GPLv3)

Libraries:
    Python 2.7
    PyQt 4.8 (http://www.riverbankcomputing.co.uk/software/pyqt/download)
    lxml 2.3 (http://pypi.python.org/pypi/lxml/2.3.3)
    IMDbPY 4.8 (http://imdbpy.sourceforge.net/)
    enzyme 0.1 (https://github.com/Diaoul/enzyme)
    cx_Freeze 4.2

IDE: Eclipse 3.7

Programming notes:

	lxml
	    libxml2-dev
	    libxslt-dev
	    
	IMDbPY 
		[under Windows] install first lxml (http://pypi.python.org/pypi/lxml/)
        python setup.py --without-cutils install
        
    Packaging:
	    cx_Freeze 4.2
	    python-dev [under Linux]
	    libssl-dev [under Linux]
	    
		setup.py bdist_dumb