import matplotlib.pyplot as plt
from dev.interpolation import Interpolation

class AnalyzeData():
    def __init__(self, parent, fname):
        self.phi = []
        self.dB = []
        self.parent = parent
        self.fname = fname
        

    def show(self, name, status):
        if status:
            plt.polar(self.theta, self.dB, '.', color = 'blue')
        else:
            plt.plot(self.theta, self.dB, '.', color = 'blue')
            plt.xlabel("θ")
            plt.ylabel("dB")
        plt.savefig(name)
        plt.close()
        
    def read_file(self, phi):
        '''
            Метод для чтения данных из файла.
        '''
        delta = self.delta
        self.theta = [0] * (72 + (73 * delta) + 2)
        self.dB = [0] * (72 + (73 * delta) + 2)
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
    
    delta = 0
