from models.analyzefarfield import AnalyzeFarfieldFile
import numpy as np

class FarfieldAnalyzerViewModel:
    def __init__(self, name):
        self._data = AnalyzeFarfieldFile(self, name)
        self.__normal_size = self._data.dB.size 
        self._spherical_x, self._spherical_y, self._spherical_z = self._data.spherical_to_cartesian()  


    def analyze_button_clicked(self, phi):
        
        phi = phi - (phi % 5)
        if phi > 360:
            phi = 360
        elif phi < 0:
            phi = 0
        assert 0 <= phi <= 360, "ValueOutOfRange"
        self._phi = phi

        self._cartesian_coords = np.zeros((37, 2))
        self._polar_coords = np.zeros((37, 2))
            
        
        #self._angles_of_zero = self._data.get_zeros(phi)
        self._cartesian_coords[:, 0] = np.linspace(0, 180, 37)
        self._cartesian_coords[:, 1] = self._data.dB[phi // 5]
        
        self._polar_coords[:, 0], self._polar_coords[:, 1] = self._data.to_polar(phi)
        
        
        #self._main_length = self._data.get_width(phi)
        #self._main_length_3dB = self._data.get_width_3dB(phi)
        self._3dB = np.linspace(self._data.get_3dB(phi), self._data.get_3dB(phi), self._polar_coords[:, 0].size)
        self._mindB = self._data.dB.min()

        #tmp = self._data.get_direction_of_maximum(phi)
        #self._direction = tmp[0]
 

        #self._previous_phi = phi