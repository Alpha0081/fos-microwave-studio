import matplotlib.pyplot as plt
from dev.interpolation import Interpolation
from math import cos, pi, sin
import numpy as np

class AnalyzeData():
    def __init__(self, parent, fname):
        self.parent = parent
        self.fname = fname
        self.read_file(90, None)
        self.mindB = self.dB.min()
        for i in range(85, -91, -5):
            self.read_file(i, None)
            if self.mindB > self.dB.min():
                self.mindB = self.dB.min()
        
        
    def read_file(self, theta, phi):
        '''
            Метод для чтения данных из файла.
        '''
        if phi is None:
            delta = self.delta
            self.theta = np.zeros(72 + (73 * delta) + 2)
            self.dB = np.zeros(72 + (73 * delta) + 2)
            count = 1 + delta
            k = (theta + 90) / 5
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
        else:
            if phi == 165:
                print("OK")
            self.theta = np.zeros(37)
            self.dB = np.zeros(37)
            k = (phi + 180) / 5
            print(k)
            count = 0
            with open(self.fname) as t:
                for i, line in enumerate(t):
                    if i == 0:
                        print("Yes")
                    if (i - 2) % 72 == k and i >= 2:
                        nums = []
                        num = ""
                        for sym in line:
                            if sym != ' ':
                                num += sym
                            elif len(num) > 0 and sym == ' ':
                                nums.append(float(num))
                                num = ""
                        if phi == -180:
                            print(nums)
                        self.theta[count] = nums[1]
                        self.dB[count] = nums[2]
                        count += 1
            t.close()

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
        self.read_file(phi, None)
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
    
    def to_spherical(self, phi, theta = None):
        if theta is None:
            self.analyze(phi)
            x = np.zeros(self.dB.size + 1)
            y = np.zeros(self.dB.size + 1)
            z = np.zeros(self.dB.size + 1)
            x[:-1] = (self.dB + 5 - self.mindB) * np.cos(self.theta * pi / 180) * cos(phi * pi / 180) 
            y[:-1] = (self.dB + 5 - self.mindB) * np.sin(self.theta * pi / 180) * cos(phi * pi / 180)
            z[:-1] = (self.dB + 5 - self.mindB) * sin(phi * pi / 180)
            x[-1] = x[0]
            y[-1] = y[0]
            z[-1] = z[0]
        else:
            self.read_file(None, theta)
            x = (self.dB + 5 - self.mindB) * cos(theta * pi / 180) * np.cos(self.theta * pi / 180) 
            y = (self.dB + 5 - self.mindB) * sin(theta * pi / 180) * np.cos(self.theta * pi / 180)
            z = (self.dB + 5 - self.mindB) * np.sin(self.theta * pi / 180)
        return np.vstack([x, y, z]).transpose()
        
    def to_polygon(self, phi):
        self.read_file(None, phi)
        x = (self.dB + 5 - self.mindB) * np.cos(phi * pi / 180) * np.cos(self.theta * pi / 180)
        y = (self.dB + 5 - self.mindB) * np.sin(phi * pi / 180) * np.cos(self.theta * pi / 180)
        z = ((self.dB + 5 - self.mindB) ** 2 - x.reshape(x.size, 1) ** 2 - y ** 2) ** .5
        print(z.ndim) 
        return x, y, z
    
    delta = 0
    
