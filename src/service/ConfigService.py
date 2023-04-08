import os
import sys
from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
from typing import Final

from PyQt5.QtCore import QObject

from base.Hotkey import Hotkey
from base.Loglevel import Loglevel
from base.common import ConfigException, OS_PLATFORM_WINDOWS
from version import VERSION

_APP_NAME: Final[str] = 'Battlefield V Hacker Checker'
_ICON_PATH: Final[str] = "res/icon.png"
_ROOT_DIR: Final[str] = os.getcwd()
_DATA_DIR: Final[str] = os.path.join(_ROOT_DIR, "data")
_BIN_DIR: Final[str] = os.path.join(_ROOT_DIR, "bin")
_LOG_DIR: Final[str] = os.path.join(_ROOT_DIR, 'log')
_TESS_ZIP_PATH: Final[str] = os.path.join(_BIN_DIR, 'Tesseract-OCR.zip')
_TESS_DIR_PATH: Final[str] = os.path.join(_BIN_DIR, 'Tesseract-OCR')
_TESS_EXE_PATH_WINDOWS: Final[str] = os.path.join(_TESS_DIR_PATH, 'tesseract.exe')
_TESS_EXE_PATH_LINUX: Final[str] = os.path.join(_BIN_DIR, 'tesseract-5.3.0-x86_64.AppImage')
_TESS_EXE_PATH: Final[str] = _TESS_EXE_PATH_WINDOWS if sys.platform == OS_PLATFORM_WINDOWS else _TESS_EXE_PATH_LINUX
_LOGGER_NAME: Final[str] = 'THA_LOGGA'


class ConfigService(QObject):

    def __init__(self):
        super().__init__()
        argument_parser: ArgumentParser = ArgumentParser(
            description="Choose players of current match for a cheater check via bfvhackers.com"
        )
        argument_parser.add_argument(
            '--debug',
            '-d',
            action='store_true'
        )
        argument_parser.add_argument(
            '--config',
            '-c',
            type=str,
            default='config.ini'
        )
        self.__args: Namespace = argument_parser.parse_args()
        self.__config_parser: ConfigParser = ConfigParser()
        self.__config_parser.read(self.__args.config)
        hotkey: str = self.__config_parser.get('user', 'hotkey')
        is_allowed_key: bool = hotkey in Hotkey.__members__
        if not is_allowed_key:
            raise ConfigException('invalid hotkey defined in config.ini')

    @property
    def app_name(self) -> str:
        return _APP_NAME

    @property
    def icon_path(self) -> str:
        return _ICON_PATH

    @property
    def bin_dir(self) -> str:
        return _BIN_DIR

    @property
    def tesseract_exe(self) -> str:
        cfg_tess_exe: str = self.__config_parser.get('user', 'tesseract_exe', fallback=None)
        return cfg_tess_exe if cfg_tess_exe else _TESS_EXE_PATH

    @property
    def tesseract_zip(self) -> str:
        return _TESS_ZIP_PATH

    @property
    def logger_name(self) -> str:
        return _LOGGER_NAME

    @property
    def log_dir(self) -> str:
        return _LOG_DIR

    @property
    def version(self) -> str:
        return VERSION

    @property
    def debug(self) -> bool:
        return self.__args.debug or self.__config_parser.getboolean('app', 'debug', fallback=False)

    @property
    def url(self) -> str:
        return self.__config_parser.get('app', 'url')

    @property
    def hotkey(self) -> str:
        return self.__config_parser.get('user', 'hotkey')

    @property
    def poi_width(self) -> int:
        return self.__config_parser.getint('user', 'poi_width', fallback=300)

    @property
    def poi_height(self) -> int:
        return self.__config_parser.getint('user', 'poi_height', fallback=150)

    @property
    def always_on_top(self) -> bool:
        return self.__config_parser.getboolean('app', 'always_on_top', fallback=False)

    @property
    def default_playername(self) -> str:
        return self.__config_parser.get('user', 'default_playername', fallback='Breeksn')

    @property
    def log_level(self) -> Loglevel:
        lvl: str = self.__config_parser.get('logging', 'level', fallback='DEBUG')
        log_level: Loglevel = Loglevel.__members__[lvl]
        return log_level

    @property
    def theme(self) -> str:
        return self.__config_parser.get('app', 'theme', fallback='none')
