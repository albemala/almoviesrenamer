from PyQt5.QtCore import QObject, pyqtProperty


class RulesListItem(QObject):
    def __init__(self, rule, parent=None):
        super().__init__(parent)
        self.__rule = rule

    @pyqtProperty('QString', constant=True)
    def rule(self):
        return self.__rule

    @rule.setter
    def rule(self, rule):
        self.__rule = rule
