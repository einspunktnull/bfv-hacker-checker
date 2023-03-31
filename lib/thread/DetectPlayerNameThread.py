import os
import re
from datetime import datetime
from pathlib import Path
from typing import Callable, Final, Optional
from xml.dom import minidom
from xml.dom.minicompat import NodeList
from xml.dom.minidom import Document, Element

from PyQt5.QtCore import QThread, pyqtSignal
from numpy import ndarray

from lib.types import PyQtSignal, BoundingBox, NoPlayernameFoundException, InvalidWindowHandleException
from lib.util.ImageUtil import ImageUtil
from lib.util.OcrUtil import OcrUtil
from lib.util.WindowUtil import WindowUtil


class DetectPlayerNameThread(QThread):
    __PATTERN_PLAYERNAME_REPLACE: Final[str] = r"\[\S{2,4}\]\ ?"
    __SUCCESS_SIGNAL: Final[PyQtSignal] = pyqtSignal(str)
    __EXCEPTION_SIGNAL: Final[PyQtSignal] = pyqtSignal(Exception)

    def __init__(
            self,
            succes_thread_fct: Callable,
            exception_thread_fct: Callable,
            poi_width: int,
            poi_height: int,
            mouse_x: int,
            mouse_y: int,
            data_dir: str = None
    ):
        super().__init__()
        # print('DetectPlayerNameThread', mouse_x, mouse_y, data_dir)
        self.__SUCCESS_SIGNAL.connect(succes_thread_fct)
        self.__EXCEPTION_SIGNAL.connect(exception_thread_fct)
        self.__data_dir: str = data_dir
        self.__mouse_x: int = mouse_x
        self.__mouse_y: int = mouse_y
        self.__poi_width_half: int = int(poi_width / 2)
        self.__poi_height_half: int = int(poi_height / 2)

    def run(self):
        screenshot_path: Optional[str] = None
        if self.__data_dir:
            now: datetime = datetime.now()
            date_time_string: str = now.strftime("%Y%m%d%H%M%S")
            basename: str = f'window_screenshot_{date_time_string}.png'
            screenshot_path = os.path.join(self.__data_dir, basename)

        try:
            try:
                WindowUtil.to_foreground_by_title('Battlefield™ V')
            except InvalidWindowHandleException as exception:
                pass
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
                string_node: Element = list(filter(self.__is_mouse_in_string, string_nodes))[0]
                player_name_raw: str = string_node.getAttribute('CONTENT')
                player_name: str = re.sub(self.__PATTERN_PLAYERNAME_REPLACE, "", player_name_raw)
                self.__SUCCESS_SIGNAL.emit(player_name)
            except Exception as exception:
                raise NoPlayernameFoundException('OCR did not found playername', exception)
        except Exception as exception:
            self.__EXCEPTION_SIGNAL.emit(exception)

    def __calculate_bbox(self) -> BoundingBox:
        left: int = self.__mouse_x - self.__poi_width_half
        right: int = self.__mouse_x + self.__poi_width_half
        top: int = self.__mouse_y - self.__poi_height_half
        bottom: int = self.__mouse_y + self.__poi_height_half
        return left, top, right, bottom

    def __preprocess_screenshot(self, screenshot_data: ndarray, screenshot_path: str) -> ndarray:
        image_name_stem: str = Path(screenshot_path).stem if screenshot_path else None
        screenshot_data_mod: ndarray = ImageUtil.copy(
            screenshot_data,
            os.path.join(self.__data_dir, f'{image_name_stem}.00_copy.png') if screenshot_path else None
        )
        screenshot_data_mod = ImageUtil.normalize(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.01_normalized.png') if screenshot_path else None
        )
        screenshot_data_mod = ImageUtil.greyscale(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.02_grey.png') if screenshot_path else None
        )
        screenshot_data_mod = ImageUtil.bitwise_not(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.03_inverted.png') if screenshot_path else None
        )
        screenshot_data_mod = ImageUtil.threshold(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.04_thresholded.png') if screenshot_path else None
        )
        screenshot_data_mod = ImageUtil.gaussian_blur(
            screenshot_data_mod,
            os.path.join(self.__data_dir, f'{image_name_stem}.05_blurred.png') if screenshot_path else None
        )
        return screenshot_data_mod

    def __is_mouse_in_string(self, string_node: Element) -> bool:
        vpos: int = int(string_node.getAttribute('VPOS'))
        hpos: int = int(string_node.getAttribute('HPOS'))
        width: int = int(string_node.getAttribute('WIDTH'))
        height: int = int(string_node.getAttribute('HEIGHT'))
        left: int = hpos
        top: int = vpos
        right: int = left + width
        bottom: int = top + height
        is_between_left_and_right = left <= self.__poi_width_half <= right
        is_between_top_and_bottom = top <= self.__poi_height_half <= bottom
        return is_between_left_and_right and is_between_top_and_bottom
