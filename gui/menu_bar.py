from configparser import ConfigParser
from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QApplication, QSpacerItem, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QPoint

from .location_menu import LocationMenu, AddLoationBt

class MenuBar(QWidget):
    def __init__(self, mainWindow: QMainWindow, settings: ConfigParser):
        super().__init__(mainWindow)

        HEIGHT, WIDTH = 50, 50
        self.setFixedHeight(HEIGHT)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(10,0,0,0)

        #region logo
        logoLb = QLabel(self)
        logoPm = QPixmap(r"gui\resources\QttieSkiesLogo.png")
        logoLb.setPixmap(logoPm.scaledToHeight(HEIGHT))
        layout.addWidget(logoLb)
        #endregion logo
        
        #region location widgets
        layout.addWidget(LocationMenu(self, settings))
        layout.addWidget(AddLoationBt(self, settings))
        #endregion location widgets

        layout.addSpacerItem(QSpacerItem(0,0, QSizePolicy.Policy.Expanding))

        #region buttons
        minimizeBt = QPushButton("_", self)
        minimizeBt.clicked.connect(mainWindow.showMinimized)
        layout.addWidget(minimizeBt)

        maximizeBt = QPushButton("□", self)
        maximizeBt.clicked.connect(mainWindow.showMaximized)
        layout.addWidget(maximizeBt)

        closeBt = QPushButton("X", self)
        closeBt.setObjectName("CloseButton")
        closeBt.clicked.connect(QApplication.quit)
        layout.addWidget(closeBt)

        for button in (minimizeBt, maximizeBt, closeBt):
            button.setFixedSize(WIDTH,HEIGHT)
        #endregion buttons
            
        
    #TODO implement the ability to move and resize the window
    # def mousePressEvent(self, event: QMouseEvent):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self.oldPos = event.globalPosition().toPoint()


    # def mouseReleaseEvent(self, event: QMouseEvent):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self.oldPos = None

    # def mouseMoveEvent(self, event: QMouseEvent):
    #     if self.oldPos is not None:
    #         delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
    #         self.parent().move(self.pos() + delta)
    #         self.oldPos = event.globalPosition().toPoint()

    # def maximizeButton(self):
    #     if self.parent().isMaximized():
    #         self.parent().resize(int(self.screen().size().height()/2), int(self.screen().size().width()/2))


