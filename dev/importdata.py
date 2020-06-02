from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QLineEdit, QPushButton, QCheckBox, QListWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from .analyzedata import AnalyzeData
from os import system

class ImportData(QWidget):
    def __init__(self, parent, name):
        super(QWidget, self).__init__(parent, Qt.Window)
        
        self.setWindowTitle('Import')
        self.setFixedSize(850, 512)
        self.move(0, 50)
        
        self.tabs = QTabWidget(self)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label1.resize(600, 512)
        self.label2.resize(600, 512)
        self.tabs.resize(600, 512)
        self.tabs.addTab(self.label1, "Normal")
        self.tabs.addTab(self.label2, "Polar")
        
        self.textbox = QLineEdit(self)
        self.textbox.setText("-90")
        self.textbox.resize(31, 22)
        self.textbox.move(640, 20)
        self.textbox.setFont(QFont("Calibri", 10))
        self.textbox.setMaxLength(3)
        
        self.data = AnalyzeData(self, name)

        btnsave = QPushButton('Save', self)
        btnsave.resize(93, 28)
        btnsave.move(740, 470)
        btnsave.setFont(QFont("Calibri", 10))
        
        btn = QPushButton('Analyze', self)
        btn.resize(93, 28)
        btn.move(620, 470)
        btn.setFont(QFont("Calibri", 10))
        btn.clicked.connect(self.analyze_button_clicked)        

        self.interpolation = QCheckBox("Use interpolation", self)
        self.interpolation.resize(121, 20)
        self.interpolation.move(690, 20)
        self.interpolation.setFont(QFont("Times", 8))

        phi = QLabel('φ :', self)
        phi.resize(31, 21)
        phi.move(610, 20)
        phi.setFont(QFont("Times", 10))
        
        degrees = QLabel('°', self)
        degrees.resize(16, 16)
        degrees.move(672, 20)
        degrees.setFont(QFont("Calibri", 10))

        self.direction = QLabel('', self)
        self.direction.resize(61, 21)
        self.direction.move(690, 50)
        self.direction.setFont(QFont("Calibri", 10))
        
        max_direction = QLabel("Direction :", self)
        max_direction.resize(81, 21)
        max_direction.move(610, 50)
        max_direction.setFont(QFont("Calibri", 10))
        
        zero = QLabel("Zeros :", self)
        zero.setFont(QFont("Calibri", 10))
        zero.resize(55, 16)
        zero.move(610, 110)
        
        self.zero = QListWidget(self)
        self.zero.setFont(QFont("Calibri", 10))
        self.zero.resize(91, 81)
        self.zero.move(670, 80)

        self.main_length = QLabel('', self)
        self.main_length.setFont(QFont("Calibri", 10))
        self.main_length.resize(51, 16)
        self.main_length.move(640, 170)
        
        theta = QLabel('θ₀ :', self)
        theta.setFont(QFont("Calibri", 10))
        theta.move(610, 170)
        theta.resize(31, 16)

        theta3dB = QLabel('θ₀̣₅:', self)
        theta3dB.setFont(QFont("Calibri", 10))
        theta3dB.move(610, 200)
        theta3dB.resize(31, 16)

        self.main_length_3dB = QLabel('', self)
        self.main_length_3dB.setFont(QFont("Calibri", 10))
        self.main_length_3dB.move(640, 200)
        self.main_length_3dB.resize(51, 16)

    def analyze_button_clicked(self):
        self.zero.clear()
        phi = int(self.textbox.text())
        phi = phi - (phi % 5)
        if phi > 90:
            phi = 90
        if phi < -90:
            phi = -90
        self.textbox.setText(str(phi))
        if self.interpolation.checkState():
            self.data.delta = 1
        else:
            self.data.delta = 0
        self.data.analyze(phi)
        for phi in self.data.get_zeros():
            self.zero.addItem(phi)
        self.data.show('normal.png', 0)
        self.data.show('polar.png', 1)
        pixmap1 = QPixmap('normal.png')
        pixmap2 = QPixmap('polar.png')
        system('del normal.png')
        system('del polar.png')
        self.label1.setPixmap(pixmap1)
        self.label2.setPixmap(pixmap2)
        self.main_length.setText(str(self.data.get_length()) + "°")
        self.main_length_3dB.setText(str(self.data.get_length_3dB()) + "°")
        self.direction.setText(str(int(self.data.get_direction_of_maximum()[0])) + "°")
