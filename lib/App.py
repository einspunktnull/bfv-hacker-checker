import os
from datetime import datetime

from PyQt5.QtWidgets import QApplication
from pynput import mouse, keyboard
from pynput.mouse import Button

from lib.MainWindow import MainWindow
from lib.Util import Util


class App:
    def __init__(self, name: str, icon_path: str, url: str, key: str, default_player: str, data_dir: str):
        self.__url: str = url
        self.__key: str = key
        self.__default_player: str = default_player
        self.__data_dir: str = data_dir
        self.__qapp: QApplication = QApplication([])
        self.__main_window: MainWindow = MainWindow(name, icon_path)
        self.__is_key_pressed: bool = False
        self.__is_busy: bool = False

    def run(self) -> int:
        keyboard_listener: keyboard.Listener = keyboard.Listener(
            on_press=self.__on_key_press,
            on_release=self.__on_key_release
        )
        keyboard_listener.start()
        mouse_listener: mouse.Listener = mouse.Listener(on_click=self.__on_mouse_click)
        mouse_listener.start()
        self.__main_window.show()
        # initial_url: str = f'{self.__url}{self.__default_player}'
        # self.__main_window.call_url(initial_url)
        code: int = self.__qapp.exec_()
        return code

    def __on_mouse_click(self, x: int, y: int, button: Button, pressed: bool):
        if pressed and button == mouse.Button.left:
            if not self.__is_busy and self.__is_key_pressed:
                self.__check_it(x, y)

    def __on_key_press(self, key):
        if key == keyboard.Key.ctrl_l:
            if not self.__is_key_pressed:
                self.__is_key_pressed = True

    def __on_key_release(self, key):
        if key == keyboard.Key.ctrl_l:
            self.__is_key_pressed = False

    def __check_it(self, x: int, y: int):
        print(f'__check_it ({x},{y})')
        self.__is_busy = True
        try:
            # self.__create_screenshot()
            initial_url: str = f'{self.__url}{self.__default_player}'
            self.__main_window.call_url(initial_url)
        except Exception as e:
            self.__main_window.show_exception(e)
        self.__is_busy = False

    def __create_screenshot(self):
        now = datetime.now()
        date_time_string: str = now.strftime("%Y%m%d%H%M%S")
        img_save_path: str = f'{self.__data_dir}{os.path.sep}window_screenshot_{date_time_string}.png'
        Util.make_window_screenshot('Battlefield™ V', img_save_path)
