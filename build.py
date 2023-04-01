import os.path
import re
import shutil
import subprocess
from typing import Final

from lib.util.FileUtil import FileUtil

BASE_NAME: Final[str] = r"bfv-hacker-checker"
DIST_DIR: Final[str] = os.path.join('dist', BASE_NAME)
BIN_DIR: Final[str] = os.path.join(DIST_DIR, 'bin')
VERSION_SOURCE_FILE: Final[str] = r'lib\version.py'


def set_version() -> str:
    with open('pyproject.toml', 'r') as f:
        contents: str = f.read()
        version: str = re.search(r'^version = "([\d\.]+)"', contents, re.MULTILINE).group(1)
    FileUtil.str_to_file(VERSION_SOURCE_FILE, f'VERSION: str = "{version}"\n')
    return version


if __name__ == '__main__':
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
    FileUtil.copy('config.ini', DIST_DIR)
    FileUtil.copy('README.md', DIST_DIR)
    os.makedirs(BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part0'), BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part1'), BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part2'), BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part3'), BIN_DIR)
    FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part4'), BIN_DIR)
    directory: str = os.path.join('dist', 'bfv-hacker-checker')
    dest_zip: str = os.path.join('dist', f'bfv-hacker-checker_{version.replace(".", "_")}.zip')
    FileUtil.zip(directory, dest_zip)
