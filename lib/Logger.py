import enum
import logging

from injector import inject

from lib.Config import Config
from lib.types import Args


class Loglevel(enum.IntEnum):
    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class Logger:

    @inject
    def __init__(self, config: Config):
        self.__logger: Logger = logging.getLogger(config.logger_name)
        logging.basicConfig(
            level=logging.DEBUG
        )

    def critical(self, msg, *args: Args):
        self.__logger.critical(msg, *args)

    def fatal(self, msg, *args: Args):
        self.__logger.fatal(msg, *args)
        pass

    def error(self, msg, *args: Args):
        self.__logger.error(msg, *args)
        pass

    def exception(self, msg, *args: Args):
        self.__logger.exception(msg, *args)
        pass

    def warning(self, msg, *args: Args):
        self.__logger.warning(msg, *args)
        pass

    def info(self, msg, *args: Args):
        self.__logger.info(msg, *args)
        pass

    def debug(self, msg, *args: Args):
        self.__logger.debug(msg, *args)
        pass

    def log(self, msg, *args: Args):
        self.__logger.log(msg, *args)
        pass
