import os
import sys
from typing import Dict, Any, Type

from PyQt5.QtCore import QUrl, QUrlQuery, QSysInfo
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from injector import inject

from lib.Config import Config
from lib.GlobalInjector import GlobalInjector
from lib.Logger import Logger
from lib.common import OS_PLATFORM_LINUX
from lib.ui.AboutDialog import AboutDialog
from lib.ui.AbstractBaseWindow import AbstractBaseWindow, Ui_Class
from lib.ui.DebugWindow import DebugWindow
from lib.ui.ExceptionDialog import ExceptionDialog
from lib.ui_generated.Ui_AppWindow import Ui_AppWindow


class AppWindow(AbstractBaseWindow[Ui_AppWindow]):
    @inject
    def __init__(self, config: Config, logger: Logger):
        GlobalInjector.bind(AboutDialog, to=AboutDialog)
        if sys.platform == OS_PLATFORM_LINUX:
            prod_type = QSysInfo.productType()
            if prod_type == "arch" or prod_type == "manjaro":
                os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"
                self.__logger.info("QtWebEngine sandbox disabled")
        self.__web_View: QWebEngineView = QWebEngineView()
        self.__debug_window: DebugWindow = GlobalInjector.get(DebugWindow)
        super().__init__(config, logger)

    def closeEvent(self, event: QCloseEvent):
        self.__close_debug_window()
        super().closeEvent(event)

    def _init_ui(self):
        if self._config.debug:
            self._ui.actionShow_Debugging_Window.triggered.connect(self.__toggle_debug_window)
            self.__show_debug_window()
        else:
            self._ui.menuHelp.removeAction(self._ui.actionShow_Debugging_Window)
        self._ui.actionAbout.triggered.connect(self.__on_about_click)

    def _get_ui(self) -> Type[Ui_AppWindow]:
        return Ui_AppWindow

    def call_url(self, url: str, query_params: Dict[str, Any] = None):
        if query_params is None:
            query_params = {}
        url_: QUrl = QUrl(url)
        query = QUrlQuery()
        for key, value in query_params.items():
            query.addQueryItem(key, value)
        url_.setQuery(query)
        self.__web_View.load(url_)

    def enable_web_view(self) -> None:
        self.__web_View.show()
        self._ui.verticalLayout.removeWidget(self._ui.label_init)
        self._ui.verticalLayout.addWidget(self.__web_View)

    def show_status_message(self, msg: str):
        self.statusBar().showMessage(msg)

    def show_exception(self, exception: Exception):
        exception_window = ExceptionDialog(exception)
        exception_window.exec_()

    def __on_about_click(self):
        self._logger.debug('AppWindow.__on_about_click')
        dlg: AboutDialog = GlobalInjector.get(AboutDialog)
        dlg.exec_()

    def __toggle_debug_window(self):
        if self.__debug_window.isVisible():
            self.__hide_debug_window()
        else:
            self.__show_debug_window()

    def __show_debug_window(self):
        self._logger.debug('AppWindow.__show_debug_window')
        self._ui.actionShow_Debugging_Window.setChecked(True)
        self.__debug_window.show()

    def __hide_debug_window(self):
        self._logger.debug('AppWindow.__hide_debug_window')
        self._ui.actionShow_Debugging_Window.setChecked(False)
        self.__debug_window.hide()

    def __close_debug_window(self):
        self._logger.debug('AppWindow.__close_debug_window')
        self.__debug_window.close()
