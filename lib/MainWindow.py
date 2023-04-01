from typing import Dict, Any

from PyQt5.QtCore import QUrl, QUrlQuery, QSettings, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QLabel, QMainWindow
from injector import inject

from lib.Config import Config
from lib.Logger import Logger


class MainWindow(QMainWindow):
    @inject
    def __init__(self, config: Config, logger: Logger):
        super().__init__()
        self.__config: Config = config
        self.__logger: Logger = logger
        self.__web_View: QWebEngineView = QWebEngineView()
        self.__msg_View: QLabel = QLabel()
        self.setWindowTitle(config.app_name)
        self.setWindowIcon(QIcon(config.icon_path))

        self.__settings: QSettings = QSettings("einspunktnull", config.app_name)
        geometry = self.__settings.value("MainWindow/Geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = self.__settings.value("MainWindow/State")
        if state:
            self.restoreState(state)

        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setCentralWidget(self.__web_View)

        if config.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def closeEvent(self, event):
        self.__logger.info('close event')
        self.__settings.setValue("MainWindow/Geometry", self.saveGeometry())
        self.__settings.setValue("MainWindow/State", self.saveState())

    def call_url(self, url: str, query_params: Dict[str, Any] = None):
        if query_params is None:
            query_params = {}
        url_: QUrl = QUrl(url)
        query = QUrlQuery()
        for key, value in query_params.items():
            query.addQueryItem(key, value)
        url_.setQuery(query)
        self.__logger.debug(f'call url {url_.url()}')
        self.__web_View.load(url_)

    def show_message(self, msg: str):
        self.__logger.debug('MainWindow.show_message()', msg)

    def show_exception(self, exception: Exception):
        self.__logger.debug('MainWindow.show_exception()', type(exception).__name__, str(exception))
