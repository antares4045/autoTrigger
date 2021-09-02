from gui.MainShell import MainShell

from PyQt5 import QtWidgets
import sys


app = QtWidgets.QApplication(sys.argv)

w = MainShell(  
                exe_name='PortalWars-Win64-Shipping.exe', 
                pause_hotkey=["7"],
                closeProgramm_hotey=["PAUSE_BREAK"],
                rect={"x":930, "y":510, "width":30, "height":30},
                points=[[26, 29], [0,0], [2, 29], [29, 29]],
                isGoodPixel=lambda color: color[2] < 0.1 and color[1] < 0.1 and color[0] > 0.9
            )

w.show()
sys.exit(app.exec_())
