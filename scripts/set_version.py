import os
import re
import sys

sys.path.append('src')

from util.FileUtil import FileUtil


def set_version() -> str:
    with open('pyproject.toml', 'r') as f:
        contents: str = f.read()
        version: str = re.search(r'^version = "([\d\.]+)"', contents, re.MULTILINE).group(1)
    FileUtil.str_to_file(f'src{os.path.sep}version.py', f'VERSION: str = "{version}"\n')
    return version


if __name__ == '__main__':
    set_version()
