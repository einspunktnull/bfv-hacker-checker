import cv2
import numpy as np
from PIL import Image, ImageGrab
from numpy import ndarray

from base.common import BoundingBox


class ImageUtil:

    @staticmethod
    def screenshot_region(region: BoundingBox, file_path: str = None) -> ndarray:
        image: Image = ImageGrab.grab(bbox=region, include_layered_windows=True, all_screens=True)
        if file_path:
            image.save(file_path)
        return np.array(image)

    @staticmethod
    def open(file_path: str) -> ndarray:
        image: Image = Image.open(file_path)
        return np.array(image)

    @staticmethod
    def copy(image_data: ndarray, file_path: str = None) -> ndarray:
        copy: ndarray = np.copy(image_data)
        if file_path:
            ImageUtil.save(copy, file_path)
        return copy

    @staticmethod
    def save(image_data: ndarray, path: str) -> str:
        image: Image = Image.fromarray(image_data)
        image.save(path)
        return path

    @staticmethod
    def normalize(image_data: ndarray, file_path: str = None) -> ndarray:
        zero_arr: ndarray = np.zeros((image_data.shape[0], image_data.shape[1]))
        image_data_mod: ndarray = cv2.normalize(image_data, zero_arr, 0, 255, cv2.NORM_MINMAX)
        if file_path:
            ImageUtil.save(image_data_mod, file_path)
        return image_data_mod

    @staticmethod
    def greyscale(image_data: ndarray, file_path: str = None) -> ndarray:
        image_data_mod: ndarray = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        if file_path:
            ImageUtil.save(image_data_mod, file_path)
        return image_data_mod

    @staticmethod
    def bitwise_not(image_data: ndarray, file_path: str = None) -> ndarray:
        image_data_mod: ndarray = cv2.bitwise_not(image_data)
        if file_path:
            ImageUtil.save(image_data_mod, file_path)
        return image_data_mod

    @staticmethod
    def threshold(image_data: ndarray, file_path: str = None) -> ndarray:
        image_data_mod: ndarray = cv2.threshold(image_data, 100, 255, cv2.THRESH_BINARY)[1]
        if file_path:
            ImageUtil.save(image_data_mod, file_path)
        return image_data_mod

    @staticmethod
    def gaussian_blur(image_data: ndarray, file_path: str = None) -> ndarray:
        image_data_mod: ndarray = cv2.GaussianBlur(image_data, (1, 1), 0)
        if file_path:
            ImageUtil.save(image_data_mod, file_path)
        return image_data_mod
