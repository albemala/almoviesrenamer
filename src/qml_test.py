import sys

from PyQt5.QtCore import QObject, pyqtProperty
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine


class DataObject(QObject):
    def __init__(self, original_name, new_name, parent=None):
        super().__init__(parent)
        self.__original_name = original_name
        self.__new_name = new_name

    @pyqtProperty('QString')
    def original_name(self):
        return self.__original_name

    @original_name.setter
    def original_name(self, original_name):
        self.__original_name = original_name

    @pyqtProperty('QString')
    def new_name(self):
        return self.__new_name

    @new_name.setter
    def new_name(self, new_name):
        self.__new_name = new_name


app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()

# dataList = [
#     DataObject("Item 1", "red"),
#     DataObject("Item 2", "green"),
#     DataObject("Item 3", "blue"),
#     DataObject("Item 4", "yellow")
# ]
# engine.rootContext().setContextProperty("mymodel", dataList)

engine.load("ui.qml")

window = engine.rootObjects()[0]
window.setProperty("fileName", "prova")
# window.property("moviesModel")

sys.exit(app.exec_())
