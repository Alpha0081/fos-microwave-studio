import numpy as np
from re import split

class ProgramFileType:
    CST2020 = 0
    CST = 1

class AnalyzeFarfieldFile():
    def __init__(self, parent, file_path):
        self.parent = parent
        self.file_path = file_path

        self.determine_program_file_type()
        self.read_file()

        self.mindB = self.dB.min()
        self.maxdB = self.dB.max()

    def determine_program_file_type(self):
        with open(self.file_path) as farfield_file:
            for line in farfield_file:
                if "Theta" in line:
                    self.program_file_type = ProgramFileType.CST
                    self.dB = np.zeros(2701).reshape(37, 73)
                elif "CST Farfield Source File" in line:
                    self.program_file_type = ProgramFileType.CST2020
                    self.dB = np.zeros(2701).reshape(73, 37)
                else:
                    raise Exception("ProgramFileTypeError")
                break
            farfield_file.close()
        
    @staticmethod
    def check_valid_file_format(file_path):
        is_valid_format = False
        file_format = file_path[-3:]
        if file_format == "txt":
            is_valid_format = True
        elif file_format == "ffs":
            is_valid_format = True
        return is_valid_format
        
    def read_file(self):
        '''Reading txt file for analyze farfield
        '''
        start_line = self.get_start_line()

        assert start_line is not None, "DefinitionStartLineError"

        if self.program_file_type == ProgramFileType.CST2020:
            shape = 37
        elif self.program_file_type == ProgramFileType.CST:
            shape = 73
        with open(self.file_path) as farfield_file:
            for i, line in enumerate(farfield_file):
                if i >= start_line:
                    nums = np.array(split("\s+", line))
                    index = np.where(nums == '')
                    nums = np.delete(nums, index)
                    self.dB[(i - start_line) // shape][(i - start_line)\
                         % shape] = float(nums[2])
            farfield_file.close()
    
    def get_start_line(self):
        with open(self.file_path) as farfield_file:
            for i, line in enumerate(farfield_file):
                line = np.array(split("\s+", line))
                if len(line) >= 6 and self.check_line_contains_values(line):
                    return i
            farfield_file.close()

    def check_line_contains_values(self, line):
        line_contains_values = True
        for value in line:
            if value:
                try:
                    float(value)
                except ValueError:
                    line_contains_values = False
                    break
        return line_contains_values

    def get_direction_of_maximum(self, phi):
        '''Метод для поиска направления максимумов.
        '''
        return self.dB[phi // 5].argmax(), self.dB[phi // 5].max()
        
    def get_width(self, phi):
        theta = np.linspace(0, 180, 37)
        j = i = self.get_direction_of_maximum(phi)[0]
        while self.dB[phi // 5][j] > self.dB[phi // 5][j + 1] and j < 36:
            j+=1
        return 2 * abs(theta[j] - theta[i])
    
    def get_3dB(self, phi):
        return self.dB[phi // 5].max() - 3

    def get_width_3dB(self, phi):
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
        angles = np.linspace(0, np.pi, 37)
        distances = self.dB[phi // 5]
        return angles, distances
    
    def spherical_to_cartesian(self):
        dB = self.dB + abs(self.mindB)
        assert dB.min() == 0, "ValueOutOfRange"
        if self.program_file_type == ProgramFileType.CST2020:
            u = np.linspace(0, 2 * np.pi, 73)
            v = np.linspace(0, np.pi, 37)
        elif self.program_file_type == ProgramFileType.CST:
            v = np.linspace(0, 2 * np.pi, 73)
            u = np.linspace(0, np.pi, 37)

        phi, theta = np.meshgrid(u, v)
        x = dB.transpose() * np.cos(phi) * np.cos(theta)
        z = dB.transpose() * np.sin(phi) * np.cos(theta)
        y = dB.transpose() * np.sin(theta)
        return x, y, z 