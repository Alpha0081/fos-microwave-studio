import matplotlib.pyplot as plt
class AnalyzeData():
    def __init__(self, parent, fname):
        self.phi = []
        self.dB = []
        self.parent = parent
        self.fname = fname

    def show(self, status, name):
        if status:
            plt.axes(projection='polar')
        plt.plot(self.phi, self.dB, '.')       

        plt.savefig(name)
    
    def analyze(self, phi):
        self.phi = []
        self.dB = []
        k = (phi - 90) / -5
        with open(self.fname) as t:
            for i, line in enumerate(t):
                if i > 72 * k + 2 and i < 75 + 72 * k:
                    nums = []
                    num = ""
                    for sym in line:
                        if sym != ' ':
                            num += sym
                        elif len(num) > 0 and sym == ' ':
                            nums.append(float(num))
                            num = ""
                    self.phi.append(nums[0])
                    self.dB.append(nums[2])
        t.close()
