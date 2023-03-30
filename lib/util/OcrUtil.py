from numpy import ndarray
from pytesseract import pytesseract


class OcrUtil:

    @staticmethod
    def tesseract_alto(image_data: ndarray) -> str:
        return pytesseract.image_to_alto_xml(image_data, lang='eng', config='')
