import os
import sys
from typing import Final

from PyQt5.QtCore import pyqtSignal, QObject
from pytesseract import pytesseract

from service.ConfigService import ConfigService
from service.LoggingService import LoggingService
from base.common import PyQtSignal, OS_PLATFORM_WINDOWS
from thread.BaseThread import BaseThread
from util.FileUtil import FileUtil


class PrepareThread(BaseThread):
    __signal_status: Final[PyQtSignal] = pyqtSignal(str)
    __signal_finished: Final[PyQtSignal] = pyqtSignal()

    def __init__(self, parent: QObject, config: ConfigService, logger: LoggingService):
        super().__init__(parent, config, logger)

    @property
    def signal_status(self) -> PyQtSignal:
        return self.__signal_status

    @property
    def signal_finished(self) -> PyQtSignal:
        return self.__signal_finished

    def run(self):
        try:
            if sys.platform == OS_PLATFORM_WINDOWS and not os.path.exists(self._config.tesseract_exe):
                self.signal_status.emit('provisioning tesseract ...')
                FileUtil.merge_files(self._config.tesseract_zip, self._config.tesseract_zip)
                FileUtil.unzip(self._config.tesseract_zip, self._config.bin_dir)
                self.signal_status.emit('... done')
            if sys.platform == OS_PLATFORM_WINDOWS and os.path.exists(self._config.tesseract_exe):
                pytesseract.tesseract_cmd = self._config.tesseract_exe
            self.signal_finished.emit()
        except Exception as exc:
            self.signal_exception.emit(exc)
