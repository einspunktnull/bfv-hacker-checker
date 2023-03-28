import os.path
import sys
from configparser import ConfigParser
from os.path import expanduser
from typing import Final

from PyQt5.QtWidgets import QApplication

from lib.Widget import Widget

if __name__ == '__main__':
    config: ConfigParser = ConfigParser()
    config.read('config.ini')

    app: QApplication = QApplication(sys.argv)
    gui: Widget = Widget(
        url=config.get('app', 'url'),
        key=config.get('user', 'key'),
        default_player=config.get('user', 'default_player'),
        data_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    )
    gui.show()
    sys.exit(app.exec_())
