from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
from models.config import config
from viewmodels.farfieldanalyzervm import FarfieldAnalyzerViewModel
from viewmodels.plotcanvas import PlotCanvas, PlotType
from viewmodels.plot3dcanvas import Plot3DCanvas



class FarfieldAnalyzer(QWidget):
    def __init__(self, parent, name):
        #ont = config.font
        super().__init__(parent, Qt.Window)
        self.vm = FarfieldAnalyzerViewModel(name)

        uic.loadUi("GUI/farfieldanalyzer.ui", self)

        self.plot_3d = Plot3DCanvas(self.plot_tabs.widget(2))
        self.plot_3d.plot(self.vm._spherical_x, self.vm._spherical_y, 
            self.vm._spherical_z)
        self.plot_3d.resize(508, 480)

        self.cartesian_plot = PlotCanvas(self.plot_tabs.widget(0),
            PlotType.CARTESIAN)
        self.cartesian_plot.resize(508, 480)
        self.cartesian_plot.set_label_axes("θ","dB")

        self.polar_plot = PlotCanvas(self.plot_tabs.widget(1), PlotType.POLAR)
        self.polar_plot.resize(508, 480)

        self.analyze_button.clicked.connect(self.clicked_analyze_button)
        

    def clicked_analyze_button(self):
        '''
        '''

        #self.vm.analyze_button_clicked(int(self.textbox.text()))
        #self.textbox.setText(str(self.vm._phi))

        #self.zero.clear()
        #for angle in self.vm._angles_of_zero:
        #    self.zero.addItem(angle)
        
        self.vm.analyze_button_clicked(90)

        self.cartesian_plot.plot(self.vm._cartesian_coords[:, 0], self.vm._cartesian_coords[:, 1], True)
        if self.vm._mindB < self.vm._3dB[0]:
            self.cartesian_plot.plot(self.vm._cartesian_coords[:, 0], self.vm._3dB[:-1], False, label = "-3dB", linestyle="--")


        self.polar_plot.plot(self.vm._polar_coords[:, 0], self.vm._polar_coords[:, 1], True)
        if self.vm._mindB < self.vm._3dB[0]:
            self.polar_plot.plot(self.vm._polar_coords[:, 0], self.vm._3dB, False, c = "r", linestyle="--", label = "-3дБ")


        ##self.main_length.setText(str(self.vm._main_length) + "°")
        #self.main_length_3dB.setText(str(self.vm._main_length_3dB) + "°")
        #self.direction.setText(str(int(self.vm._direction)) + "°")
        
        
    def clicked_save_button(self):
        fileName, _ = QFileDialog.getSaveFileName(self, '',"normal(" + self.textbox.text() + ").png", '*.png')
        if fileName:
            pass
        fileName, _ = QFileDialog.getSaveFileName(self, '',"polar(" + self.textbox.text() + ").png", '*.png')
        if fileName:
            pass
        fileName, _ = QFileDialog.getSaveFileName(self, '',"3Dview.png", '*.png')
        if fileName:
            pass
        