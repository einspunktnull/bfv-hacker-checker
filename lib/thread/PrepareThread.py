import os
import shutil
import sys
from time import sleep
from typing import Callable, Final

from PyQt5.QtCore import QThread, pyqtSignal
from pytesseract import pytesseract

from lib.Config import Config
from lib.Hotkey import Hotkey
from lib.common import PyQtSignal, OS_PLATFORM_WINDOWS
from lib.util.FileUtil import FileUtil


class PrepareThread(QThread):
    __PROGRESS_SIGNAL: Final[PyQtSignal] = pyqtSignal(str)
    __SUCCESS_SIGNAL: Final[PyQtSignal] = pyqtSignal()
    __EXCEPTION_SIGNAL: Final[PyQtSignal] = pyqtSignal(Exception)

    def __init__(
            self,
            config: Config,
            progress_fct: Callable,
            success_fct: Callable,
            exception_fct: Callable,
    ):
        super().__init__()
        self.__config: Config = config
        self.__PROGRESS_SIGNAL.connect(progress_fct)
        self.__SUCCESS_SIGNAL.connect(success_fct)
        self.__EXCEPTION_SIGNAL.connect(exception_fct)

    def run(self):
        self.__PROGRESS_SIGNAL.emit('PrepareThread.run')
        sleep(5)
        if sys.platform == OS_PLATFORM_WINDOWS and os.path.exists(self.__config.tesseract_exe):
            pytesseract.tesseract_cmd = self.__config.tesseract_exe
        is_allowed_key: bool = self.__config.hotkey in Hotkey.__members__
        if not is_allowed_key:
            raise RuntimeError('invalid hotkey defined in config.ini')
        if self.__config.clear_data_dir and os.path.exists(self.__config.data_dir):
            shutil.rmtree(self.__config.data_dir)
        if self.__config.debug:
            os.makedirs(self.__config.data_dir, exist_ok=True)
        if sys.platform == OS_PLATFORM_WINDOWS and not os.path.exists(self.__config.tesseract_exe):
            self.__PROGRESS_SIGNAL.emit('provisioning tesseract ...')
            FileUtil.merge_files(self.__config.tesseract_zip, self.__config.tesseract_zip)
            FileUtil.unzip(self.__config.tesseract_zip, self.__config.bin_dir)
            self.__PROGRESS_SIGNAL.emit('... done')
        self.__PROGRESS_SIGNAL.emit('JOOOOOOOOO')
        self.__SUCCESS_SIGNAL.emit()
