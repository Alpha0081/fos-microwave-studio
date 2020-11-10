from models.analyzedata import AnalyzeData
from pyqtgraph import glColor, QtGui, mkPen, QtCore
from math import sin, cos, pi
import pyqtgraph.opengl as gl
import numpy as np


class Importvm:
    def __init__(self, name):
        self._data = AnalyzeData(self, name)
        self.__normal_size = self._data.dB.size 
        self._tracesTheta = {}
        self._tracesPhi = {}
        self._previous_phi = -90
        for i in range(90, -91, -5):
            self._tracesTheta[i] = gl.GLLinePlotItem(pos = self._data.to_spherical(i))
        for i in range(-180, 176, 5):
            self._tracesPhi[i] = gl.GLLinePlotItem(pos = self._data.to_spherical(i, i))
        self._phi = -90
        self._angles_of_zero = []

        self._pts_previous = None
        self._pts_current = None


    def analyze_button_clicked(self, phi, interpolation_state):
        self._polar_grid = []
        
        phi = phi - (phi % 5)
        if phi > 90:
            phi = 90
        if phi < -90:
            phi = -90
        self._phi = phi
        
        if interpolation_state:
            self._data.delta = 1
            self._cartesian_coords = np.zeros((self.__normal_size * 2 - 1, 2))
            self._polar_coords = np.zeros((self.__normal_size * 2, 2))
        else:
            self._data.delta = 0
            self._cartesian_coords = np.zeros((self.__normal_size, 2))
            self._polar_coords = np.zeros((self.__normal_size + 1, 2))
            
        self._data.analyze(phi)
        
        self._angles_of_zero = self._data.get_zeros()
        
        self._cartesian_coords[:, 0] = self._data.theta
        self._cartesian_coords[:, 1] = self._data.dB
        
        self._polar_coords[:, 0], self._polar_coords[:, 1] = self._data.to_polar()
        
        
        self._pts_previous = self._data.to_spherical(self._previous_phi)
        self._pts_current = self._data.to_spherical(self._phi)      

        self._tracesTheta[self._previous_phi].setData(pos = self._pts_previous, color = glColor((255, 255, 255))) 
        self._tracesTheta[self._phi].setData(pos = self._pts_current, color = glColor((255, 0, 0)))
        
        self._main_length = self._data.get_length()
        self._main_length_3dB = self._data.get_length_3dB()
        
        tmp = self._data.get_direction_of_maximum()
        self._direction = tmp[0]
        
        self._circles = []
        self._dB = []
        self._maxR = ((self._data.dB.max() + 5 - self._data.mindB) // 10 + 2) * 10
        maxdB = (self._data.dB.max()) // 10 * 10
        for i in range(int(self._maxR / 10) - 2):
            r = self._maxR - 10 * (i + 2) + self._data.dB.max()
            self._circles.append(QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2))
            self._circles[i].setPen(mkPen(0.2))
            self._dB.append([str(maxdB - 10 * i), QtCore.QPointF(0, -r)])
        
        self._lines_grid = []
        for i in range(90, -90, -30):
            x = np.array([self._maxR * cos(i * pi / 180), self._maxR * cos(i * pi / 180 + pi)])
            y = np.array([self._maxR * sin(i * pi / 180), self._maxR * sin(i * pi / 180 + pi)])
            self._lines_grid.append(np.vstack([x, y]).transpose())
        
        self._circles.append(QtGui.QGraphicsEllipseItem(-self._maxR, -self._maxR, self._maxR * 2, self._maxR * 2))
        self._circles[-1].setPen(mkPen(0.2))        
        
        
        self._degrees = []
        for i in range(-180, 180, 30):
            self._degrees.append([str(i), QtCore.QPointF(self._maxR * cos(i * pi / 180), self._maxR * sin(i * pi / 180))])

        self._previous_phi = phi
