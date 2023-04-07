from PyQt5.QtCore import pyqtSignal, QObject
from pynput import keyboard, mouse
from pynput.keyboard import Key
from pynput.mouse import Button

from service.ConfigService import ConfigService
from service.LoggingService import LoggingService
from base.common import PyQtSignal
from thread.BaseThread import BaseThread


class UserInputListenerThread(BaseThread):
    __signal_event: PyQtSignal = pyqtSignal(int, int)

    def __init__(self, parent: QObject, config: ConfigService, logger: LoggingService):
        super().__init__(parent, config, logger)
        self.__is_key_pressed: bool = False
        self.__keyboard_listener: keyboard.Listener = keyboard.Listener(
            on_press=self.__on_key_press,
            on_release=self.__on_key_release
        )
        self.__mouse_listener: mouse.Listener = mouse.Listener(on_click=self.__on_mouse_click)

    @property
    def signal_event(self) -> PyQtSignal:
        return self.__signal_event

    def run(self) -> None:
        self.__keyboard_listener.start()
        self.__mouse_listener.start()

    def __on_mouse_click(self, x: int, y: int, button: Button, pressed: bool):
        if pressed and button == mouse.Button.left:
            if self.__is_key_pressed:
                self.signal_event.emit(x, y)

    def __on_key_press(self, key):
        if isinstance(key, Key):
            if key.name == self._config.hotkey:
                if not self.__is_key_pressed:
                    self.__is_key_pressed = True

    def __on_key_release(self, key):
        if isinstance(key, Key):
            if key.name == self._config.hotkey:
                self.__is_key_pressed = False
