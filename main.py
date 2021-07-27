import sys 

from PyQt5.QtWidgets import QApplication
from view.mainwindow import MainWindow
from models.config import config

print("OK")
app = QApplication(sys.argv) 
ex = MainWindow()
sys.exit(app.exec_())
