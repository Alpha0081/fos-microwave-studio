from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy
import matplotlib.pyplot as plt


class PlotCanvas(FigureCanvas):
    '''
    Class for 
    '''
    def __init__(self, parent, type_graph):
        self.figure = Figure()
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        self.type = type_graph
        if type_graph == "normal":
            self.ax = self.figure.add_subplot(1, 1, 1)
        else:
            self.ax = self.figure.add_subplot(1, 1, 1, projection = "polar")
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
    def set_label_axes(self, x, y):
        self.x_label = x
        self.y_label = y

    def plot(self, x, y, clear: bool, label = "ДН", c = "b", linestyle = "solid"):
        if clear:
            self.ax.clear()
        if self.type == "normal":
            self.ax.plot(x, y, linestyle = linestyle, label = label)         
            self.ax.set_xlabel(self.x_label)
            self.ax.set_ylabel(self.y_label)  
            self.ax.legend(loc = "upper right")     
        else:
            self.ax.plot(x, y, linestyle = linestyle, c = c)
        self.ax.grid(True)
        self.draw()
    