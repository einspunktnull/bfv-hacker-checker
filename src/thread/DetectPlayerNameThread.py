import re
from typing import Final
from xml.dom import minidom
from xml.dom.minicompat import NodeList
from xml.dom.minidom import Document, Element

from PyQt5.QtCore import pyqtSignal, QObject
from numpy import ndarray

from service.ConfigService import ConfigService
from service.LoggingService import LoggingService
from base.common import PyQtSignal, BoundingBox, NoPlayernameFoundException, InvalidWindowHandleException
from thread.BaseThread import BaseThread
from util.ImageUtil import ImageUtil
from util.OcrUtil import OcrUtil
from util.WindowUtil import WindowUtil


class DetectPlayerNameThread(BaseThread):
    __BFV_WINDOW_TITLE: Final[str] = 'Battlefield™ V'
    __PATTERN_PLAYERNAME_REPLACE: Final[str] = r"\[\S{2,4}\]\ ?"
    signal_report: Final[PyQtSignal] = pyqtSignal(ndarray)
    signal_finished: Final[PyQtSignal] = pyqtSignal(str)

    def __init__(self, parent: QObject, config: ConfigService, logger: LoggingService, mouse_x: int, mouse_y: int):
        super().__init__(parent, config, logger)
        self.__mouse_x: int = mouse_x
        self.__mouse_y: int = mouse_y
        self.__poi_width_half: int = int(self._config.poi_width / 2)
        self.__poi_height_half: int = int(self._config.poi_height / 2)

    def run(self):
        try:
            try:
                WindowUtil.to_foreground_by_title(self.__BFV_WINDOW_TITLE)
            except InvalidWindowHandleException as exception:
                self._logger.debug(exception)
            mouse_bbox: BoundingBox = self.__calculate_bbox()
            screenshot_data: ndarray = ImageUtil.screenshot_region(mouse_bbox)
            screenshot_data_preprared: ndarray = self.__preprocess_screenshot(screenshot_data)
            alto_xml_str: str = OcrUtil.tesseract_alto(screenshot_data_preprared)
            alto_doc: Document = minidom.parseString(alto_xml_str)
            root_element: Element = alto_doc.documentElement
            string_nodes: NodeList = root_element.getElementsByTagName('String')
            try:
                string_node: Element = list(filter(self.__is_mouse_in_string, string_nodes))[0]
                player_name_raw: str = string_node.getAttribute('CONTENT')
                player_name: str = re.sub(self.__PATTERN_PLAYERNAME_REPLACE, "", player_name_raw)
                self._logger.info(f'found playername: "{player_name}"')
                self.signal_finished.emit(player_name)
            except Exception as exception:
                raise NoPlayernameFoundException('OCR did not found playername', exception)
        except Exception as exception:
            self.signal_exception.emit(exception)

    def __preprocess_screenshot(self, screenshot_data: ndarray) -> ndarray:
        self._logger.debug('DetectPlayerNameThread.__preprocess_screenshot')
        screenshot_data_mod: ndarray = ImageUtil.copy(screenshot_data)
        screenshot_data_mod = ImageUtil.normalize(screenshot_data_mod)
        screenshot_data_mod = ImageUtil.greyscale(screenshot_data_mod)
        screenshot_data_mod = ImageUtil.bitwise_not(screenshot_data_mod)
        screenshot_data_mod = ImageUtil.threshold(screenshot_data_mod)
        screenshot_data_mod = ImageUtil.gaussian_blur(screenshot_data_mod)
        self._logger.debug('emit report')
        self.signal_report.emit(screenshot_data_mod)
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

    def __calculate_bbox(self) -> BoundingBox:
        left: int = self.__mouse_x - self.__poi_width_half
        right: int = self.__mouse_x + self.__poi_width_half
        top: int = self.__mouse_y - self.__poi_height_half
        bottom: int = self.__mouse_y + self.__poi_height_half
        return left, top, right, bottom
