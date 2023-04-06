from typing import Type

from injector import inject

from lib.Config import Config
from lib.Logger import Logger
from lib.ui.AbstractBaseWindow import AbstractBaseWindow
from lib.ui_generated.Ui_DebugWindow import Ui_DebugWindow


class DebugWindow(AbstractBaseWindow[Ui_DebugWindow]):
    @inject
    def __init__(self, config: Config, logger: Logger):
        super().__init__(config, logger)

    def _init_ui(self):
        pass

    def _get_ui(self) -> Type[Ui_DebugWindow]:
        return Ui_DebugWindow
