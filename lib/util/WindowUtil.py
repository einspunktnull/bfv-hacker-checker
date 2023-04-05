import sys

from lib.types import BoundingBox, InvalidWindowHandleException, UnsupportedOsException

OS_PLATFORM: str = sys.platform
OS_PLATFORM_LINUX: str = "linux"
OS_PLATFORM_WINDOWS: str = "win32"

if OS_PLATFORM == OS_PLATFORM_WINDOWS:
    import win32gui
    import pywintypes
    import win32con
elif OS_PLATFORM == OS_PLATFORM_LINUX:
    import ewmh
else:
    raise UnsupportedOsException()


class WindowUtil:

    @staticmethod
    def to_foreground_by_title(window_title: str) -> object:
        window_handle: object = None
        if OS_PLATFORM == OS_PLATFORM_WINDOWS:
            window_handle = win32gui.FindWindow(None, window_title)
        elif OS_PLATFORM == OS_PLATFORM_LINUX:
            all_windows = ewmh.getClientList()
            for window in all_windows:
                if ewmh.getWmName(window) == window_title:
                    window_handle = window
                    break
        else:
            raise UnsupportedOsException()
        if not window_handle:
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
            ewmh.setActiveWindow(window_handle, ewmh.WM_TAKE_FOCUS)
            ewmh.display.flush()
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
