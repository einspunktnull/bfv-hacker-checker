import enum
import sys
from typing import Union, Tuple, Final

from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal

OS_PLATFORM: str = sys.platform
OS_PLATFORM_LINUX: str = "linux"
OS_PLATFORM_WINDOWS: str = "win32"


PyQtSignal = Union[pyqtSignal, pyqtBoundSignal]
BoundingBox = Tuple[int, int, int, int]


class AppException(Exception):
    pass


class NoPlayernameFoundException(AppException):
    pass


class InvalidWindowHandleException(AppException):
    def __init__(self, *args):
        super().__init__(f'invalid window handle: {sys.platform}', *args)


class UnsupportedOsException(AppException):

    def __init__(self):
        super().__init__(f'Unsupported OS: {sys.platform}')


class ExitCode(enum.IntEnum):
    OK = 0
    DETECT_THREAD_FAILED = 1
