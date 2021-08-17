import win32api
import win32con

from time import sleep
from time import time

STANDARD_DELAY=0.01

DEFAULT_MAP = {
    "UP": win32con.VK_UP,
    "DOWN": win32con.VK_DOWN,
    "LEFT": win32con.VK_LEFT,
    "RIGHT": win32con.VK_RIGHT,
    
    " ": win32con.VK_SPACE,
    
    
    "F1" : win32con.VK_F1,
    "F2" : win32con.VK_F2,
    "F3" : win32con.VK_F3,
    "F4" : win32con.VK_F4,
    "F5" : win32con.VK_F5,
    "F6" : win32con.VK_F6,
    "F7" : win32con.VK_F7,
    "F8" : win32con.VK_F8,
    "F9" : win32con.VK_F9,
    "F10" : win32con.VK_F10,
    "F11" : win32con.VK_F11,
    "F12" : win32con.VK_F12,
    
    "NUM0" : win32con.VK_NUMPAD0,
    "NUM1" : win32con.VK_NUMPAD1,
    "NUM2" : win32con.VK_NUMPAD2,
    "NUM3" : win32con.VK_NUMPAD3,
    "NUM4" : win32con.VK_NUMPAD4,
    "NUM5" : win32con.VK_NUMPAD5,
    "NUM6" : win32con.VK_NUMPAD6,
    "NUM7" : win32con.VK_NUMPAD7,
    "NUM8" : win32con.VK_NUMPAD8,
    "NUM9" : win32con.VK_NUMPAD9,
    
    "L_WIN" : win32con.VK_LWIN,
    "R_WIN" : win32con.VK_RWIN,
    
    "LMB" : win32con.VK_LBUTTON,
    "RMB" : win32con.VK_RBUTTON,
    "MMB" : win32con.VK_MBUTTON,

    "SHIFT" : win32con.VK_SHIFT,
    "CTRL" : win32con.VK_CONTROL,
    "ALT" : win32con.VK_MENU,

    "ENTER": win32con.VK_RETURN,
    "CAPS_LOCK" : win32con.VK_CAPITAL,
    "BACKSPASE" : win32con.VK_BACK,
    "TAB" : win32con.VK_TAB,
    "ESC" : win32con.VK_ESCAPE,

    "PAUSE_BREAK" :win32con.VK_PAUSE,
    "PAGE_UP" : win32con.VK_PRIOR,
    "PAGE_DOWN" : win32con.VK_NEXT,
    "END" : win32con.VK_END, 
    "HOME" : win32con.VK_HOME, 
    "INSERT" : win32con.VK_INSERT, 
    "DELETE" : win32con.VK_DELETE, 

    ';' : 0xBA, #win32con.VK_OEM_1,
    '/' : 0xBF, #win32con.VK_OEM_2,
    '~' : 0xC0, #win32con.VK_OEM_3,    
    '[' : 0xDB, #win32con.VK_OEM_4,
    '|' : 0xDC, #win32con.VK_OEM_5,
    ']' : 0xDD,#win32con.VK_OEM_6,
    '"' : 0xDE, #win32con.VK_OEM_7,    
    
    "RMB" : 0x02,
    "LMB" : 0x01,
    "MMB" : 0x04,

}

for i in range(ord('A'), 1+ ord('Z')):
    DEFAULT_MAP[chr(i)] = i
    
for i in range(10):
    DEFAULT_MAP[str(i)] = i + 0x30



class keyboardBeholder:
    DEPRECATED_PARAM = 0
    def __init__(self, btn_map=DEFAULT_MAP, listen_list=list(DEFAULT_MAP.keys())):
        self._ignoreNow = set()
        self.setBtnMap(btn_map)
        self.listen_list=listen_list
        
    def setBtnMap(self, btn_map=DEFAULT_MAP):
        self._map = {}
        for k in btn_map:
            v = btn_map[k]
            if isinstance(v, str):
                v = ord(v)
            self._map[k] = v

    def getKeys(self):
        result = {}
        for k in self.listen_list:
            v = self._map[k]
            
            keyState = win32api.GetAsyncKeyState(v)
            if keyState != 0:
                if not(v in self._ignoreNow):
                    result[k] = keyState == 1

        self._ignoreNow = set()
        
        return result
    
    def useButton(self, vk, send=win32con.KEYEVENTF_EXTENDEDKEY, down=True, up=True):
        if down:
            win32api.keybd_event(vk, keyboardBeholder.DEPRECATED_PARAM, send, 0)
            
        if up:
            win32api.keybd_event(vk, keyboardBeholder.DEPRECATED_PARAM, send | win32con.KEYEVENTF_KEYUP , 0)

        if up or down:
            self._ignoreNow.add(vk)
    

    def createHotkey(self, delay=STANDARD_DELAY):
        self.getKeys()
        res = set()
        
        curr = {}
        while not curr:
            curr = self.getKeys()
            sleep(delay)
        
        while curr:
            prev = set(curr.keys())
            #print('curr:', *prev)
            if prev - res:
                if res - prev:
                    res = prev
                else:
                    res |= prev
                print(*res, sep=' + ')
            curr = self.getKeys()
            sleep(delay)
        
        
        print('result: ', ' + '.join(map(lambda x: '['+x+']', res)))
        return self.namesToVK(res)
    
    #'WWAE'
    def namesToVK(self, names, finaliser=list):
        return finaliser(map(lambda name: self._map[name], names))

    def useHotkey(self, hotkey):
        for code in hotkey:
            self.useButton(code, up=False)
        sleep(STANDARD_DELAY)
        for code in hotkey:
            self.useButton(code, down=False)

    def writeLine(self, line):
        for code in line:
            self.useButton(code)
            sleep(STANDARD_DELAY)

    def hotkeyChain(self, chain):
        for hotkey in chain:
            self.useHotkey(hotkey)
            sleep(STANDARD_DELAY)
        
    
