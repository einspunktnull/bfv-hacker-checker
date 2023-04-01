import os
from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
from typing import Final

_APP_NAME: Final[str] = 'Battlefield V Hacker Checker'
_ICON_PATH: Final[str] = "res/icon.png"
_ROOT_DIR: Final[str] = os.getcwd()
_UI_DIR: str = os.path.join(_ROOT_DIR, 'ui')
_DATA_DIR: Final[str] = os.path.join(_ROOT_DIR, "data")
_BIN_DIR: Final[str] = os.path.join(_ROOT_DIR, "bin")
_UI_FILE_PATH: str = os.path.join(_UI_DIR, 'form.ui')
_TESS_ZIP_PATH: Final[str] = os.path.join(_BIN_DIR, 'Tesseract-OCR.zip')
_TESS_DIR_PATH: Final[str] = os.path.join(_BIN_DIR, 'Tesseract-OCR')
_TESS_EXE_PATH: str = os.path.join(_TESS_DIR_PATH, 'tesseract.exe')


class Config:

    def __init__(self):
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
        argument_parser.add_argument(
            '--clear-data-dir',
            '-C',
            action='store_true'
        )
        self.__args: Namespace = argument_parser.parse_args()
        self.__config_parser: ConfigParser = ConfigParser()
        self.__config_parser.read(self.__args.config)

    @property
    def app_name(self) -> str:
        return _APP_NAME

    @property
    def icon_path(self) -> str:
        return _ICON_PATH

    @property
    def data_dir(self) -> str:
        return _DATA_DIR

    @property
    def bin_dir(self) -> str:
        return _BIN_DIR

    @property
    def tesseract_exe(self) -> str:
        return _TESS_EXE_PATH

    @property
    def tesseract_zip(self) -> str:
        return _TESS_ZIP_PATH

    @property
    def ui_file(self) -> str:
        return _UI_FILE_PATH

    @property
    def clear_data_dir(self) -> bool:
        return self.__args.clear_data_dir or self.__config_parser.getboolean('app', 'clear_data_dir', fallback=True)

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
