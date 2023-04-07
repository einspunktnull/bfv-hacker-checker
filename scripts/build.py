import os.path
import shutil
import subprocess
import sys
from typing import Final

sys.path.append('src')
from base.common import OS_PLATFORM_WINDOWS, OS_PLATFORM_LINUX
from set_version import set_version

from util.FileUtil import FileUtil

BASE_NAME: str = r"bfv-hacker-checker"
DIST_DIR: Final[str] = os.path.join('dist', BASE_NAME)
BIN_DIR: Final[str] = os.path.join(DIST_DIR, 'bin')

if __name__ == '__main__':
    debug: bool = len(sys.argv) >= 2 and sys.argv[1] == 'debug'
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    version: str = set_version()
    subprocess.run([
        'pyinstaller',
        '--windowed',
        '--noconfirm',
        '--onefile',
        f'--paths=src',
        f'--icon=res{os.path.sep}icon.png',
        f'--distpath={DIST_DIR}',
        f'--name={BASE_NAME}',
        f'src/main.py'
    ])
    FileUtil.copy('res', os.path.join(DIST_DIR, 'res'))
    if sys.platform == OS_PLATFORM_LINUX:
        FileUtil.copy('config.linux.ini', os.path.join(DIST_DIR, 'config.ini'))
    else:
        FileUtil.copy('config.release.ini', os.path.join(DIST_DIR, 'config.ini'))
    FileUtil.copy('README.md', DIST_DIR)
    if sys.platform == OS_PLATFORM_WINDOWS:
        os.makedirs(BIN_DIR)
        FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part0'), BIN_DIR)
        FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part1'), BIN_DIR)
        FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part2'), BIN_DIR)
        FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part3'), BIN_DIR)
        FileUtil.copy(os.path.join('bin', 'Tesseract-OCR.zip_part4'), BIN_DIR)
    directory: str = os.path.join('dist', BASE_NAME)
    dest_zip_name: str = f'bfv-hacker-checker_{version.replace(".", "_")}_{sys.platform}.zip'
    dest_zip: str = os.path.join('dist', dest_zip_name)
    FileUtil.zip(directory, dest_zip)
