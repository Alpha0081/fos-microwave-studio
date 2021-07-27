from models.analyzedata import AnalyzeData
from math import sin, cos, pi
import numpy as np


class Importvm:
    def __init__(self, name):
        self._data = AnalyzeData(self, name)
        self.__normal_size = self._data.dB.size 
        self._tracesTheta = {}
        self._tracesPhi = {}
        self._previous_phi = -90
        self._spherical_x, self._spherical_y, self._spherical_z = self._data.to_spherical()  
        self._phi = 0
        self._angles_of_zero = []

        self._pts_previous = None
        self._pts_current = None


    def analyze_button_clicked(self, phi):
        
        phi = phi - (phi % 5)
        if phi > 360:
            phi = 360
        if phi < 0:
            phi = 0
        self._phi = phi

        self._cartesian_coords = np.zeros((37, 2))
        self._polar_coords = np.zeros((37, 2))
            
        
        #self._angles_of_zero = self._data.get_zeros(phi)
        self._cartesian_coords[:, 0] = np.linspace(0, 180, 37)
        self._cartesian_coords[:, 1] = self._data.dB[phi // 5]
        
        self._polar_coords[:, 0], self._polar_coords[:, 1] = self._data.to_polar(phi)
        
        
        #self._main_length = self._data.get_length(phi)
        #self._main_length_3dB = self._data.get_length_3dB(phi)
        self._3dB = np.linspace(self._data.get_3dB(phi), self._data.get_3dB(phi), self._polar_coords[:, 0].size)
        self._mindB = self._data.dB.min()

        #tmp = self._data.get_direction_of_maximum(phi)
        #self._direction = tmp[0]
 

        #self._previous_phi = phi
