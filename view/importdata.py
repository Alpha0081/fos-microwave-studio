from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QLineEdit, QPushButton, QCheckBox, QListWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QFont, QVector3D
from PyQt5.QtCore import Qt
from os import system
from sys import platform
from shutil import copyfile  
from pathlib import Path
from models.config import config
from viewmodels.importvm import Importvm
from viewmodels.plotcanvas import PlotCanvas
from viewmodels.plot3dcanvas import Plot3DCanvas


import matplotlib.pyplot as plt
from math import sin, cos, pi
import numpy as np



class ImportData(QWidget):
    def __init__(self, parent, name):
        font = config.font
        super().__init__(parent, Qt.Window)

        self.vm = Importvm(name)

        self.setWindowTitle('Import')
        self.setFixedSize(850, 512)
        self.move(0, 50)
        
        self.tabs = QTabWidget(self)

        self.graph1 = PlotCanvas(self, "normal")
        self.graph1.set_label_axes("θ","dB")

        
        self.graph2 = PlotCanvas(self, "polar")
        
                
        self.graph3d = Plot3DCanvas(self)
        
        self.graph3d.plot(self.vm._spherical_x, self.vm._spherical_y, self.vm._spherical_z)
        
        self.graph3d.resize(600, 512)
        self.graph1.resize(600, 512)
        self.graph2.resize(600, 512)

        self.tabs.resize(600, 512)
        self.tabs.addTab(self.graph1, "Normal")
        self.tabs.addTab(self.graph2, "Polar")
        self.tabs.addTab(self.graph3d, "3D View")
        
        self.textbox = QLineEdit(self)
        self.textbox.setText("0")
        self.textbox.resize(31, 22)
        self.textbox.move(640, 20)
        self.textbox.setFont(QFont(font, 12))
        self.textbox.setMaxLength(3)
        
        btnsave = QPushButton('Save', self)
        btnsave.resize(93, 28)
        btnsave.move(740, 470)
        btnsave.setFont(QFont(font, 12))
        btnsave.clicked.connect(self.save_button_clicked)
        
        btn = QPushButton('Analyze', self)
        btn.resize(93, 28)
        btn.move(620, 470)
        btn.setFont(QFont(font, 12))
        btn.clicked.connect(self.analyze_button_clicked)        

        phi = QLabel('φ :', self)
        phi.resize(31, 21)
        phi.move(610, 20)
        phi.setFont(QFont(font, 12))
        
        degrees = QLabel('°', self)
        degrees.resize(16, 16)
        degrees.move(672, 20)
        degrees.setFont(QFont(font, 12))

        self.direction = QLabel('', self)
        self.direction.resize(61, 21)
        self.direction.move(690, 50)
        self.direction.setFont(QFont(font, 12))
        
        max_direction = QLabel("Direction :", self)
        max_direction.resize(81, 21)
        max_direction.move(610, 50)
        max_direction.setFont(QFont(font, 12))
        zero = QLabel("Zeros :", self)
        zero.setFont(QFont(font, 12))
        zero.resize(55, 16)
        zero.move(610, 110)
        
        self.zero = QListWidget(self)
        self.zero.setFont(QFont(font, 12))
        self.zero.resize(91, 81)
        self.zero.move(670, 80)

        self.main_length = QLabel('', self)
        self.main_length.setFont(QFont(font, 12))
        self.main_length.resize(51, 16)
        self.main_length.move(640, 170)
        
        theta = QLabel('θ₀ :', self)
        theta.setFont(QFont(font, 14))
        theta.move(610, 170)
        theta.resize(31, 16)

        theta3dB = QLabel('θ₀̣₅:', self)
        theta3dB.setFont(QFont(font, 14))
        theta3dB.move(610, 200)
        theta3dB.resize(31, 16)

        self.main_length_3dB = QLabel('', self)
        self.main_length_3dB.setFont(QFont(font, 12))
        self.main_length_3dB.move(640, 200)
        self.main_length_3dB.resize(51, 16)

    def analyze_button_clicked(self):
        '''
        '''

        self.vm.analyze_button_clicked(int(self.textbox.text()))
        self.textbox.setText(str(self.vm._phi))

        self.zero.clear()
        for angle in self.vm._angles_of_zero:
            self.zero.addItem(angle)
        
        self.graph1.plot(self.vm._cartesian_coords[:, 0], self.vm._cartesian_coords[:, 1], True)
        if self.vm._mindB < self.vm._3dB[0]:
            self.graph1.plot(self.vm._cartesian_coords[:, 0], self.vm._3dB[:-1], False, label = "-3dB", linestyle="--")


        self.graph2.plot(self.vm._polar_coords[:, 0], self.vm._polar_coords[:, 1], True)
        if self.vm._mindB < self.vm._3dB[0]:
            self.graph2.plot(self.vm._polar_coords[:, 0], self.vm._3dB, False, c = "r", linestyle="--", label = "-3дБ")


        ##self.main_length.setText(str(self.vm._main_length) + "°")
        #self.main_length_3dB.setText(str(self.vm._main_length_3dB) + "°")
        #self.direction.setText(str(int(self.vm._direction)) + "°")
        
        
    def save_button_clicked(self):
        fileName, _ = QFileDialog.getSaveFileName(self, '',"normal(" + self.textbox.text() + ").png", '*.png')
        if fileName:
            pass
        fileName, _ = QFileDialog.getSaveFileName(self, '',"polar(" + self.textbox.text() + ").png", '*.png')
        if fileName:
            pass
        fileName, _ = QFileDialog.getSaveFileName(self, '',"3DView.png", '*.png')
        if fileName:
            pass
