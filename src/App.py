from typing import Any

from PyQt5.QtCore import pyqtSlot, QObject
from injector import inject

from QApplicationWrap import QApplicationWrap
from base.common import NoPlayernameFoundException
from service.ConfigService import ConfigService
from service.DetectPlayerNameService import DetectPlayerNameService
from service.LoggingService import LoggingService
from thread.PrepareThread import PrepareThread
from thread.UserInputListenerThread import UserInputListenerThread
from ui.AppWindow import AppWindow
from ui.DebugWindow import DebugWindow
from ui.ExceptionDialog import ExceptionDialog


class App(QObject):

    @inject
    def __init__(
            self,
            config: ConfigService,
            logger: LoggingService,
            qapp_wrap: QApplicationWrap,
            app_window: AppWindow,
            debug_window: DebugWindow,
            detect_player_name_service: DetectPlayerNameService
    ):
        super().__init__()

        self.__config: ConfigService = config
        self.__logger: LoggingService = logger
        self.__detect_player_name_service: DetectPlayerNameService = detect_player_name_service
        self.__qapp_wrap: QApplicationWrap = qapp_wrap
        self.__app_window: AppWindow = app_window
        self.__debug_window: DebugWindow = debug_window

        self.__prepare_thread: PrepareThread = PrepareThread(self, config, logger)
        self.__prepare_thread.signal_status.connect(self.__on_prepare_thread_progress)
        self.__prepare_thread.signal_finished.connect(self.__on_prepare_thread_success)
        self.__prepare_thread.signal_exception.connect(self.__on_exception)

        self.__listener_thread: UserInputListenerThread = UserInputListenerThread(self, config, logger)
        self.__listener_thread.signal_event.connect(self.__on_listener_thread_event)
        self.__listener_thread.signal_exception.connect(self.__on_exception)

        self.__detect_player_name_service.signal_exception.connect(self.__on_exception)

        self.__app_window.show()

    def run(self) -> int:
        self.__prepare_thread.start()
        return self.__qapp_wrap.exec_()

    @pyqtSlot(str)
    def __on_prepare_thread_progress(self, msg: str):
        self.__app_window.show_status_message(msg)

    @pyqtSlot()
    def __on_prepare_thread_success(self):
        self.__app_window.enable_web_view()
        self.__app_window.check_playername(self.__config.default_playername)
        self.__listener_thread.start()

    @pyqtSlot(int, int)
    def __on_listener_thread_event(self, mouse_x: int, mouse_y: int) -> None:
        self.__app_window.show_status_message('try to detect playername')
        self.__detect_player_name_service.detect(mouse_x, mouse_y)

    @pyqtSlot(Exception)
    def __on_exception(self, exception: Exception) -> Any:
        # self.__app_window.show_status_message(ex.message)
        if not isinstance(exception, NoPlayernameFoundException):
            self.__logger.exception(exception)
            exception_window = ExceptionDialog(exception)
            exception_window.exec_()
            self.__qapp_wrap.exit(1)
