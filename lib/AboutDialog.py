from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from injector import inject

from lib.Config import Config


class AboutDialog(QDialog):

    @inject
    def __init__(self, config: Config, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel(config.app_name)
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setFixedSize(200, 200)
        pixmap = QPixmap(config.icon_path)
        pixmap = pixmap.scaled(logo.size(), aspectRatioMode=Qt.KeepAspectRatio)
        logo.setPixmap(pixmap)
        layout.addWidget(logo)

        layout.addWidget(QLabel(f"Version {config.version}"))
        link = QLabel(self)
        link.setTextFormat(Qt.RichText)
        link.setText(
            '<a href="https://github.com/einspunktnull/bfv-hacker-checker">https://github.com/einspunktnull/bfv-hacker-checker</a>')
        link.linkActivated.connect(self.__on_link_clicked)
        layout.addWidget(link)

        layout.addWidget(self.buttonBox)

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        self.setLayout(layout)

    def __on_link_clicked(self, url):
        # Open the clicked URL in the default web browser
        QDesktopServices.openUrl(QUrl(url))
