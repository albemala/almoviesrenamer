from PyQt5.QtCore import QObject, pyqtProperty


class MovieTableItem(QObject):
    def __init__(self, original_name, new_name, parent=None):
        super().__init__(parent)
        self.__original_name = original_name
        self.__new_name = new_name

    @pyqtProperty('QString', constant=True)
    def original_name(self):
        return self.__original_name

    @original_name.setter
    def original_name(self, original_name):
        self.__original_name = original_name

    @pyqtProperty('QString', constant=True)
    def new_name(self):
        return self.__new_name

    @new_name.setter
    def new_name(self, new_name):
        self.__new_name = new_name