from typing import Optional

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QLabel, QMainWindow


class Widget(QMainWindow):
    def __init__(self, url: str, key: str, default_player: str, data_dir: str):
        super().__init__()
        self.__url: str = url
        self.__key: str = key
        self.__default_player: str = default_player
        self.__data_dir: str = data_dir
        self.__lbl: Optional[QLabel] = None
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon("res/icon.png"))
        # Set the window size and title
        self.setGeometry(0, 0, 600, 420)
        self.setWindowTitle('Battlefield V Hacker Checker')

        view = QWebEngineView()
        view.setUrl(QUrl(f'{self.__url}{self.__default_player}'))
        self.setCentralWidget(view)

        # self.__lbl = QLabel(f'{self.__key} {self.__data_dir}', self)
        # self.__lbl.move(0, 0)

        # btn = QPushButton('Click me!', self)
        # btn.setToolTip('Click to update the label')
        # btn.move(50, 50)
        # btn.clicked.connect(self.updateLabel)

        self.show()

    def updateLabel(self):
        self.lbl.setText('Button clicked!')
