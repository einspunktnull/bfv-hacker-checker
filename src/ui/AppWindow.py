import os
import sys
from typing import Type

from PyQt5.QtCore import QUrl, QUrlQuery, QSysInfo, pyqtSlot
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from injector import inject

from service.ConfigService import ConfigService
from service.LoggingService import LoggingService
from base.common import OS_PLATFORM_LINUX, get_monospace_font, NoPlayernameFoundException
from service.PrepareService import PrepareService
from ui.AbstractBaseWindow import AbstractBaseWindow
from service.DetectPlayerNameService import DetectPlayerNameService
from ui.AboutDialog import AboutDialog
from ui.DebugWindow import DebugWindow
from ui_generated.Ui_AppWindow import Ui_AppWindow


class AppWindow(AbstractBaseWindow[Ui_AppWindow]):

    @inject
    def __init__(
            self,
            config: ConfigService,
            logger: LoggingService,
            detect_player_name_service: DetectPlayerNameService,
            prepare_service: PrepareService,
            debug_window: DebugWindow,
            about_dialog: AboutDialog
    ):
        self.__detect_player_name_service: DetectPlayerNameService = detect_player_name_service
        self.__prepare_service: PrepareService = prepare_service
        self.__web_View: QWebEngineView = QWebEngineView()
        self.__debug_window: DebugWindow = debug_window
        self.__about_dialog: AboutDialog = about_dialog
        super().__init__(config, logger)

    def _post_init(self):
        if sys.platform == OS_PLATFORM_LINUX:
            prod_type = QSysInfo.productType()
            if prod_type == "arch" or prod_type == "manjaro":
                os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"
                self._logger.info("QtWebEngine sandbox disabled")
        self._ui.label_init.setFont(get_monospace_font())
        if self._config.debug:
            self.__debug_window.signal_close.connect(self.__on_child_window_closed)
            self._ui.actionShow_Debugging_Window.triggered.connect(self.__toggle_debug_window)
            self.__show_debug_window()
        else:
            self._ui.menuHelp.removeAction(self._ui.actionShow_Debugging_Window)
        self._ui.actionAbout.triggered.connect(self.__on_about_click)
        self.__detect_player_name_service.signal_detection_result.connect(self.__on_playername_detected)
        self.__detect_player_name_service.signal_exception.connect(self.__on_exception)
        self.__prepare_service.signal_status.connect(self.__on_prep_status)
        self.__prepare_service.signal_exception.connect(self.__on_exception)

    def _get_ui(self) -> Type[Ui_AppWindow]:
        return Ui_AppWindow

    def closeEvent(self, event: QCloseEvent):
        self.__close_debug_window()
        super().closeEvent(event)

    def check_playername(self, player_name: str):
        self.show_status_message(f'request hacker lookup for: {player_name}')
        url: QUrl = QUrl(self._config.url)
        query = QUrlQuery()
        query.addQueryItem('name', player_name)
        url.setQuery(query)
        self.__web_View.load(url)

    def enable_web_view(self) -> None:
        self.__web_View.show()
        self._ui.verticalLayout.removeWidget(self._ui.label_init)
        self._ui.verticalLayout.addWidget(self.__web_View)

    def show_status_message(self, msg: str):
        self.statusBar().showMessage(msg)

    @pyqtSlot(str)
    def __on_playername_detected(self, player_name: str) -> None:
        self.check_playername(player_name)

    @pyqtSlot(str)
    def __on_prep_status(self, message: str) -> None:
        self.show_status_message(message)

    @pyqtSlot(Exception)
    def __on_exception(self, exception: Exception) -> None:
        if isinstance(exception, NoPlayernameFoundException):
            self.show_status_message(exception.message)

    def __on_about_click(self):
        self._logger.debug('AppWindow.__on_about_click')
        self.__about_dialog.exec_()

    @pyqtSlot()
    def __on_child_window_closed(self):
        if self._config.debug:
            self._ui.actionShow_Debugging_Window.setChecked(False)

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
