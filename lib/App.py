import os
import shutil
import sys
from time import sleep
from typing import Any, Dict, Optional

from PyQt5.QtWidgets import QApplication
from injector import singleton, Injector

from lib.Config import Config
from lib.Hotkey import Hotkey
from lib.MainWindow import MainWindow
from lib.thread.DetectPlayerNameThread import DetectPlayerNameThread
from lib.thread.UserInputListenerThread import UserInputListenerThread
from lib.types import NoPlayernameFoundException, ExitCode
from lib.util.FileUtil import FileUtil


class App:
    def __init__(self):
        self.__qapp: QApplication = QApplication([])

        injector: Injector = Injector()
        injector.binder.bind(Config, to=Config, scope=singleton)
        injector.binder.bind(MainWindow, to=MainWindow)

        self.__config: Config = injector.get(Config)
        self.__main_window: MainWindow = injector.get(MainWindow)
        self.__listener_thread: Optional[UserInputListenerThread] = UserInputListenerThread(
            self.__config.hotkey,
            self.__on_got_triggered
        )
        self.__detect_thread: Optional[DetectPlayerNameThread] = None

    def run(self) -> int:
        self.__main_window.show()
        self.__prepare()
        return self.__exec()

    def __prepare(self) -> None:
        is_allowed_key: bool = self.__config.hotkey in Hotkey.__members__
        if not is_allowed_key:
            raise RuntimeError('invalid key in config.ini')
        if self.__config.clear_data_dir and os.path.exists(self.__config.data_dir):
            shutil.rmtree(self.__config.data_dir)
        os.makedirs(self.__config.data_dir, exist_ok=True)
        if not os.path.exists(self.__config.tesseract_exe):
            self.__main_window.show_message('provisioning tesseract ...')
            FileUtil.merge_files(self.__config.tesseract_zip, self.__config.tesseract_zip)
            FileUtil.unzip(self.__config.tesseract_zip, self.__config.bin_dir)
            self.__main_window.show_message('... done')

    def __exec(self) -> int:
        self.__check_playername(self.__config.default_playername)
        self.__listener_thread.start()
        return self.__qapp.exec_()

    def __on_got_triggered(self, mouse_x: int, mouse_y: int) -> None:
        # print(f'__check_it ({mouse_x},{mouse_y})')
        if self.__detect_thread is None:
            self.__detect_thread = DetectPlayerNameThread(
                self.__check_playername,
                self.__on_thread_exception,
                self.__config.poi_width,
                self.__config.poi_height,
                mouse_x,
                mouse_y,
                self.__config.data_dir if self.__config.debug else None
            )
            self.__detect_thread.start()

    def __check_playername(self, player_name: str):
        query_params: Dict[str, Any] = {'name': player_name}
        self.__main_window.call_url(self.__config.url, query_params)
        if self.__detect_thread is not None:
            sleep(1)
            self.__detect_thread = None

    def __on_thread_exception(self, exception: Exception):
        self.__main_window.show_exception(exception)
        try:
            raise exception
        except NoPlayernameFoundException:
            pass
        except Exception:
            sys.exit(ExitCode.DETECT_THREAD_FAILED)
        sleep(1)
        self.__detect_thread = None
