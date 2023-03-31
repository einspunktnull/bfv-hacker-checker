import os
import sys
from argparse import ArgumentParser
from configparser import ConfigParser
from typing import Final

from lib.App import App

# THIS_DIR: Final[str] = os.path.dirname(os.path.realpath(__file__))
THIS_DIR: Final[str] = os.getcwd()
DATA_DIR: Final[str] = os.path.join(THIS_DIR, "data")
BIN_DIR: Final[str] = os.path.join(THIS_DIR, "bin")
TESS_ZIP_PATH: Final[str] = os.path.join(BIN_DIR, 'Tesseract-OCR.zip')
TESS_DIR_PATH: Final[str] = os.path.join(BIN_DIR, 'Tesseract-OCR')
TESS_EXE_PATH: str = os.path.join(TESS_DIR_PATH, 'tesseract.exe')

if __name__ == '__main__':
    parser: ArgumentParser = ArgumentParser(
        description="Choose players of current match for a cheater check via bfvhackers.com"
    )
    parser.add_argument(
        '--debug',
        '-d',
        action='store_true'
    )
    parser.add_argument(
        '--config',
        '-c',
        type=str,
        default='config.ini'
    )
    parser.add_argument(
        '--clear-data-dir',
        '-C',
        action='store_true'
    )
    args = parser.parse_args()

    config: ConfigParser = ConfigParser()
    config.read(args.config)

    app: App = App(
        name='Battlefield V Hacker Checker',
        icon_path="res/icon.png",
        url=config.get('app', 'url'),
        key=config.get('user', 'hotkey'),
        data_dir=DATA_DIR,
        tesseract_exe=TESS_EXE_PATH,
        tesseract_zip=TESS_ZIP_PATH,
        bin_dir=BIN_DIR,
        clear_data_dir=args.clear_data_dir,
        debug=args.debug
    )
    sys.exit(app.run())
