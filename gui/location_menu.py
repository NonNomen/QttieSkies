from geonamescache import GeonamesCache
from PyQt6.QtWidgets import QComboBox, QWidget, QPushButton, QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
from PyQt6.QtCore import QEvent, Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QIcon, QKeyEvent
from configparser import ConfigParser

class LocationMenu(QComboBox):
    def __init__(self, parent: QWidget, settings: ConfigParser):
        super().__init__(parent)
        self.settings = settings
        self.addItems(self.settings["CityIds"])

    @pyqtSlot()
    def refresh(self):
        self.clear()
        self.addItems(self.settings["CityIds"])


class AddLoationBt(QPushButton):
    def __init__(self, parent: QWidget, settings: ConfigParser):
        super().__init__(parent)

        self.settings = settings
        self.dialog = AddLocationDialog(self, self.settings)
        self.setIcon(QIcon(r"gui\resources\plus_light.png"))
        self.setFixedSize(self.parentWidget().height(), self.parentWidget().height())

        self.clicked.connect(self.addCityDialog)

    def addCityDialog(self):
        if self.dialog.exec():
            print(f"add city")
        else:
            print("failed")


class AddLocationDialog(QDialog):
    def __init__(self, parent: QWidget, settings: ConfigParser):
        super().__init__(parent)
        self.setWindowTitle("Add Location")

        self.settings = settings

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        buttonBox = QDialogButtonBox(buttons, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.citySearch = CitySearch(self)
        self.cityList = CityList(self.citySearch)
        layout = QVBoxLayout(self)

        self.citySearch.searchUpdated.connect(self.cityList.updateList)

        layout.addWidget(self.citySearch)
        layout.addWidget(self.cityList)
        layout.addWidget(buttonBox)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if isinstance(self.focusWidget(), QLineEdit):
                    self.citySearch.keyPressEvent(event)
                    return True
        return super().eventFilter(obj, event)
    
    def accept(self):
        city:CityItem = self.cityList.selectedItems()[0]
        if not self.settings.has_section("CityIds"):
            self.settings.add_section("CityIds")
        self.settings["CityIds"][city.name] = f"{city.id}"
        with open("settings.ini", "w") as settingFile:
            self.settings.write(settingFile)
        super().accept()


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
    

class CityItem(QListWidgetItem):
    def __init__(self, name, id, region):
        self.name = name
        self.id = id
        super().__init__(f"{self.name}, {region}")


class CityList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)


    @pyqtSlot(list)
    def updateList(self, geoCache: list[dict] | list):
        self.clear()
        for city in geoCache:
            if city["countrycode"] == "US":
                listItem = CityItem(city['name'], city['geonameid'], city['countrycode'])
            else:
                listItem = CityItem(city['name'], city['geonameid'], city['admin1code'])
            self.addItem(listItem)


