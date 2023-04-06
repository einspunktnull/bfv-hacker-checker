from typing import Callable

from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard, mouse
from pynput.keyboard import Key
from pynput.mouse import Button

from lib.common import PyQtSignal


class UserInputListenerThread(QThread):
    __EVENT_SIGNAL: PyQtSignal = pyqtSignal(int, int)

    def __init__(self, key: str, event_fct: Callable):
        super().__init__()
        self.__key: str = key
        self.__EVENT_SIGNAL.connect(event_fct)
        self.__keyboard_listener: keyboard.Listener = keyboard.Listener(
            on_press=self.__on_key_press,
            on_release=self.__on_key_release
        )
        self.__keyboard_listener.start()
        self.__mouse_listener: mouse.Listener = mouse.Listener(on_click=self.__on_mouse_click)
        self.__mouse_listener.start()
        self.__is_key_pressed: bool = False

    def __on_mouse_click(self, x: int, y: int, button: Button, pressed: bool):
        if pressed and button == mouse.Button.left:
            if self.__is_key_pressed:
                self.__EVENT_SIGNAL.emit(x, y)

    def __on_key_press(self, key):
        if isinstance(key, Key):
            if key.name == self.__key:
                if not self.__is_key_pressed:
                    self.__is_key_pressed = True

    def __on_key_release(self, key):
        if isinstance(key, Key):
            if key.name == self.__key:
                self.__is_key_pressed = False
