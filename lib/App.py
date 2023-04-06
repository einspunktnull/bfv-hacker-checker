import sys
from time import sleep
from typing import Any, Dict, Optional

import qdarktheme
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QApplication
from injector import singleton

from lib.Config import Config
from lib.GlobalInjector import GlobalInjector
from lib.Logger import Logger
from lib.common import NoPlayernameFoundException
from lib.thread.DetectPlayerNameThread import DetectPlayerNameThread
from lib.thread.PrepareThread import PrepareThread
from lib.thread.UserInputListenerThread import UserInputListenerThread
from lib.ui.AppWindow import AppWindow
from lib.ui.DebugWindow import DebugWindow


class App(QObject):
    def __init__(self):
        super().__init__()

        self.__config: Config = GlobalInjector.get(Config)
        self.__logger: Logger = GlobalInjector.get(Logger)

        if self.__config.theme != 'none':
            qdarktheme.enable_hi_dpi()

        self.__qapp: QApplication = QApplication(sys.argv)

        if self.__config.theme != 'none':
            qdarktheme.setup_theme(self.__config.theme)

        GlobalInjector.bind(AppWindow, to=AppWindow, scope=singleton)
        GlobalInjector.bind(DebugWindow, to=DebugWindow, scope=singleton)

        self.__app_window: AppWindow = GlobalInjector.get(AppWindow)
        self.__app_window.show()

        self.__debug_window: DebugWindow = GlobalInjector.get(DebugWindow)

        self.__prep_thread: PrepareThread = PrepareThread(
            self.__config,
            self.__on_prepare_thread_progress,
            self.__on_prepare_thread_success,
            self.__on_thread_exception
        )
        self.__listener_thread: UserInputListenerThread = UserInputListenerThread(
            self.__config.hotkey,
            self.__on_listener_thread_event
        )

        self.__detect_thread: Optional[DetectPlayerNameThread] = None

    def run(self) -> int:
        self.__prep_thread.start()
        return self.__qapp.exec_()

    def __on_prepare_thread_progress(self, msg: str):
        self.__app_window.show_status_message(msg)

    def __on_prepare_thread_success(self):
        self.__app_window.enable_web_view()
        self.__check_playername(self.__config.default_playername)
        self.__listener_thread.start()

    def __on_listener_thread_event(self, mouse_x: int, mouse_y: int) -> None:
        if self.__detect_thread is None:
            self.__detect_thread = DetectPlayerNameThread(
                self.__on_detect_thread_success,
                self.__on_thread_exception,
                self.__config.poi_width,
                self.__config.poi_height,
                mouse_x,
                mouse_y,
                self.__config.data_dir if self.__config.debug else None
            )
            self.__app_window.show_status_message('try to detect playername')
            self.__detect_thread.start()

    def __on_detect_thread_success(self, player_name: str):
        self.__app_window.show_status_message(f'detected playername: {player_name}')
        self.__check_playername(player_name)

    @pyqtSlot(Exception)
    def __on_thread_exception(self, exception: Exception) -> Any:
        try:
            raise exception
        except NoPlayernameFoundException as ex:
            self.__app_window.show_status_message(ex.message)
            self.__logger.warning(ex.args[0])
        except Exception as ex:
            self.__logger.exception(ex)
            self.__app_window.show_exception(exception)
            self.__qapp.exit(1)
        self.__detect_thread = None

    def __check_playername(self, player_name: str):
        self.__app_window.show_status_message(f'request hacker lookup for: {player_name}')
        query_params: Dict[str, Any] = {'name': player_name}
        self.__app_window.call_url(self.__config.url, query_params)
        if self.__detect_thread is not None:
            sleep(1)
            self.__detect_thread = None
