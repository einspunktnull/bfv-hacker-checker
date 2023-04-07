import sys

import qdarktheme
from PyQt5.QtWidgets import QApplication
from injector import inject

from service.ConfigService import ConfigService


class QApplicationWrap:
    @inject
    def __init__(
            self,
            config: ConfigService
    ):
        if config.theme != 'none':
            qdarktheme.enable_hi_dpi()
        self.__qapp: QApplication = QApplication(sys.argv)
        if config.theme != 'none':
            qdarktheme.setup_theme(config.theme)

    def exec_(self) -> int:
        return self.__qapp.exec_()

    def exit(self, exit_code: int) -> None:
        self.__qapp.exit(exit_code)
