import enum
from typing import Union, Tuple, List, Any

from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal

PyQtSignal = Union[pyqtSignal, pyqtBoundSignal]
BoundingBox = Tuple[int, int, int, int]
Args = List[Any]


class AppException(Exception):
    pass


class NoPlayernameFoundException(AppException):
    pass


class InvalidWindowHandleException(AppException):
    pass


class ExitCode(enum.IntEnum):
    OK = 0
    DETECT_THREAD_FAILED = 1
