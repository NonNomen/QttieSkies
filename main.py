import sys
from configparser import ConfigParser
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from gui.main_window import MainWindow

if __name__ == "__main__":
    settings = ConfigParser()
    app = QApplication(sys.argv)

    settings.read(r"settings.ini")

    with open(r"gui\styles\dark_styles.qss") as f:
        app.setStyleSheet(f.read())

    mainWindow = MainWindow(settings)
    mainWindow.showMaximized()

    sys.exit(app.exec())