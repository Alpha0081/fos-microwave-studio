import sys 

from GUI.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
from dev.config import config
from time import sleep

print(config.language, config.system, config.language_default)
app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec_())
