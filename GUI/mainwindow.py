from PyQt5.QtWidgets import QPushButton, QToolTip, QFileDialog, QMainWindow, QAction, QWidget, QLabel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication
from dev.importdata import ImportData
from GUI.toolbar import ToolBar
import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        toolbar = ToolBar(self)
        
        self.resize(640, 480)
        self.move(0,0)

        self.setWindowTitle('CSTpy')
        self.show()

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if fname:
            pass

    def save_file(self):
        fname = QFileDialog.getSaveFileName(self, 'Open file', '/home')[0]
        if fname:
            pass
        
    def import_data(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if fname:
            im = ImportData(self, fname)     
            im.show()  
            



