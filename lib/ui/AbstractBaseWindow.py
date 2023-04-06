from abc import abstractmethod, ABC, ABCMeta
from typing import TypeVar, Generic

from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow

from lib.Config import Config
from lib.Logger import Logger


class QMainWindowABCMeta(ABCMeta, type(QMainWindow)):
    pass


Ui_Class = TypeVar('Ui_Class')


class AbstractBaseWindow(Generic[Ui_Class], QMainWindow, ABC, metaclass=QMainWindowABCMeta):

    def __init__(self, config: Config, logger: Logger):
        QMainWindow.__init__(self)
        self.__config: Config = config
        self.__logger: Logger = logger
        self.__class_name: str = self.__class__.__name__
        self.__settings: QSettings = QSettings("the_window_settings", self.__config.app_name)
        self.__ui: Ui_Class = self._get_ui()()  # create inst of ui class
        self.__init_ui()

    @abstractmethod
    def _init_ui(self) -> None:
        pass

    @abstractmethod
    def _get_ui(self) -> Ui_Class:
        pass

    @property
    def _ui(self) -> Ui_Class:
        return self.__ui

    @property
    def _config(self) -> Config:
        return self.__config

    @property
    def _logger(self) -> Logger:
        return self.__logger

    def closeEvent(self, event: QCloseEvent):
        self.__save()

    def __init_ui(self):
        self.__ui.setupUi(self)
        self.setWindowTitle(f'{self.__config.app_name} {self.__config.version}')
        self.setWindowIcon(QIcon(self.__config.icon_path))
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.__restore()
        if self.__config.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self._init_ui()

    def __restore(self):
        geometry = self.__settings.value(f"{self.__class_name}/Geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = self.__settings.value(f"{self.__class_name}/State")
        if state:
            self.restoreState(state)

    def __save(self):
        self.__settings.setValue(f"{self.__class_name}/Geometry", self.saveGeometry())
        self.__settings.setValue(f"{self.__class_name}/State", self.saveState())
