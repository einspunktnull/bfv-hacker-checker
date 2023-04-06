from __future__ import annotations

import logging
from typing import Type, Final

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent, QPixmap, QImage
from injector import inject
from numpy import ndarray

from lib.Config import Config
from lib.Logger import Logger
from lib.common import get_monospace_font, PyQtSignal
from lib.ui.AbstractBaseWindow import AbstractBaseWindow
from lib.ui_generated.Ui_DebugWindow import Ui_DebugWindow


class ConsoleHandler(logging.Handler):

    def __init__(self, window: DebugWindow):
        super().__init__()
        self.__debug_window: DebugWindow = window

    def emit(self, record: logging.LogRecord):
        message: str = self.format(record)
        self.__debug_window.add_log_text(message)


class DebugWindow(AbstractBaseWindow[Ui_DebugWindow]):
    CLOSED: Final[PyQtSignal] = pyqtSignal()

    @inject
    def __init__(self, config: Config, logger: Logger):
        super().__init__(config, logger)
        handler: ConsoleHandler = ConsoleHandler(self)
        handler.setFormatter(Logger.DEFAULT_FORMATTER)
        logger.add_handler(handler)

    def _init_ui(self):
        self.setWindowTitle('Debugging Window')
        self._ui.plainTextEdit.clear()
        self._ui.plainTextEdit.setFont(get_monospace_font())
        stylesheet = """
        QSplitterHandle {
            background-color: red;
        }
        """
        self._ui.splitter.setStyleSheet(stylesheet)

    def _get_ui(self) -> Type[Ui_DebugWindow]:
        return Ui_DebugWindow

    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        self.CLOSED.emit()

    def add_log_text(self, message: str):
        self._ui.plainTextEdit.appendPlainText(message)
        self._ui.plainTextEdit.moveCursor(QtGui.QTextCursor.End)
        self._ui.plainTextEdit.ensureCursorVisible()

    def set_detection_report(self, image: ndarray):
        # self._logger.debug('set_detection_report', str(image))
        pixmap: QPixmap = QPixmap.fromImage(
            QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8))
        self._ui.label_image_processed.setPixmap(pixmap)
