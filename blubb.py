from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = QtWebEngineWidgets.QWebEngineView(self)
        self.setCentralWidget(self.view)

        # Set up a timer to change the URL every 3 seconds
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.change_url)
        self.timer.start(3000)  # milliseconds

    def change_url(self):
        # Generate a new URL
        url = QtCore.QUrl('https://www.example.com')
        query = QtCore.QUrlQuery()
        query.addQueryItem('time', QtCore.QTime.currentTime().toString())
        url.setQuery(query)

        # Load the new URL

        print('dsadas', url)
        self.view.load(url)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
