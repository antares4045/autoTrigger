from PyQt5.QtWidgets import (QWidget, QScrollArea , QVBoxLayout, QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from threading import Thread
from PyQt5.QtWidgets import QDialog
import os
from threading import Thread

from utils.playsound import playsound

from time import sleep
from time import time

import traceback
import sys
HOTKEY_REPEAT_DELAY = 0.5

from utils.beholder import keyboardBeholder
from utils.getHWND import getHWNDbyExeName as getWID

CURRENT_DIRECTORY = os.path.dirname(__file__)

SOUND_DIRECTORY = os.path.normpath(os.path.relpath(
    os.path.join(
        CURRENT_DIRECTORY, '../assets'
    ), os.getcwd()))

sound_start = "au.wav"
sound_pause = "peep.wav"
sound_finish = "beep.wav"
sound_error = "bzzz.wav"



def playSound(name, blocking=False):
    playsound(os.path.join(SOUND_DIRECTORY, name), blocking=blocking)
    #Thread(target=playsound, args=(),)).start()

def mainLoop(shell,exe_name, rect, points, isGoodPixel, pause_hotkey, closeProgram_hotkey,savePic):
    try:
        beholder = keyboardBeholder()
        beholder.listen_list = list(set(pause_hotkey) | set(closeProgram_hotkey))

        enableSwitch = beholder.namesToVK(pause_hotkey, finaliser=set)
        offSwitch = beholder.namesToVK(closeProgram_hotkey, finaliser=set)

        shot = beholder.namesToVK(["LMB"])
        lasthotkeyTiming = time()

        wid = None
        screen = None

        while shell and shell.running:
            sleep(0.001)
            keys = beholder.namesToVK(beholder.getKeys().keys(), finaliser=set)
            if not (offSwitch - keys):
                playSound(sound_finish, blocking=True)
                shell.running = False
                shell.close()
                shell = None
            else:
                if not (enableSwitch - keys):
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
                    pic = screen.grabWindow(wid, **rect)
                    if savePic:
                        pic.save('shot.jpg', 'jpg')
                    img = pic.toImage()
                    for coord in points:
                        color = QColor(img.pixel(*coord)).getRgbF()
                        isGood = isGoodPixel(color)
                        if isGood:
                            Thread(target=lambda:beholder.writeLine(shot)).start()
                            break
                    
    except Exception as error:
        playSound(sound_error)
        err_info = sys.exc_info()

        answer = traceback.format_exception(*err_info)

        shell.printError('\n'.join(map(lambda line: f"{line}", answer)))



class MainShell(QWidget):
    def __init__(self, exe_name, rect, points, isGoodPixel, pause_hotkey=["F1"],closeProgram_hotkey=["PAUSE_BREAK"],savePic=False):
        super().__init__()
    
        self.running = True
        self.beholderEnabled = False
        self.setBeholderEnabled(False)
        self.beeholdThread = Thread(target=mainLoop, args=(self,exe_name, rect, points, isGoodPixel, pause_hotkey, closeProgram_hotkey, savePic))
        self.beeholdThread.start()

        layout = QVBoxLayout()

        texts = ["Окно длжно быть расположено на одном экране с игрой", 
        "Игра должна быть в оконном режиме",
        f"{'+'.join(pause_hotkey)} для включения/паузы", 
        f"{'+'.join(closeProgram_hotkey)} для выключения"]
        
        for text in texts:
            label = QLabel()
            label.setText(text)
            layout.addWidget(label)

        self.errorLabel = QLabel()
        self.errorLabel.setStyleSheet("QLabel { color : red; }");
        layout.addWidget(self.errorLabel)
        self.setLayout(layout)

    def setBeholderEnabled(self, enabled) -> None:
        self.beholderEnabled = enabled
        self.setWindowTitle("Активно" if enabled else "Приостановлено")

    def closeEvent(self, event):
        self.running = False

    def printError(self, text):
        self.errorLabel.setText(text)