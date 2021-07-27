import matplotlib.pyplot as plt
from models.interpolation import Interpolation
from math import cos, pi, sin
import numpy as np
from re import split

class AnalyzeData():
    def __init__(self, parent, fname):
        self.parent = parent
        self.fname = fname
        self.read_file()
        self.mindB = self.dB.min()
        self.maxdB = self.dB.max()
        
        
    def read_file(self):
        '''
            Reading txt file for analyze farfield
        '''
        self.dB = np.zeros(2701).reshape(73, 37)
        with open(self.fname) as t:
            for i, line in enumerate(t):
                if i > 30:
                    nums = np.array(split("\s+", line))
                    index = np.where(nums == '')
                    nums = np.delete(nums, index)
                    self.dB[(i - 31) // 37][(i - 31) % 37] = float(nums[2])
            t.close()
                
    def get_direction_of_maximum(self, phi):
        '''
            Метод для поиска направления максимумов.
        '''
        return self.dB[phi // 5].argmax(), self.dB[phi // 5].max()
        
    def get_length(self, phi):
        theta = np.linspace(0, 180, 37)
        j = i = self.get_direction_of_maximum(phi)[0]
        while self.dB[phi // 5][j] > self.dB[phi // 5][j + 1] and j < 36:
            j+=1
        return 2 * abs(theta[j] - theta[i])
    
    def get_3dB(self, phi):
        return self.dB[phi // 5].max() - 3


    def get_length_3dB(self, phi):
        theta = np.linspace(0, 180, 37)
        i = self.get_direction_of_maximum(phi)[0]
        dB = self.dB[phi // 5][i] - 3
        for k in range(i, 37):
            if abs(self.dB[phi // 5][k] - dB) < 0.5:
                break
            else:
                k = i
        return 2 * abs(theta[k] - theta[i])
        
    def get_zeros(self, phi):
        out = []
        theta = np.linspace(0, 180, 37)
        for i, dB in enumerate(self.dB[phi // 5]):
            if abs(dB) < 0.5:
                out.append(str(theta[i]) + "°")
        return out
                
    
    def to_polar(self, phi):

        x = np.linspace(0, np.pi, 37)
        y = self.dB[phi // 5]
        return x, y
    
    def to_spherical(self):
        u = np.linspace(0, 2 * np.pi, 73)
        v = np.linspace(0, np.pi, 37)
        phi, theta = np.meshgrid(u, v)
        x = self.dB.transpose() * np.cos(phi) * np.cos(theta)
        y = self.dB.transpose() * np.sin(phi) * np.cos(theta)
        z = self.dB.transpose() * np.sin(theta)
        return x, y, z 

    
