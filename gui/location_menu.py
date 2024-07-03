from geonamescache import GeonamesCache
from PyQt6.QtWidgets import QComboBox, QWidget, QPushButton, QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QListWidget
from PyQt6.QtCore import QEvent, Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QIcon, QKeyEvent
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

        self.clicked.connect(self.addCityDialog)

    def addCityDialog(self):
        dialog = AddLocationDialog(self)
        if dialog.exec():
            print("city add")
        else:
            print("failed")


class AddLocationDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setWindowTitle("Add Location")

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        buttonBox = QDialogButtonBox(buttons, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.citySearch = CitySearch(self)
        cityList = CityList(self)
        layout = QVBoxLayout(self)

        self.citySearch.searchUpdated.connect(cityList.updateList)

        layout.addWidget(self.citySearch)
        layout.addWidget(cityList)
        layout.addWidget(buttonBox)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if isinstance(self.focusWidget(), QLineEdit):
                    self.citySearch.keyPressEvent(event)
                    return True
        return super().eventFilter(obj, event)




class CitySearch(QLineEdit):
    searchUpdated: pyqtSignal = pyqtSignal(list)
    def __init__(self, parent):
        super().__init__(parent)
        self.geoCache = GeonamesCache()
        self.setPlaceholderText("Enter a city name: ")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.searchUpdated.emit(self.geoCache.search_cities(self.text()))
        else:
            super().keyPressEvent(event)
    

class CityList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)


    @pyqtSlot(list)
    def updateList(self, geoCache: list[dict] | list):
        self.clear()
        [self.addItem(f"{city['name']}, {city['admin1code']}") if city["countrycode"] == "US" 
         else self.addItem(f"{city['name']}, {city['countrycode']}")
         for city in geoCache]

