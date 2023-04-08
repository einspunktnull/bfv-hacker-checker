from typing import List

from base.common import (
    BoundingBox,
    InvalidWindowHandleException,
    UnsupportedOsException,
    OS_PLATFORM,
    OS_PLATFORM_WINDOWS,
    OS_PLATFORM_LINUX
)

if OS_PLATFORM == OS_PLATFORM_WINDOWS:
    import win32gui
    import pywintypes
    import win32con
elif OS_PLATFORM == OS_PLATFORM_LINUX:
    from ewmh import EWMH
else:
    raise UnsupportedOsException()


class WindowUtil:

    @staticmethod
    def to_foreground_by_title(window_title: str) -> object:
        if OS_PLATFORM == OS_PLATFORM_WINDOWS:
            window_handle = win32gui.FindWindow(None, window_title)
        elif OS_PLATFORM == OS_PLATFORM_LINUX:
            window_handle = WindowUtil.get_window_emwh(window_title)
        else:
            raise UnsupportedOsException()
        if window_handle is None:
            raise InvalidWindowHandleException('no window found')
        return WindowUtil.to_foreground_by_handle(window_handle)

    @staticmethod
    def to_foreground_by_handle(window_handle) -> object:
        if OS_PLATFORM == OS_PLATFORM_WINDOWS:
            win32gui.ShowWindow(window_handle, win32con.SW_NORMAL)
            try:
                win32gui.SetForegroundWindow(window_handle)
            except pywintypes.error as err:
                if err.winerror:
                    raise InvalidWindowHandleException(err)
            return window_handle
        elif OS_PLATFORM == OS_PLATFORM_LINUX:
            ew = EWMH()
            ew.setActiveWindow(window_handle, EWMH.WM_TAKE_FOCUS)
            ew.display.flush()
        else:
            raise UnsupportedOsException()

    @staticmethod
    def get_bbox_by_title(window_title: str) -> BoundingBox:
        if OS_PLATFORM == OS_PLATFORM_WINDOWS:
            window_handle = win32gui.FindWindow(None, window_title)
            return WindowUtil.get_bbox_by_handle(window_handle)
        elif OS_PLATFORM == OS_PLATFORM_LINUX:
            raise NotImplementedError()
        else:
            raise UnsupportedOsException()

    @staticmethod
    def get_bbox_by_handle(window_handle) -> BoundingBox:
        if OS_PLATFORM == OS_PLATFORM_WINDOWS:
            return win32gui.GetWindowRect(window_handle)
        elif OS_PLATFORM == OS_PLATFORM_LINUX:
            raise NotImplementedError()
        else:
            raise UnsupportedOsException()

    @staticmethod
    def get_window_emwh(name_or_class: str, ignore_case: bool = True) -> object:
        if OS_PLATFORM != OS_PLATFORM_LINUX:
            raise UnsupportedOsException()
        instance: EWMH = EWMH()
        windows = instance.getClientList()
        for window in windows:
            name = str(window.get_wm_name())
            clazz = window.get_wm_class()
            names: List[str] = [name, *clazz]
            names = list(dict.fromkeys(names))
            for name in names:
                name_for_comp: str = name.lower() if ignore_case else name
                name_or_class_for_comp: str = name_or_class.lower() if ignore_case else name_or_class
                if name_for_comp == name_or_class_for_comp:
                    return window
