import sys 

from view.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
from models.config import config
from time import sleep

app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
