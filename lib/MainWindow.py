from typing import Optional, Dict, Any

from PyQt5.QtCore import QUrl, Qt, QUrlQuery
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, window_title: str, icon_path: str):
        super().__init__()
        self.__window_title: str = window_title
        self.__icon_path: str = icon_path
        self.__web_View: QWebEngineView = QWebEngineView()
        self.__msg_View: QLabel = QLabel()
        self.setWindowTitle(self.__window_title)
        self.setWindowIcon(QIcon(self.__icon_path))
        self.setGeometry(0, 0, 600, 420)
        self.setCentralWidget(self.__web_View)

    def call_url(self, url: str, query_params: Dict[str, Any] = None):
        if query_params is None:
            query_params = {}
        url_: QUrl = QUrl(url)
        query = QUrlQuery()
        for key, value in query_params.items():
            query.addQueryItem(key, value)
        url_.setQuery(query)
        self.__web_View.load(url_)

    @staticmethod
    def show_exception(e: Exception):
        print(e)
