import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from PyQt5.QtWidgets import QApplication
from numpy import ndarray
from pytesseract import pytesseract

from lib.ListenerThread import ListenerThread
from lib.MainWindow import MainWindow
from lib.NpImgUtil import NpImgUtil
from lib.Util import Util


class App:
    def __init__(
            self,
            name: str,
            icon_path: str,
            url: str,
            key: str,
            default_player: str,
            data_dir: str,
            tesseract_exe: str
    ):
        self.__url: str = url
        self.__key: str = key
        self.__default_player: str = default_player
        self.__data_dir: str = data_dir
        self.__tesseract_exe: str = tesseract_exe

        self.__qapp: QApplication = QApplication([])
        self.__main_window: MainWindow = MainWindow(name, icon_path)
        self.__is_busy: bool = False
        self.__listener_thread: ListenerThread = ListenerThread(self.__check_it)

    def run(self) -> int:
        self.__main_window.show()
        self.__listener_thread.start()
        code: int = self.__qapp.exec_()
        return code

    def __check_it(self, x: int, y: int):
        print(f'__check_it ({x},{y})')
        if not self.__is_busy:
            self.__is_busy = True
            try:
                player_name: str = self.__detect_playername()
                query_params: Dict[str, Any] = {'name': player_name}
                self.__main_window.call_url(self.__url, query_params)
            except Exception as e:
                MainWindow.show_exception(e)
            self.__is_busy = False

    def __detect_playername(self) -> str:
        screenshot_path: str = self.__create_screenshot()
        image_data: ndarray = self.__preprocess_screenshot(screenshot_path)
        alto: Any = pytesseract.image_to_string(image_data, lang='eng', config='').strip()
        # alto: Any = pytesseract.image_to_alto_xml(image_data, lang='eng', config='').strip()
        print(alto)
        return self.__default_player

    def __create_screenshot(self) -> str:
        now = datetime.now()
        date_time_string: str = now.strftime("%Y%m%d%H%M%S")
        img_save_path: str = f'{self.__data_dir}{os.path.sep}window_screenshot_{date_time_string}.png'
        return Util.make_window_screenshot('Battlefield™ V', img_save_path)

    def __preprocess_screenshot(self, image_path: str) -> ndarray:
        image_name_stem: str = Path(image_path).stem
        image_data: ndarray = NpImgUtil.open(image_path)
        image_data_mod: ndarray = NpImgUtil.copy(
            image_data,
            os.path.join(self.__data_dir, f'{image_name_stem}.00_copy.png')
        )
        image_data_mod = NpImgUtil.normalize(
            image_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.01_normalized.png')
        )
        image_data_mod = NpImgUtil.greyscale(
            image_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.02_grey.png')
        )
        image_data_mod = NpImgUtil.bitwise_not(
            image_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.03_inverted.png')
        )
        image_data_mod = NpImgUtil.threshold(
            image_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.04_thresholded.png')
        )
        image_data_mod = NpImgUtil.gaussian_blur(
            image_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.05_blurred.png')
        )
        return image_data_mod
