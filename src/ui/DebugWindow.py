from __future__ import annotations

from typing import Type, Final

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QPixmap, QImage
from injector import inject
from numpy import ndarray

from service.ConfigService import ConfigService
from service.LoggingService import LoggingService
from base.common import get_monospace_font, PyQtSignal
from ui.AbstractBaseWindow import AbstractBaseWindow
from service.DetectPlayerNameService import DetectPlayerNameService
from ui_generated.Ui_DebugWindow import Ui_DebugWindow


class DebugWindow(AbstractBaseWindow[Ui_DebugWindow]):
    __signal_close: Final[PyQtSignal] = pyqtSignal()

    @inject
    def __init__(
            self,
            config: ConfigService,
            logger: LoggingService,
            detect_player_name_service: DetectPlayerNameService
    ):
        self.__detect_player_name_service: DetectPlayerNameService = detect_player_name_service
        super().__init__(config, logger)

    def _post_init(self):
        self.setWindowTitle('Debugging Window')
        self._ui.label_image_processed.setText('preview_imaaage')
        self._ui.plainTextEdit.clear()
        self._ui.plainTextEdit.setFont(get_monospace_font())
        stylesheet = """
        QSplitterHandle {
            background-color: red;
        }
        """
        self._ui.splitter.setStyleSheet(stylesheet)

        self._logger.signal_message.connect(self.__add_log_message)
        self.__detect_player_name_service.signal_report.connect(self.__set_detection_report)

    def _get_ui(self) -> Type[Ui_DebugWindow]:
        return Ui_DebugWindow

    @property
    def signal_close(self) -> PyQtSignal:
        return self.__signal_close

    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)
        self.signal_close.emit()

    @pyqtSlot(ndarray)
    def __set_detection_report(self, image: ndarray):
        self._logger.debug('set_detection_report')
        pixmap: QPixmap = QPixmap.fromImage(
            QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Grayscale8))
        self._ui.label_image_processed.setPixmap(pixmap)

    @pyqtSlot(str)
    def __add_log_message(self, message: str):
        self._ui.plainTextEdit.appendPlainText(message)
        self._ui.plainTextEdit.moveCursor(QtGui.QTextCursor.End)
        self._ui.plainTextEdit.ensureCursorVisible()
