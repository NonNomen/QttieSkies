from PyQt6.QtWidgets import QComboBox, QWidget, QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon
from configparser import ConfigParser

class LocationMenu(QComboBox):
    def __init__(self, parent: QWidget, setting: ConfigParser):
        super().__init__(parent)

        self.addItems(["Ballwin , MO", "Chesterfield, MO"])

class AddLoationBt(QPushButton):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setIcon(QIcon(r"gui\resources\plus_light.png"))
        self.setFixedSize(self.parentWidget().height(), self.parentWidget().height())