from PyQt5.QtWidgets import (QWidget, QScrollArea , QVBoxLayout, QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from threading import Thread
from PyQt5.QtWidgets import QDialog
import os
from playsound import playsound
from threading import Thread

from time import sleep
from time import time

import traceback
import sys
HOTKEY_REPEAT_DELAY = 0.5

from utils.beholder import keyboardBeholder
from utils.getHWND import getHWNDbyExeName as getWID

CURRENT_DIRECTORY = os.path.dirname(__file__)

SOUND_DIRECTORY = os.path.normpath("C:/Windows/Media/")
sound_start = "Windows Unlock.wav"
sound_pause = "Windows Proximity Notification.wav"
sound_finish = "Windows Message Nudge.wav"
sound_error = "Windows Foreground.wav"



def playSound(name):
    Thread(target=playsound, args=(os.path.join(SOUND_DIRECTORY, name),)).start()

def mainLoop(shell,exe_name, rect, points, isGoodPixel, pause_hotkey, closeProgramm_hotey):
    try:
        beholder = keyboardBeholder()
        beholder.listen_list = list(set(pause_hotkey) | set(closeProgramm_hotey))

        enbbleSwitch = beholder.namesToVK(pause_hotkey, finaliser=set)
        offSwithch = beholder.namesToVK(closeProgramm_hotey, finaliser=set)

        shot = beholder.namesToVK(["LMB"])
        lasthotkeyTiming = time()

        wid = None
        screen = None

        while shell and shell.running:
            sleep(0.001)
            keys = beholder.namesToVK(beholder.getKeys().keys(), finaliser=set)
            if not (offSwithch - keys):
                playSound(sound_finish)
                shell.running = False
                shell.close()
                shell = None
            else:
                if not (enbbleSwitch - keys):
                    now = time()
                    if now - lasthotkeyTiming > HOTKEY_REPEAT_DELAY:
                        lasthotkeyTiming = now
                        if not shell.beholderEnabled:
                            if not wid:
                                wid = getWID(exe_name)
                                screen = QtWidgets.QApplication.primaryScreen()
                                
                            shell.setBeholderEnabled(True)
                            playSound(sound_start)
                        else:
                            shell.setBeholderEnabled(False)
                            playSound(sound_pause)
                
                if shell.beholderEnabled:
                    img = screen.grabWindow(wid, **rect).toImage()
                    for coord in points:
                        color = QColor(img.pixel(*coord)).getRgbF()
                        isGood = isGoodPixel(color)
                        if isGood:
                            Thread(target=lambda:beholder.writeLine(shot)).start()
                            break
                # else:
                #     sleep(0.001)
                    
    except Exception as error:
        playSound(sound_error)
        err_info = sys.exc_info()

        answer = traceback.format_exception(*err_info)

        shell.printError('\n'.join(map(lambda line: f"{line}", answer)))



class MainShell(QWidget):
    def __init__(self, exe_name, rect, points, isGoodPixel, pause_hotkey=["F1"],closeProgramm_hotey=["PAUSE_BREAK"],):
        super().__init__()
    
        self.running = True
        self.beholderEnabled = False
        self.setBeholderEnabled(False)
        self.beeholdThread = Thread(target=mainLoop, args=(self,exe_name, rect, points, isGoodPixel, pause_hotkey, closeProgramm_hotey))
        self.beeholdThread.start()

        layout = QVBoxLayout()

        texts = ["Окно длжно быть расположено на одном экране с игрой", 
        "Игра должна быть в оконном режиме",
        f"{'+'.join(pause_hotkey)} для включения/паузы", 
        f"{'+'.join(closeProgramm_hotey)} для выключения"]
        
        for text in texts:
            label = QLabel()
            label.setText(text)
            layout.addWidget(label)

        self.errorLablel = QLabel()
        self.errorLablel.setStyleSheet("QLabel { color : red; }");
        layout.addWidget(self.errorLablel)
        self.setLayout(layout)

    def setBeholderEnabled(self, enabled) -> None:
        self.beholderEnabled = enabled
        self.setWindowTitle("Активно" if enabled else "Приостановлено")

    def closeEvent(self, event):
        self.running = False

    def printError(self, text):
        self.errorLablel.setText(text)