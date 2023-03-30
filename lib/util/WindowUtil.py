import win32con
import win32gui

from lib.types import BoundingBox


class WindowUtil:

    @staticmethod
    def to_foreground_by_title(window_title: str):
        window_handle = win32gui.FindWindow(None, window_title)
        return WindowUtil.to_foreground_by_handle(window_handle)

    @staticmethod
    def to_foreground_by_handle(window_handle):
        win32gui.ShowWindow(window_handle, win32con.SW_NORMAL)
        try:
            win32gui.SetForegroundWindow(window_handle)
        except:
            pass
        return window_handle

    @staticmethod
    def get_bbox_by_title(window_title: str) -> BoundingBox:
        window_handle = win32gui.FindWindow(None, window_title)
        return WindowUtil.get_bbox_by_handle(window_handle)

    @staticmethod
    def get_bbox_by_handle(window_handle) -> BoundingBox:
        return win32gui.GetWindowRect(window_handle)
