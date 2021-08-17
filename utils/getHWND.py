import psutil
import win32gui
import win32process

def getHWNDbyExeName(exeName):
    pid = next(item for item in psutil.process_iter() if item.name() == exeName).pid
    print('pid = ', pid)
    return getHWNDbyPID(pid)

def getHWNDbyPID(pid):
    def enum_window_callback(hwnd, pid):
        tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid == current_pid and win32gui.IsWindowVisible(hwnd):
            windows.append(hwnd)

    windows = []

    win32gui.EnumWindows(enum_window_callback, pid)

    # Выводим заголовки всех полученных окон
    windownames = [win32gui.GetWindowText(item) for item in windows]
    print('windownames = ', windownames)

    return getHWNDbyWindowName(windownames[0])

def getHWNDbyWindowName(windowname):
    hwnd = win32gui.FindWindow(None, windowname)
    print('hwnd = ', hwnd)

    return hwnd