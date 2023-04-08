from typing import Final

from PyQt5.QtCore import QObject
from injector import inject

from base.common import PyQtSignal
from service.ConfigService import ConfigService
from service.LoggingService import LoggingService
from thread.PrepareThread import PrepareThread


class PrepareService(QObject):
    @inject
    def __init__(self, config: ConfigService, logger: LoggingService):
        super().__init__()
        self.__config: ConfigService = config
        self.__logger: LoggingService = logger
        self.__prepare_thread: PrepareThread = PrepareThread(self, config, logger)
        self.signal_status: Final[PyQtSignal] = self.__prepare_thread.signal_status
        self.signal_finished: Final[PyQtSignal] = self.__prepare_thread.signal_finished
        self.signal_exception: Final[PyQtSignal] = self.__prepare_thread.signal_exception

    def prepare(self):
        self.__prepare_thread.start()
