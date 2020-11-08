import matplotlib.pyplot as plt
from dev.interpolation import Interpolation
from math import cos, pi, sin
import numpy as np

class AnalyzeData():
    def __init__(self, parent, fname):
        self.parent = parent
        self.fname = fname
        self.read_file(90)
        self.mindB = self.dB.min()
        for i in range(85, -91, -5):
            self.read_file(i)
            if self.mindB > self.dB.min():
                self.mindB = self.dB.min()
        
        
    def read_file(self, phi):
        '''
            Метод для чтения данных из файла.
        '''
        delta = self.delta
        self.theta = np.zeros(72 + (73 * delta) + 2)
        self.dB = np.zeros(72 + (73 * delta) + 2)
        count = 1 + delta
        k = (phi + 90) / 5
        with open(self.fname) as t:
            for i, line in enumerate(t):
                if i > 72 * k + 1 and i < 74 + 72 * k:
                    nums = []
                    num = ""
                    for sym in line:
                        if sym != ' ':
                            num += sym
                        elif len(num) > 0 and sym == ' ':
                            nums.append(float(num))
                            num = ""
                    self.theta[count] = nums[0]
                    self.dB[count] = nums[2]
                    count += (delta + 1)
        t.close()
        for i in range(1, delta + 2):
            self.theta[i - 1] = self.theta[delta + 1]
            self.dB[i - 1] = self.dB[delta + 1]
            self.dB[-i] = self.dB[-delta-2]
            self.theta[-i] = self.theta[-delta-2]

    def use_interpolation(self):
        '''
            Метод для добавление точек в искомый массив с использованием 
            кубической интерполяции.
        '''
        delta = self.delta
        count = (delta + 1) * 3
        for i in range(count, len(self.dB), delta + 1):
            quadro = [self.dB[i], 
                      self.dB[i - (delta + 1)],
                      self.dB[i - 2 * (delta + 1)],
                      self.dB[i - 3 * (delta + 1)]
                      ]
            dtheta = (self.theta[i - (delta + 1)] - self.theta[i - 2 * (delta + 1)]) / (delta + 1)
            for j in range(delta, 0, - 1):
                self.theta[i - 2 * (delta + 1) + j] = self.theta[i - 2 * (delta + 1)] + j * dtheta
                self.dB[i - 2 * (delta + 1) + j] = Interpolation.cubic(quadro, self.theta[i - 2 * (delta + 1) + j], self.theta[i - (delta + 1)])
                
    def get_direction_of_maximum(self):
        '''
            Метод для поиска направления максимумов.
        '''
        maximum = self.dB[0]
        for i, dB in enumerate(self.dB):
            if dB > maximum:
                maximum = dB
                num = i
        return (self.theta[num], num)
        
    def get_length(self):
        j = i = self.get_direction_of_maximum()[1]
        while self.dB[j] > self.dB[j + 1] and j < len(self.theta):
            j+=1
        return 2 * abs(self.theta[j] - self.theta[i])
    
    def get_length_3dB(self):
        i = self.get_direction_of_maximum()[1]
        dB = self.dB[i] - 3
        for k in range(i, len(self.theta)):
            if abs(self.dB[k] - dB) < (0.5 - (self.delta + 1) * 0.1):
                break
            else:
                k = i
        return 2 * abs(self.theta[k] - self.theta[i])
        
    def get_zeros(self):
        out = []
        for i, dB in enumerate(self.dB):
            if abs(dB) < (0.5 - (self.delta + 1) * 0.1):
                out.append(str(self.theta[i]) + "°")
        return out
                
    def analyze(self, phi):
        self.read_file(phi)
        if self.delta:
            self.use_interpolation()
        
    
    def to_polar(self):
        x = np.zeros(self.dB.size + 1)
        y = np.zeros(self.dB.size + 1)
        x[:-1] = (self.dB + 5 - self.mindB) * np.cos(self.theta * pi / 180)
        y[:-1] = (self.dB + 5 - self.mindB) * np.sin(self.theta * pi / 180)
        x[-1] = x[0]
        y[-1] = y[0]
        return x, y
    
    def to_spherical(self, phi):
        x = np.zeros(self.dB.size + 1)
        y = np.zeros(self.dB.size + 1)
        z = np.zeros(self.dB.size + 1)
        self.analyze(phi)
        x[:-1] = (self.dB + 5 - self.mindB) * np.cos(self.theta * pi / 180) * cos(phi * pi / 180) 
        y[:-1] = (self.dB + 5 - self.mindB) * np.sin(self.theta * pi / 180) * cos(phi * pi / 180)
        z[:-1] = (self.dB + 5 - self.mindB) * sin(phi * pi / 180)
        x[-1] = x[0]
        y[-1] = y[0]
        z[-1] = z[0]
        return np.vstack([x, y, z]).transpose()
        

    
    delta = 0
    
