from datetime import datetime

import win32con
import win32gui
from PIL import ImageGrab


class Util:

    @staticmethod
    def make_window_screenshot(window_title: str, img_save_path: str = None) -> str:
        if img_save_path is None:
            now = datetime.now()
            date_time_string: str = now.strftime("%Y%m%d%H%M%S")
            img_save_path = f'window_screenshot_{date_time_string}.png'
        window_handle = win32gui.FindWindow(None, window_title)
        rect = win32gui.GetWindowRect(window_handle)

        win32gui.ShowWindow(window_handle, win32con.SW_NORMAL)
        win32gui.SetForegroundWindow(window_handle)
        game_screen = ImageGrab.grab(bbox=rect)
        game_screen.save(img_save_path)
        return img_save_path
