from gui.MainShell import MainShell

from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets
import sys

EXE_NAME = 'PortalWars-Win64-Shipping.exe'


app = QtWidgets.QApplication(sys.argv)

w = MainShell(  exe_name=EXE_NAME, 
                pause_hotkey=["7"],
                closeProgramm_hotey=["CTRL", "HOME"],
                rect={"x":930, "y":510, "width":30, "height":30},
                points=[[26, 29], [0,0], [2, 29], [29, 29]],
                isGoodPixel=lambda color: color[2] < 0.1 and color[1] < 0.1 and color[0] > 0.9
                
            )

w.show()
sys.exit(app.exec_())
