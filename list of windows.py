import psutil
import win32gui
import win32process

def enum_window_callback(hwnd, pid):
        tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid == current_pid and win32gui.IsWindowVisible(hwnd):
            windows.append(hwnd)

for process in psutil.process_iter():
    #exeName = process.name()
    pid = process.pid

    windows = []

    win32gui.EnumWindows(enum_window_callback, pid)

    windownames = [win32gui.GetWindowText(item) for item in windows]
    
    if len(windownames):
        exeName = process.name()
        for windowName in windownames:
            hwnd = win32gui.FindWindow(None, windowName)
            print(f'"{exeName}" - "{windowName}" - "{hwnd}"')