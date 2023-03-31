from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("My Window")
        self.setGeometry(100, 100, 640, 480)

        # Load the saved window position and size from the settings
        settings = QSettings("MyCompany", "MyApp")
        self.restoreGeometry(settings.value("MainWindow/Geometry"))
        self.restoreState(settings.value("MainWindow/State"))




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("My Window")
        self.setGeometry(100, 100, 640, 480)

        # Load the saved window position and size from the settings
        settings = QSettings("MyCompany", "MyApp")
        self.restoreGeometry(settings.value("MainWindow/Geometry"))
        self.restoreState(settings.value("MainWindow/State"))

    def closeEvent(self, event):
        # Save the current window position and size to the settings
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())

    def closeEvent(self, event):
        # Save the current window position and size to the settings
        settings = QSettings("MyCompany", "MyApp")
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())


