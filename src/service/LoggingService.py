import logging
import os.path
from typing import Any, Final

from PyQt5.QtCore import QObject, pyqtSignal
from injector import inject

from service.ConfigService import ConfigService
from base.common import PyQtSignal
from util.StringUtil import StringUtil


class LoggingService(QObject, logging.Handler):
    DEFAULT_FORMATTER: Final[logging.Formatter] = logging.Formatter('[%(asctime)s - %(levelname)s] %(message)s')

    signal_message: Final[PyQtSignal] = pyqtSignal(str)

    #
    @inject
    def __init__(self, config: ConfigService):
        super().__init__()
        self.__logger: logging.Logger = logging.getLogger(config.logger_name)
        self.__logger.setLevel(config.log_level)

        if not config.debug:
            return

        os.makedirs(config.log_dir, exist_ok=True)

        self.formatter = self.DEFAULT_FORMATTER
        self.__logger.addHandler(self)

        stream_handler: logging.StreamHandler = logging.StreamHandler()
        stream_handler.formatter = self.DEFAULT_FORMATTER
        self.__logger.addHandler(stream_handler)

        log_file_name: str = os.path.join(config.log_dir, f'{StringUtil.get_now_string()}.log')
        file_handler: logging.FileHandler = logging.FileHandler(
            log_file_name, encoding='utf-8'
        )
        file_handler.formatter = self.DEFAULT_FORMATTER
        self.__logger.addHandler(file_handler)

    def emit(self, record: logging.LogRecord):
        message: str = self.format(record)
        self.signal_message.emit(message)

    def critical(self, msg, *args: Any):
        self.__logger.critical(self.__args_to_str(msg, *args))

    def fatal(self, msg, *args: Any):
        self.__logger.fatal(self.__args_to_str(msg, *args))

    def error(self, msg, *args: Any):
        self.__logger.error(self.__args_to_str(msg, *args))

    def exception(self, msg, *args: Any):
        self.__logger.exception(self.__args_to_str(msg, *args))

    def warning(self, msg, *args: Any):
        self.__logger.warning(self.__args_to_str(msg, *args))

    def info(self, msg, *args: Any):
        self.__logger.info(self.__args_to_str(msg, *args))

    def debug(self, msg, *args: Any):
        self.__logger.debug(self.__args_to_str(msg, *args))

    @staticmethod
    def __args_to_str(msg, *args: Any) -> str:
        return f'{str(msg)} {", ".join(args)}'
