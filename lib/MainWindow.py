import os
import sys
from typing import Dict, Any

from PyQt5.QtCore import QUrl, QUrlQuery, QSettings, Qt, QSysInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow
from injector import inject

from lib.AboutDialog import AboutDialog
from lib.Config import Config
from lib.GlobalInjector import GlobalInjector
from lib.Logger import Logger
from lib.Ui_MainWindow import Ui_MainWindow
from lib.common import OS_PLATFORM_LINUX


class MainWindow(QMainWindow):
    @inject
    def __init__(self, config: Config, logger: Logger):
        super().__init__()
        self.__config: Config = config
        self.__logger: Logger = logger
        self.__settings: QSettings = QSettings("main_window_settings", self.__config.app_name)
        GlobalInjector.bind(AboutDialog, to=AboutDialog)
        self.__ui: Ui_MainWindow = Ui_MainWindow()
        if sys.platform == OS_PLATFORM_LINUX:
            prod_type = QSysInfo.productType()
            if prod_type == "arch" or prod_type == "manjaro":
                os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"
                print("Info: QtWebEngine sandbox disabled")
        self.__web_View: QWebEngineView = QWebEngineView()
        self.__init_ui()

    def __init_ui(self):
        self.__ui.setupUi(self)
        self.setWindowTitle(f'{self.__config.app_name} {self.__config.version}')
        self.setWindowIcon(QIcon(self.__config.icon_path))
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        # self.__web_View.show()
        # self.__ui.verticalLayout.addWidget(self.__web_View)
        self.__restore()
        if self.__config.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.__ui.actionAbout.triggered.connect(self.__on_about_click)

    def enable_web_view(self) -> None:
        self.__web_View.show()
        self.__ui.verticalLayout.addWidget(self.__web_View)

    def closeEvent(self, event):
        self.__save()

    def call_url(self, url: str, query_params: Dict[str, Any] = None):
        if query_params is None:
            query_params = {}
        url_: QUrl = QUrl(url)
        query = QUrlQuery()
        for key, value in query_params.items():
            query.addQueryItem(key, value)
        url_.setQuery(query)
        self.__web_View.load(url_)

    def show_message(self, msg: str):
        print("MainWindow.show_message()", msg)

    def show_exception(self, exception: Exception):
        print("MainWindow.show_exception()", str(exception))

    def __on_about_click(self):
        self.__logger.debug('MainWindow.__on_about_click')
        dlg: AboutDialog = GlobalInjector.get(AboutDialog)
        dlg.exec_()

    def __restore(self):
        geometry = self.__settings.value("MainWindow/Geometry")
        if geometry:
            self.restoreGeometry(geometry)
        state = self.__settings.value("MainWindow/State")
        if state:
            self.restoreState(state)

    def __save(self):
        self.__settings.setValue("MainWindow/Geometry", self.saveGeometry())
        self.__settings.setValue("MainWindow/State", self.saveState())
