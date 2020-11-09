from PyQt5.QtWidgets import QWidget, QLabel, QTabWidget, QLineEdit, QPushButton, QCheckBox, QListWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QFont, QVector3D
from PyQt5.QtCore import Qt
from dev.analyzedata import AnalyzeData
from os import system
from sys import platform
from shutil import copyfile  
from pathlib import Path
from dev.config import config
import pyqtgraph as pg
from math import sin, cos, pi
import pyqtgraph.opengl as gl
import numpy as np
import pyqtgraph.exporters


class ImportData(QWidget):
    def __init__(self, parent, name):
        font = config.font
        super(QWidget, self).__init__(parent, Qt.Window)
        
        self.data = AnalyzeData(self, name)

        self.setWindowTitle('Import')
        self.setFixedSize(850, 512)
        self.move(0, 50)
        
        self.tabs = QTabWidget(self)
        
        self.graph1 = pg.PlotWidget(self)
        self.graph1.getPlotItem().setLabel('left', "dB")
        self.graph1.getPlotItem().setLabel('bottom', "θ")
        
        self.graph2 = pg.PlotWidget(self)
        self.graph2.getPlotItem().hideAxis('left')
        self.graph2.getPlotItem().hideAxis('bottom')
        
        self.graph3d = gl.GLViewWidget(self)
        self.tracesTheta = {}
        self.tracesPhi = {}
        
        self.surface = {}
        
        self.previous = -90
        for i in range(90, -91, -5):
            self.tracesTheta[i] = gl.GLLinePlotItem(pos = self.data.to_spherical(i), antialias = True)
            self.graph3d.addItem(self.tracesTheta[i])
        for i in range(-180, 176, 5):
            self.tracesPhi[i] = gl.GLLinePlotItem(pos = self.data.to_spherical(i, i), antialias = True)
            self.graph3d.addItem(self.tracesPhi[i])




        
        
        
        
        
        self.graph3d.resize(600, 512)
        self.graph1.resize(600, 512)
        self.graph2.resize(600, 512)

        self.tabs.resize(600, 512)
        self.tabs.addTab(self.graph1, "Normal")
        self.tabs.addTab(self.graph2, "Polar")
        self.tabs.addTab(self.graph3d, "3D View")
        
        self.textbox = QLineEdit(self)
        self.textbox.setText("-90")
        self.textbox.resize(31, 22)
        self.textbox.move(640, 20)
        self.textbox.setFont(QFont(font, 12))
        self.textbox.setMaxLength(3)
        


        btnsave = QPushButton('Save', self)
        btnsave.resize(93, 28)
        btnsave.move(740, 470)
        btnsave.setFont(QFont(font, 12))
        btnsave.clicked.connect(self.save_analyze)
        
        btn = QPushButton('Analyze', self)
        btn.resize(93, 28)
        btn.move(620, 470)
        btn.setFont(QFont(font, 12))
        btn.clicked.connect(self.analyze_button_clicked)        

        self.interpolation = QCheckBox("Use interpolation", self)
        self.interpolation.resize(121, 20)
        self.interpolation.move(690, 20)
        self.interpolation.setFont(QFont(font, 10))

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
        for angle in self.data.get_zeros():
            self.zero.addItem(angle)
        self.graph1.getPlotItem().clear()
        self.graph1.getPlotItem().plot(self.data.theta, self.data.dB)
        self.graph2.getPlotItem().clear()
        tmp = self.data.to_polar()
        self.graph2.getPlotItem().plot(tmp[0], tmp[1])
        
        
        self.tracesTheta[self.previous].setData(pos = self.data.to_spherical(self.previous), color = pg.glColor((255, 255, 255))) 
        self.tracesTheta[phi].setData(pos = self.data.to_spherical(phi), color = pg.glColor((255, 0, 0)))
        
         
        self.main_length.setText(str(self.data.get_length()) + "°")
        self.main_length_3dB.setText(str(self.data.get_length_3dB()) + "°")
        self.direction.setText(str(int(self.data.get_direction_of_maximum()[0])) + "°")
        self.previous = phi
    
    def save_analyze(self):
        fileName, _ = QFileDialog.getSaveFileName(self, '',"normal(" + self.textbox.text() + ").png", '*.png')
        if fileName:
            pg.exporters.ImageExporter(self.graph1.plotItem).export(fileName)
        fileName, _ = QFileDialog.getSaveFileName(self, '',"polar(" + self.textbox.text() + ").png", '*.png')
        if fileName:
            pg.exporters.ImageExporter(self.graph2.plotItem).export(fileName)
        fileName, _ = QFileDialog.getSaveFileName(self, '',"3DView.png", '*.png')
        if fileName:
            self.graph3d.grabFrameBuffer().save(fileName)
