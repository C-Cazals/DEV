#!/usr/bin/python
# -*- coding: utf-8 

import sys
from PySide.QtGui import *
from PySide.QtCore import *

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Ma fenetre")
        self.show()

    def mousePressEvent(self,event):
        print("appui souris")

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
fen = Fenetre()
app.exec_()