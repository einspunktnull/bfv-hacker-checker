import sys
from typing import Union, Tuple

from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt5.QtGui import QFont, QFontDatabase

OS_PLATFORM: str = sys.platform
OS_PLATFORM_LINUX: str = "linux"
OS_PLATFORM_WINDOWS: str = "win32"

PyQtSignal = Union[pyqtSignal, pyqtBoundSignal]
BoundingBox = Tuple[int, int, int, int]


def get_monospace_font() -> QFont:
    return QFontDatabase.systemFont(QFontDatabase.FixedFont)


class AppException(Exception):
    def __init__(self, message: str, *args):
        super().__init__(message, *args)
        self.__message: str = message

    @property
    def message(self) -> str:
        return self.__message


class ConfigException(AppException):
    pass


class NoPlayernameFoundException(AppException):
    def __init__(self, *args):
        super().__init__(f'no playername detected', *args)


class InvalidWindowHandleException(AppException):
    def __init__(self, *args):
        super().__init__(f'invalid window handle: {sys.platform}', *args)


class UnsupportedOsException(AppException):

    def __init__(self):
        super().__init__(f'Unsupported OS: {sys.platform}')
