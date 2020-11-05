from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QLineEdit, QPushButton, QCheckBox, QListWidget, QFileDialog
from PyQt5.QtCore import Qt
from .config import config


class Setting(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent, Qt.Window)
        
        self.setWindowTitle('Settings')
        self.setFixedSize(850, 512)
        self.move(0, 100)
        
        self.tabs = QTabWidget(self)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label1.resize(600, 512)
        self.label2.resize(600, 512)
        self.tabs.resize(600, 512)
        self.tabs.addTab(self.label1, "General")
        self.tabs.addTab(self.label2, "Other")
