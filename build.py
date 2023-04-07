import os.path
import re
import shutil
import subprocess
import sys
from typing import Final

from lib.util.FileUtil import FileUtil
from set_version import set_version

BASE_NAME: str = r"bfv-hacker-checker"
DIST_DIR: Final[str] = os.path.join('dist', BASE_NAME)
BIN_DIR: Final[str] = os.path.join(DIST_DIR, 'bin')
VERSION_SOURCE_FILE: Final[str] = r'lib/version.py'

if __name__ == '__main__':
    debug: bool = len(sys.argv) >= 2 and sys.argv[1] == 'debug'
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    version: str = set_version()
    subprocess.run([
        'pyinstaller',
        '--windowed',
        '--noconfirm',
        '--onefile',
        r'--icon=res\icon.png',
        f'--distpath={DIST_DIR}',
        f'--name={BASE_NAME}',
        'main.py'
    ])
    FileUtil.copy('res', os.path.join(DIST_DIR, 'res'))
    FileUtil.copy('config.ini' if debug else 'config.release.ini', os.path.join(DIST_DIR, 'config.ini'))
    FileUtil.copy('README.md', DIST_DIR)
    os.makedirs(BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part0'), BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part1'), BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part2'), BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part3'), BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part4'), BIN_DIR)
    directory: str = os.path.join('dist', BASE_NAME)
    dest_zip_name: str = f'bfv-hacker-checker{"_debug" if debug else ""}_{version.replace(".", "_")}.zip'
    dest_zip: str = os.path.join('dist', dest_zip_name)
    FileUtil.zip(directory, dest_zip)
