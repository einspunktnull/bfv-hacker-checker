import os
import sys
import zipfile
from configparser import ConfigParser
from typing import Final

from lib.App import App

THIS_DIR: Final[str] = os.path.dirname(os.path.realpath(__file__))
DATA_DIR: Final[str] = os.path.join(THIS_DIR, "data")
BIN_DIR: Final[str] = os.path.join(THIS_DIR, "bin")
TESS_ZIP_PATH: Final[str] = os.path.join(BIN_DIR, 'Tesseract-OCR.zip')
TESS_DIR_PATH: Final[str] = os.path.join(BIN_DIR, 'Tesseract-OCR')
TESS_EXE_PATH: str = os.path.join(TESS_DIR_PATH, 'tesseract.exe')

if __name__ == '__main__':
    config: ConfigParser = ConfigParser()
    config.read('config.ini')

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(TESS_EXE_PATH):
        with zipfile.ZipFile(TESS_ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(BIN_DIR)

    app: App = App(
        name='Battlefield V Hacker Checker',
        icon_path="res/icon.png",
        url=config.get('app', 'url'),
        key=config.get('user', 'key'),
        default_player=config.get('user', 'default_player'),
        data_dir=DATA_DIR,
        tesseract_exe=TESS_EXE_PATH,
    )

    sys.exit(app.run())
