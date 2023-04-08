from typing import Optional, Final

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from injector import inject
from numpy import ndarray

from service.ConfigService import ConfigService
from service.LoggingService import LoggingService
from base.common import PyQtSignal, NoPlayernameFoundException
from thread.DetectPlayerNameThread import DetectPlayerNameThread


class DetectPlayerNameService(QObject):
    signal_detection_result: Final[PyQtSignal] = pyqtSignal(str)
    signal_exception: Final[PyQtSignal] = pyqtSignal(Exception)
    signal_report: Final[PyQtSignal] = pyqtSignal(ndarray)

    @inject
    def __init__(self, config: ConfigService, logger: LoggingService):
        super().__init__()
        self.__config: ConfigService = config
        self.__logger: LoggingService = logger
        self.__detect_thread: Optional[DetectPlayerNameThread] = None

    def detect(self, mouse_x: int, mouse_y: int) -> None:
        if self.__detect_thread is None:
            self.__detect_thread = DetectPlayerNameThread(
                self,
                self.__config,
                self.__logger,
                mouse_x,
                mouse_y,
            )
            self.__detect_thread.signal_finished.connect(self.__on_detect_thread_success)
            self.__detect_thread.signal_exception.connect(self.__on_thread_exception)
            self.__detect_thread.signal_report.connect(self.__on_detect_thread_report)
            self.__detect_thread.start()

    @pyqtSlot(str)
    def __on_detect_thread_success(self, player_name: str) -> None:
        self.signal_detection_result.emit(player_name)
        self.__detect_thread = None

    @pyqtSlot(ndarray)
    def __on_detect_thread_report(self, image: ndarray) -> None:
        self.__logger.debug('__on_detect_thread_report')
        self.signal_report.emit(image)

    @pyqtSlot(Exception)
    def __on_thread_exception(self, exception: Exception) -> None:
        if isinstance(exception, NoPlayernameFoundException):
            self.__logger.warning(exception.args[0])
        self.signal_exception.emit(exception)
        self.__detect_thread = None
