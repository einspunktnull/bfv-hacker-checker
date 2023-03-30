import os
import re
from datetime import datetime
from pathlib import Path
from typing import Callable, Final
from xml.dom import minidom
from xml.dom.minicompat import NodeList
from xml.dom.minidom import Document, Element

from PyQt5.QtCore import QThread, pyqtSignal
from numpy import ndarray

from lib.types import PyQtSignal, BoundingBox
from lib.util.ImageUtil import ImageUtil
from lib.util.OcrUtil import OcrUtil
from lib.util.WindowUtil import WindowUtil

WIDTH: Final[int] = 500
HEIGHT: Final[int] = 300


class DetectPlayerNameThread(QThread):
    __success_signal: PyQtSignal = pyqtSignal(str)
    __exception_signal: PyQtSignal = pyqtSignal(Exception)

    def __init__(
            self,
            succes_thread_fct: Callable,
            exception_thread_fct: Callable,
            mouse_x: int,
            mouse_y: int,
            data_dir: str = None
    ):
        super().__init__()
        print('DetectPlayerNameThread', mouse_x, mouse_y, data_dir)
        self.__success_signal.connect(succes_thread_fct)
        self.__exception_signal.connect(exception_thread_fct)
        self.__data_dir: str = data_dir
        self.__mouse_x: int = mouse_x
        self.__mouse_y: int = mouse_y

    def run(self):
        now: datetime = datetime.now()
        date_time_string: str = now.strftime("%Y%m%d%H%M%S")
        basename: str = f'window_screenshot_{date_time_string}.png'
        screenshot_path: str = os.path.join(self.__data_dir, basename)
        try:
            window_handle: int = WindowUtil.to_foreground_by_title('Battlefield™ V')
            window_bbox: BoundingBox = WindowUtil.get_bbox_by_handle(window_handle)
            mouse_bbox: BoundingBox = self.__calculate_bbox()
            screenshot_data: ndarray = ImageUtil.screenshot_region(
                mouse_bbox,
                screenshot_path
            )
            screenshot_data_preprared: ndarray = self.__preprocess_screenshot(screenshot_data, screenshot_path)
            alto_xml_str: str = OcrUtil.tesseract_alto(screenshot_data_preprared)
            alto_doc: Document = minidom.parseString(alto_xml_str)
            root_element: Element = alto_doc.documentElement
            string_nodes: NodeList = root_element.getElementsByTagName('String')
            try:
                string_node: Element = list(filter(DetectPlayerNameThread.__is_mouse_in_string, string_nodes))[0]
                player_name_raw: str = string_node.getAttribute('CONTENT')
                player_name: str = re.sub(r"\[\S{2,4}\]\ ?", "", player_name_raw)
                self.__success_signal.emit(player_name)
            except Exception as e:
                raise Exception('no_playername_found')
        except Exception as e:
            self.__exception_signal.emit(e)

    def __calculate_bbox(self) -> BoundingBox:
        left: int = int(self.__mouse_x - WIDTH / 2)
        right: int = int(self.__mouse_x + WIDTH / 2)
        top: int = int(self.__mouse_y - HEIGHT / 2)
        bottom: int = int(self.__mouse_y + HEIGHT / 2)
        return left, top, right, bottom

    def __preprocess_screenshot(self, screenshot_data: ndarray, screenshot_path: str) -> ndarray:
        image_name_stem: str = Path(screenshot_path).stem
        screenshot_data_mod: ndarray = ImageUtil.copy(
            screenshot_data,
            os.path.join(self.__data_dir, f'{image_name_stem}.00_copy.png') if self.__data_dir else None
        )
        screenshot_data_mod = ImageUtil.normalize(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.01_normalized.png') if self.__data_dir else None
        )
        screenshot_data_mod = ImageUtil.greyscale(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.02_grey.png') if self.__data_dir else None
        )
        screenshot_data_mod = ImageUtil.bitwise_not(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.03_inverted.png') if self.__data_dir else None
        )
        screenshot_data_mod = ImageUtil.threshold(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.04_thresholded.png') if self.__data_dir else None
        )
        screenshot_data_mod = ImageUtil.gaussian_blur(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.05_blurred.png') if self.__data_dir else None
        )
        return screenshot_data_mod

    @staticmethod
    def __is_mouse_in_string(string_node: Element) -> bool:
        vpos: int = int(string_node.getAttribute('VPOS'))
        hpos: int = int(string_node.getAttribute('HPOS'))
        width: int = int(string_node.getAttribute('WIDTH'))
        height: int = int(string_node.getAttribute('HEIGHT'))
        left: int = hpos
        top: int = vpos
        right: int = left + width
        bottom: int = top + height
        is_between_left_and_right = left <= WIDTH / 2 <= right
        is_between_top_and_bottom = top <= HEIGHT / 2 <= bottom
        return is_between_left_and_right and is_between_top_and_bottom
