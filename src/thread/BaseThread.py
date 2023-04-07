from typing import Final

from PyQt5.QtCore import QThread, QObject, pyqtSignal

from service.ConfigService import ConfigService
from service.LoggingService import LoggingService
from base.common import PyQtSignal


class BaseThread(QThread):
    __signal_exception: Final[PyQtSignal] = pyqtSignal(Exception)

    def __init__(self, parent: QObject, config: ConfigService, logger: LoggingService):
        super().__init__(parent)
        self.__config: ConfigService = config
        self.__logger: LoggingService = logger

    @property
    def signal_exception(self) -> PyQtSignal:
        return self.__signal_exception

    @property
    def _config(self) -> ConfigService:
        return self.__config

    @property
    def _logger(self) -> LoggingService:
        return self.__logger

    def emit_exception(self, exception: Exception) -> None:
        self.signal_exception.emit(exception)
