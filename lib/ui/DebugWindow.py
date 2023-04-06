from __future__ import annotations

import logging
from typing import Type

from PyQt5 import QtGui
from injector import inject

from lib.Config import Config
from lib.Logger import Logger
from lib.common import get_monospace_font
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
    @inject
    def __init__(self, config: Config, logger: Logger):
        super().__init__(config, logger)
        handler: ConsoleHandler = ConsoleHandler(self)
        handler.setFormatter(Logger.DEFAULT_FORMATTER)
        logger.add_handler(handler)

    def _init_ui(self):
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

    def add_log_text(self, message: str):
        self._ui.plainTextEdit.appendPlainText(message)
        self._ui.plainTextEdit.moveCursor(QtGui.QTextCursor.End)
        self._ui.plainTextEdit.ensureCursorVisible()
