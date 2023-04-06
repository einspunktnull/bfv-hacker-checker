import logging
import os.path
from typing import Any, Final

from injector import inject

from lib.Config import Config
from lib.util.StringUtil import StringUtil


class Logger:
    DEFAULT_FORMATTER: Final[logging.Formatter] = logging.Formatter('[%(asctime)s - %(levelname)s] %(message)s')

    @inject
    def __init__(self, config: Config):
        self.__logger: logging.Logger = logging.getLogger(config.logger_name)
        self.__logger.setLevel(config.log_level)

        if not config.debug:
            return

        os.makedirs(config.log_dir, exist_ok=True)

        stream_handler: logging.StreamHandler = logging.StreamHandler()
        stream_handler.formatter = self.DEFAULT_FORMATTER
        self.__logger.addHandler(stream_handler)

        log_file_name: str = os.path.join(config.log_dir, f'{StringUtil.get_now_string()}.log')
        file_handler: logging.FileHandler = logging.FileHandler(
            log_file_name, encoding='utf-8'
        )
        file_handler.formatter = self.DEFAULT_FORMATTER
        self.__logger.addHandler(file_handler)

    def add_handler(self, handler: logging.Handler):
        self.__logger.addHandler(handler)

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
