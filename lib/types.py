import enum
from typing import Union, Tuple

from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal

PyQtSignal = Union[pyqtSignal, pyqtBoundSignal]
BoundingBox = Tuple[int, int, int, int]


class AppException(Exception):
    pass


class NoPlayernameFoundException(AppException):
    pass


class InvalidWindowHandleException(AppException):
    pass


class ExitCode(enum.IntEnum):
    OK = 0
    DETECT_THREAD_FAILED = 1
