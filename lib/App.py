import os
import shutil
import zipfile
from time import sleep
from typing import Any, Dict, Optional

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from lib.Hotkey import Hotkey
from lib.thread.DetectPlayerNameThread import DetectPlayerNameThread
from lib.thread.UserInputListenerThread import UserInputListenerThread
from lib.MainWindow import MainWindow


class App:
    def __init__(
            self,
            name: str,
            icon_path: str,
            url: str,
            key: str,
            data_dir: str,
            tesseract_exe: str,
            tesseract_zip: str,
            bin_dir: str,
            clear_data_dir: bool,
            debug: bool = False
    ):
        self.__url: str = url
        self.__key: str = key
        self.__data_dir: str = data_dir
        self.__tesseract_exe: str = tesseract_exe
        self.__tesseract_zip: str = tesseract_zip
        self.__bin_dir: str = bin_dir
        self.__clear_data_dir: bool = clear_data_dir
        self.__debug: bool = debug

        self.__qapp: QApplication = QApplication([])
        self.__main_window: MainWindow = MainWindow(name, icon_path)
        self.__listener_thread: Optional[UserInputListenerThread] = None
        self.__detect_thread: Optional[DetectPlayerNameThread] = None

    def run(self) -> int:
        self.__main_window.show()
        try:
            self.__prepare()
            self.__init()
            return self.__exec()
        except Exception as e:
            self.__main_window.show_exception(e)
            return -1

    def __prepare(self) -> None:
        is_allowed_key: bool = self.__key in Hotkey.__members__
        if not is_allowed_key:
            raise RuntimeError('invalid key in config.ini')
        if os.path.exists(self.__data_dir):
            shutil.rmtree(self.__data_dir)
        os.makedirs(self.__data_dir, exist_ok=True)
        if not os.path.exists(self.__tesseract_exe):
            self.__main_window.show_message('extracting tesseract ...')
            with zipfile.ZipFile(self.__tesseract_zip, 'r') as zip_ref:
                zip_ref.extractall(self.__bin_dir)
            self.__main_window.show_message('... done')

    def __init(self) -> None:
        self.__listener_thread: UserInputListenerThread = UserInputListenerThread(self.__key, self.__check_it)
        self.__listener_thread.start()

    def __exec(self) -> int:
        return self.__qapp.exec_()

    def __check_it(self, mouse_x: int, mouse_y: int) -> None:
        # print(f'__check_it ({mouse_x},{mouse_y})')
        if self.__detect_thread is None:
            self.__detect_thread = DetectPlayerNameThread(
                self.__on_playername_detected,
                self.__on_thread_exception,
                mouse_x,
                mouse_y,
                self.__data_dir if self.__debug else None
            )
            self.__detect_thread.start(QThread.Priority.HighPriority)

    def __on_playername_detected(self, player_name: str):
        query_params: Dict[str, Any] = {'name': player_name}
        self.__main_window.call_url(self.__url, query_params)
        sleep(1)
        self.__detect_thread = None

    def __on_thread_exception(self, exception: Exception):
        self.__main_window.show_exception(exception)
        sleep(1)
        self.__detect_thread = None
