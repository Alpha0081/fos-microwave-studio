from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

class Plot3DCanvas(FigureCanvas):
    def __init__(self, parent):
        self.figure = Figure()
        self.ax = self.figure.add_subplot(1, 1, 1, projection = "3d")
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, x, y, z):
        self.ax.plot_surface(x, y, z, cmap = cm.get_cmap('jet'))
        self.ax.axis('off')
        self.draw()
