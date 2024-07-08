from configparser import ConfigParser
from PyQt6.QtWidgets import QMainWindow, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from .menu_bar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self, settings: ConfigParser):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Qttie Skies")
        logoIco = QIcon("gui/resources/weatherlogo.ico")
        self.setWindowIcon(logoIco)
        self.setWindowIconText("Qttie Skies logo")

        self.setMenuWidget(MenuBar(self, settings))