import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from movie_table_item import MovieTableItem

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()

dataList = [
    MovieTableItem("Item 1", "red"),
    MovieTableItem("Item 2", "green"),
    MovieTableItem("Item 3", "blue"),
    MovieTableItem("Item 4", "yellow")
]
engine.rootContext().setContextProperty("myModel", dataList)

engine.load("main_window.qml")

window = engine.rootObjects()[0]
window.setProperty("fileName", "prova")

sys.exit(app.exec_())
