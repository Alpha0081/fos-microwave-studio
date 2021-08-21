from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy
import matplotlib.pyplot as plt


class PlotType:
    CARTESIAN = 0
    POLAR = 1
    PLOT3D = 2

class PlotCanvas(FigureCanvas):
    '''
    Class for 
    '''
    def __init__(self, parent, plot_type):
        self.figure = Figure()
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        self.type = plot_type
        if plot_type == PlotType.CARTESIAN:
            self.ax = self.figure.add_subplot(1, 1, 1)
        else:
            self.ax = self.figure.add_subplot(1, 1, 1, projection = "polar")
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, 
            QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
    def set_label_axes(self, x, y):
        self.x_label = x
        self.y_label = y

    def plot(self, x, y, clear: bool, label = "ДН", c = "b", linestyle = "solid"):
        if clear:
            self.ax.clear()
        if self.type == PlotType.CARTESIAN:
            self.ax.plot(x, y, linestyle = linestyle, label = label)         
            self.ax.set_xlabel(self.x_label)
            self.ax.set_ylabel(self.y_label)  
            self.ax.legend(loc = "upper right")     
        else:
            self.ax.plot(x, y, linestyle = linestyle, color = c)
        self.ax.grid(True)
        self.draw()
    