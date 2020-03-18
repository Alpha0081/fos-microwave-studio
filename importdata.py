from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .analyzedata import AnalyzeData

import matplotlib.pyplot as plt

class ImportData(QWidget):
    def __init__(self, parent, name):
        super(QWidget, self).__init__(parent, Qt.Window)
        

        self.setWindowTitle('Import')
        self.resize(600, 550)
        
        self.tabs = QTabWidget(self)
        
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label1.resize(600, 512)
        self.label2.resize(600, 512)
        
        self.textbox = QLineEdit(self)
        self.textbox.setText("90")
        self.textbox.resize(50, 20)
        self.textbox.move(0, 520)
        self.tabs.resize(600, 512)
        
        self.tabs.addTab(self.label1,"Normal")
        self.tabs.addTab(self.label2,"Polar")
        
        self.picture1 = AnalyzeData(self, name)
        self.picture1.analyze(90)
        self.picture1.show(0, 'normal.png')
        self.picture2 = AnalyzeData(self, name)
        self.picture2.analyze(90)
        self.picture2.show(1, 'polar.png')
        
        
        pixmap1 = QPixmap('normal.png')
        pixmap2 = QPixmap('polar.png')
        
        
        self.label1.setPixmap(pixmap1)
        self.label2.setPixmap(pixmap2)

        btnsave = QPushButton('Save', self)
        btn = QPushButton('OK', self)
        
        btnsave.resize(70, 20)
        btn.resize(70, 20)
        
        btnsave.move(450, 520)
        
        btn.move(60, 520)
        btn.clicked.connect(self.pr)

    def pr(self):
        phi = int(self.textbox.text())
        phi = phi - (phi%5) if phi >= -85 else -90
        self.textbox.setText(str(phi))
        self.picture1.analyze(phi)
        self.picture2.analyze(phi)
        self.picture2.show(1, 'polar.png')
        self.picture1.show(0, 'normal.png')
        pixmap1 = QPixmap('normal.png')
        pixmap2 = QPixmap('polar.png')
        
        
        self.label1.setPixmap(pixmap1)
        self.label2.setPixmap(pixmap2)

        print(self.textbox.text())
