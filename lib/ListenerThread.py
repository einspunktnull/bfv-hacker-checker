from typing import Callable

from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard, mouse
from pynput.mouse import Button


class ListenerThread(QThread):
    __signal: pyqtSignal = pyqtSignal(int, int)

    def __init__(self, thread_fct: Callable):
        super().__init__()
        self.__signal.connect(thread_fct)
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
                self.__signal.emit(x, y)

    def __on_key_press(self, key):
        if key == keyboard.Key.ctrl_l:
            if not self.__is_key_pressed:
                self.__is_key_pressed = True

    def __on_key_release(self, key):
        if key == keyboard.Key.ctrl_l:
            self.__is_key_pressed = False
