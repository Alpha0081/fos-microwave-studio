from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from models.analyzefarfield import AnalyzeFarfieldFile
from .farfieldanalyzer import FarfieldAnalyzer
from .setting import Setting

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/mainwindow.ui", self)
        self.action_import_farfield.triggered.connect(self.analyze_farfield)
        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)
        self.show()

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if file_path:
            pass

    def save_file(self):
        file_path = QFileDialog.getSaveFileName(self, 'Open file', '/home')[0]
        if file_path:
            pass
        
    def analyze_farfield(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open file', '/home', \
            'Текстовый файл (*.txt)\nFar-Field Source (*.ffs)\n')[0]
        if file_path:
            assert AnalyzeFarfieldFile.check_valid_file_format(file_path),\
                 "NotValidFileFormat"
            im = FarfieldAnalyzer(self, file_path)     
            im.show()

    def open_settings(self):
        setting = Setting(self)
        setting.show()