#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QApplication
from mainWindow import MainWindow
from PySide6.QtGui import QIcon

if __name__ == "__main__":
   app = QApplication([])
   
   app_icon = QIcon("resources\images\icons8-video-download-50.png") 
   app.setWindowIcon(app_icon)
   
   window = MainWindow()
   window.show()
   app.exec()